__all__ = ["config"]

import asyncio
import nest_asyncio
import atexit
import json
import os
import re
from json.decoder import WHITESPACE

import config as ext_config_mod
from config import Configuration
from config.helpers import interpolate_object
from eventemitter import EventEmitter
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from refinitiv.dataplatform.tools._common import get_from_path


def _get_filepath(rootdir, filename):
    if rootdir and filename:
        path = os.path.join(rootdir, filename)
        return path


_SUBS_PATTERN = re.compile(r'.*?\${(\w+(-\w+)*(_\w+)*(:\w+)*)}.*?')


def _substitute_values(data, root=None):
    if not data:
        return data

    for k, v in data.items():
        if hasattr(v, "get"):
            _substitute_values(v, root)
        elif isinstance(v, str):
            match = _SUBS_PATTERN.findall(v)
            if match:
                for g in match:
                    path = g[0]
                    old = f"${{{path}}}"
                    new = get_from_path(root, path, ":")
                    new = None if isinstance(new, list) else new
                    v = v.replace(old, new or old)
                data[k] = v
    return data


def _read_config_file(path):
    try:
        with open(path, 'r') as f:
            data = json.load(f, cls=_JSONDecoder)
    except Exception:
        return {}

    return _substitute_values(data, data)


def _create_configs(files_paths):
    config_from_dict = ext_config_mod.config_from_dict
    dicts = [_read_config_file(f) for f in files_paths]
    configs = [config_from_dict(d) for d in dicts]
    return configs


def _create_rdpconfig(files_paths):
    configs = _create_configs(files_paths)
    return _RDPConfig(*configs)


class _RDPConfigChangedHandler(PatternMatchingEventHandler):

    def on_any_event(self, event):
        config.configs = _create_configs(_config_files_paths)
        try:
            config.emit('update')
        except Exception:
            pass


class _JSONDecoder(json.JSONDecoder):
    _ENV_SUBS_PATTERN = re.compile(r'.*?\${(\w+)}.*?')

    def decode(self, s, _w=WHITESPACE.match):
        match = self._ENV_SUBS_PATTERN.findall(s)
        if match:
            for g in match:
                s = s.replace(f'${{{g}}}', os.environ.get(g, g))
            s = s.replace('\\', '\\\\')
        return super().decode(s, _w)


class _RDPConfig(ext_config_mod.ConfigurationSet):
    def __init__(self, *configs):
        super().__init__(*configs)

        try:
            asyncio.get_event_loop()
        except RuntimeError:
            asyncio.set_event_loop(asyncio.new_event_loop())

        nest_asyncio.apply(asyncio.get_event_loop())

        self._emitter = EventEmitter()
        setattr(self, "on", self._emitter.on)
        setattr(self, "remove_listener", self._emitter.remove_listener)
        setattr(self, "emit", self._emitter.emit)

    def _from_configs(self, attr, *args, **kwargs):
        last_err = Exception()
        values = []
        for config_ in self._configs:
            try:
                values.append(getattr(config_, attr)(*args, **kwargs))
            except Exception as err:
                last_err = err
                continue
        if not values:
            # raise the last error
            raise last_err
        if all(isinstance(v, Configuration) for v in values):
            result: dict = {}
            for v in values[::-1]:
                result.update(v)
            return Configuration(result)
        elif isinstance(values[0], Configuration):
            result = {}
            for v in values[::-1]:
                if not isinstance(v, Configuration):
                    continue
                result.update(v)
            return Configuration(result)
        elif self._interpolate:
            return interpolate_object(values[0], self.as_dict())
        else:
            return values[0]


def unload():
    if _observer:
        _observer.stop()
        _observer.join()


_RDPLIB_ENV = 'RDPLIB_ENV'
_RDPLIB_ENV_DIR = 'RDPLIB_ENV_DIR'

_config_filename_template = 'rdplibconfig.%s.json'
_default_env_name = 'prod'
_default_config_filename = _config_filename_template % _default_env_name

_env_name = os.environ.get(_RDPLIB_ENV, _default_env_name)
_config_filename = _config_filename_template % _env_name
_project_config_dir = os.environ.get(_RDPLIB_ENV_DIR) or os.getcwd()
_config_files_paths = [c for c in [
    _get_filepath(rootdir=_project_config_dir, filename=_config_filename),  # PROJECT_CONFIG_FILE
    _get_filepath(rootdir=os.path.expanduser('~'), filename=_config_filename),  # USER_CONFIG_FILE
    _get_filepath(rootdir=os.path.dirname(__file__), filename=_config_filename),  # DEFAULT_CONFIG_FILE

    ] if c]

config = _create_rdpconfig(_config_files_paths)

_watch_enabled = config.get('watch-enabled')
_observer = None
if _watch_enabled:
    _observer = Observer()
    _event_handler = _RDPConfigChangedHandler(patterns=_config_files_paths)
    _dir_names = {os.path.dirname(f) for f in _config_files_paths}
    [_observer.schedule(_event_handler, dirname)
     for dirname in _dir_names]
    _observer.start()

    atexit.register(unload)

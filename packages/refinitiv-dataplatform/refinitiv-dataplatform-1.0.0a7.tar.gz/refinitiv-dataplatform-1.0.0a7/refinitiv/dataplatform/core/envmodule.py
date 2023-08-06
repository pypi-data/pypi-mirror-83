# coding: utf8

__all__ = ['Environment', 'create_env']

import copy

from config import config_from_dict, Configuration

from refinitiv.dataplatform import configure
from refinitiv.dataplatform.errors import EnvError


class Environment(object):

    def __init__(self, name, url_by_content):
        if isinstance(url_by_content, dict):
            url_by_content = config_from_dict(url_by_content)
        self.name = name
        self.url_by_content = url_by_content

    def __contains__(self, content):
        return content in self.url_by_content

    def get_url(self, content_key):
        return self.url_by_content.get(content_key)

    def get_url_or_raise_error(self, content_key):
        rv = self.get_url(content_key) or self.raise_if_not_available(content_key)
        return rv

    def raise_if_not_available(self, content_key):
        has = content_key in self
        if not has:
            has = self.url_by_content.get(content_key)
        if not has:
            raise EnvError(1, f'{content_key} not available in environment {self.name}')

    def clone(self):
        return Environment(self.name, self.url_by_content.copy())

    def get_str(self, content_key):
        return self.url_by_content.get_str(content_key)

    def get_keys(self, content_key):
        content_dict = self.url_by_content.get_dict(content_key)
        keys = set()
        for key in content_dict.keys():
            key_tuple = key.split('.')
            assert(len(key_tuple)>0)
            keys.add(key_tuple[0])
        return keys

    def get_dict(self, content_key):
        return self.url_by_content.get_dict(content_key)


def create_env(data=None):
    if isinstance(data, Environment):
        env = data.clone()
    elif isinstance(data, str):
        env = Environment(configure.config.get('name'), configure.config)
    elif isinstance(data, dict):
        env = Environment(data.get('name'), copy.deepcopy(data))
    elif isinstance(data, Configuration):
        env = Environment(data.get('name'), data)
    else:
        env = Environment(configure.config.get('name'), configure.config)
    return env

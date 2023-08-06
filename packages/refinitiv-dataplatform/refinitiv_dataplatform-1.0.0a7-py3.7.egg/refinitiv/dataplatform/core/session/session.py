# coding: utf-8

__all__ = ['Session', 'DacsParams']

###############################################################
#
#   STANDARD IMPORTS
#
import abc
import httpx
import asyncio
import nest_asyncio
import requests_async
import logging
import os
import socket
import sys
import warnings
from datetime import datetime
from enum import Enum, unique
from logging.handlers import RotatingFileHandler
from threading import Lock, Event

import collections

from refinitiv.dataplatform.core.envmodule import create_env
from refinitiv.dataplatform.errors import SessionError
from refinitiv.dataplatform import configure
from ._omm_stream_listener import OMMStreamListener
from ._omm_stream_listener._omm_stream_listener_manager import OMMStreamObserver
from ._streaming_chain_listener import StreamingChainListener
from ._streaming_chain_listener._streaming_chain_listener_manager import StreamingChainObserver

###############################################################
#
#   REFINITIV IMPORTS
#

# Load nest_asyncio to allow multiple calls to run_until_complete available
nest_asyncio.apply()


###############################################################
#
#   CLASS DEFINITIONS
#

class DacsParams(object):

    def __init__(self, *args, **kwargs):
        self.deployed_platform_username = kwargs.get("deployed_platform_username", "user")
        self.dacs_application_id = kwargs.get("dacs_application_id", "256")
        self.dacs_position = kwargs.get("dacs_position")
        if self.dacs_position in [None, '']:
            try:
                position_host = socket.gethostname()
                self.dacs_position = "{}/{}".format(socket.gethostbyname(position_host), position_host)
            except socket.gaierror:
                self.dacs_position = "127.0.0.1/net"
        self.authentication_token = kwargs.get("authentication_token")


class EndpointServices(object):
    """ This class is designed to store the endpoint service information that retrieved from discovery endpoint """

    # EndpointService class is designed to store a single endpoint service '
    EndpointService = collections.namedtuple('EndpointService',
                                             ['data_format_list',
                                              'endpoint',
                                              'location_list',
                                              'port',
                                              'provider',
                                              'transport']
                                             )

    #   discovery endpoint response key name
    #   for pricing discovery endpoint beta1
    # DiscoveryEndpointResponseKeyName = 'service'
    #   Default pricing discovery endpoint v1
    DiscoveryEndpointResponseKeyName = 'services'

    def __init__(self, stream_connection_name: str, discovery_endpoint_response_json):
        self._stream_connection_name = stream_connection_name
        self._endpoint_service_list = None

        #   initialize endpoint service list
        self._initialize(discovery_endpoint_response_json)

    @property
    def websocket_authority_list(self):
        return None if len(self._endpoint_service_list) == 0 \
            else ['{}:{}'.format(endpoint_service.endpoint, endpoint_service.port)
                  for endpoint_service in self._endpoint_service_list
                  if endpoint_service.transport == 'websocket'
                  and 'tr_json2' in endpoint_service.data_format_list]

    def get_websocket_authority_list_by_location(self, location_list=None):
        """ get a websocket authority by specific prefer location """
        assert (self._endpoint_service_list is not None)
        assert (len(self._endpoint_service_list) > 0)

        #   filter only websocket and tr2_json endpoint services
        endpoint_services = [endpoint_service for endpoint_service in self._endpoint_service_list
                             if endpoint_service.transport == 'websocket'
                             and 'tr_json2' in endpoint_service.data_format_list]

        #   determine websocket authority
        websocket_authority_list = None
        if location_list is not None:
            #   valid location
            #   loop over all given location for determine websocket authority
            websocket_authority_list = []
            for location in location_list:
                #   get the websocket authority
                this_location_websocket_authority_list = self._get_websocket_authority_list_by_location(
                    endpoint_services, location)
                #   check for valid location
                if this_location_websocket_authority_list is None:
                    #   no valid location
                    raise ValueError(
                        'ERROR!!! region \'{}\' is not valid for the stream connection["{}"] service discovery'.format(
                            location, self._stream_connection_name))
                websocket_authority_list.extend(this_location_websocket_authority_list)
        else:
            #   location is not specific
            websocket_authority_list = self._get_websocket_authority_list_by_location(endpoint_services)

        #   done
        return websocket_authority_list

    @staticmethod
    def _get_websocket_authority_list_by_location(endpoint_services, location=None):
        """ Get a endpoint service by location
                return None if no matched location in the endpoint services
        """

        #   search for location
        websocket_authority_to_num_availability_zones = {}
        for endpoint_service in endpoint_services:
            #   check with the prefer location
            if len(endpoint_service.location_list) == 1 and location in endpoint_service.location_list:
                #   found the location, done
                return endpoint_service

            #   check the location without availability zones
            matched_locations = [endpoint_location
                                 for endpoint_location in endpoint_service.location_list
                                 if location is None or endpoint_location.strip().startswith(location)]

            #   build the websocket_authority
            websocket_authority = '{}:{}'.format(endpoint_service.endpoint, endpoint_service.port)
            websocket_authority_to_num_availability_zones[websocket_authority] = len(matched_locations)

        #   select the maximum availability zones
        websocket_authority = max(websocket_authority_to_num_availability_zones,
                                  key=websocket_authority_to_num_availability_zones.get)
        maximum_availability_zones = websocket_authority_to_num_availability_zones[websocket_authority]

        #   check for no match
        if maximum_availability_zones == 0:
            #   no match on location, return None
            return None

        #   check when more that one maximum
        websocket_authority_list = [k
                                    for k, v in websocket_authority_to_num_availability_zones.items()
                                    if v == maximum_availability_zones]

        #   best matched location with highest availability zones (possible more then one websocket authority)
        return websocket_authority_list

    def _initialize(self, discovery_endpoint_response_json):
        """ Initialize the endpoint service from discovery endpoint response """

        #   extract each endpoint service
        assert self.DiscoveryEndpointResponseKeyName in discovery_endpoint_response_json
        services = discovery_endpoint_response_json[self.DiscoveryEndpointResponseKeyName]

        #   reset the endpoint service list
        self._endpoint_service_list = []

        #   construct each endpoint service object
        for service in services:
            #   extract service information
            #       data format
            assert 'dataFormat' in service
            data_format_list = service['dataFormat']
            #       endpoint
            assert 'endpoint' in service
            endpoint = service['endpoint']
            #       location list
            assert 'location' in service
            location_list = service['location']
            #       port
            assert 'port' in service
            port = service['port']
            #       provider
            assert 'provider' in service
            provider = service['provider']
            #       transport
            assert 'transport' in service
            transport = service['transport']

            #   construct endpoint service
            endpoint_service = self.EndpointService(data_format_list, endpoint, location_list, port, provider, transport)
            #   append to a endpoint service list
            self._endpoint_service_list.append(endpoint_service)


class Session(abc.ABC, OMMStreamObserver, StreamingChainObserver):
    _DUMMY_STATUS_CODE = -1

    @unique
    class State(Enum):
        """
        Define the state of the session.
            Closed : The session is closed and ready to be opened.
            Pending : the session is in a pending state.
                Upon success, the session will move into an open state, otherwise will be closed.
            Open : The session is opened and ready for use.
        """
        Closed = 1
        Pending = 2
        Open = 3

    @classmethod
    def _state_msg(cls, state):
        if isinstance(state, Session.State):
            if state == Session.State.Opened:
                return "Session is Opened"
            if state == Session.State.Closed:
                return "Session is Closed"
            if state == Session.State.Pending:
                return "Session is Pending"
        return "Session is in an unknown state"  # Should not process this code path

    @unique
    class EventCode(Enum):
        """
        Each session can report different status events during it's lifecycle.
            StreamConnecting : Denotes the connection to the stream service within the session is pending.
            StreamConnected : Denotes the connection to the stream service has been successfully established.
            StreamDisconnected : Denotes the connection to the stream service is not established.
            SessionAuthenticationSuccess : Denotes the session has successfully authenticated this client.
            SessionAuthenticationFailed : Denotes the session has failed to authenticate this client.
            StreamAuthenticationSuccess: Denotes the stream has successfully authenticated this client.
            StreamAuthenticationFailed: Denotes the stream has failed to authenticate this client.
            DataRequestOk : The request for content from the sessions data services has completed successfully.
            DataRequestFailed : The request for content from the sessions data services has failed.
        """
        StreamConnecting = 1
        StreamConnected = 2
        StreamDisconnected = 3
        StreamAuthenticationSuccess = 4
        StreamAuthenticationFailed = 5
        StreamReconnecting = 6

        SessionConnecting = 21
        SessionConnected = 22
        SessionDisconnected = 23
        SessionAuthenticationSuccess = 24
        SessionAuthenticationFailed = 25
        SessionReconnecting = 26

        DataRequestOk = 61
        DataRequestFailed = 62

    class Params(object):
        def __init__(self, app_key=None, on_event=None, on_state=None, **kwargs):
            self._app_key = app_key
            self._on_event_cb = on_event
            self._on_state_cb = on_state
            self._dacs_params = DacsParams()

        def app_key(self, app_key):
            if app_key is None:
                raise AttributeError("app_key value can't be None")
            self._app_key = app_key
            return self

        def with_deployed_platform_username(self, user):
            if user:
                self._dacs_params.deployed_platform_username = user
            return self

        def with_dacs_application_id(self, application_id):
            if application_id:
                self._dacs_params.dacs_application_id = application_id
            return self

        def with_dacs_position(self, position):
            if position:
                self._dacs_params.dacs_position = position
            return self

        def on_state(self, on_state):
            self._on_state_cb = on_state
            return self

        def on_event(self, on_event):
            self._on_event_cb = on_event
            return self

    __all_sessions = {}
    __register_session_lock = Lock()
    __session_id_counter = 0

    @classmethod
    def register_session(cls, session):
        with cls.__register_session_lock:
            if not session:
                raise SessionError('Error', 'Try to register unavailable session')
            session_id = session.session_id
            if session_id in cls.__all_sessions:
                return
            session._session_id = cls.__session_id_counter
            cls.__session_id_counter += 1
            cls.__all_sessions[session._session_id] = session

    @classmethod
    def unregister_session(cls, session):
        with cls.__register_session_lock:
            if not session:
                raise SessionError('Error', 'Try to unregister unavailable session')
            session_id = session.session_id
            if session_id is None:
                raise SessionError('Error', 'Try to unregister unavailable session')
            if session_id not in cls.__all_sessions:
                raise SessionError('Error',
                                   'Try to unregister unknown session id {}'.format(session_id))
            cls.__all_sessions.pop(session_id)

    @classmethod
    def get_session(cls, session_id):
        """
        Returns the stream session singleton
        """
        if session_id not in cls.__all_sessions:
            raise SessionError('Error', 'Try to get unknown session id {}'.format(session_id))
        return cls.__all_sessions.get(session_id)

    #   logger properties
    #       name of logger
    _LOGGER_NAME = 'session'
    #       logger file name format
    _LOGGER_FILE_NAME_FORMAT = 'refinitiv-dataplatform.{}.log'
    #       log file name size for rotate
    MAX_LOG_SIZE_MEGABYTES = 10
    MAX_LOG_SIZE_BYTES = MAX_LOG_SIZE_MEGABYTES * 1024 * 1024

    def __init__(
                self,
                app_key,
                on_state=None,
                on_event=None,
                token=None,
                deployed_platform_username=None,
                dacs_position=None,
                dacs_application_id=None
                ):
        if app_key is None:
            raise AttributeError("app_key value can't be None")

        OMMStreamObserver.__init__(self, self)
        StreamingChainObserver.__init__(self, self)

        self._session_id = None
        self._lock_log = Lock()

        self._logger = None

        self._state = Session.State.Closed
        self._status = Session.EventCode.StreamDisconnected
        self._last_event_code = None
        self._last_event_message = None

        self._last_stream_connection_name = None

        self._app_key = app_key
        self._on_event_cb = on_event
        self._on_state_cb = on_state
        self._access_token = token
        self._dacs_params = DacsParams()

        if deployed_platform_username:
            self._dacs_params.deployed_platform_username = deployed_platform_username
        if dacs_position:
            self._dacs_params.dacs_position = dacs_position
        if dacs_application_id:
            self._dacs_params.dacs_application_id = dacs_application_id

        self._log_path = None
        self._log_level = logging.NOTSET
        self._initialize_logger()

        self._env = create_env()

        ############################################################
        #   multi-websockets support

        #   a mapping dictionary between the stream connection name -> stream connection obj
        self._stream_connection_name_to_stream_connection_dict = {}

        ############################################################
        #   stream connection auto-reconnect support

        #   a mapping dictionary between the stream connection name -> a list of stream ids
        self._stream_connection_name_to_stream_ids_dict = {}

        # parameters for stream websocket
        try:
            self._loop = asyncio.get_event_loop()
            self.log(1, f'Session loop was set to current event loop {self._loop}')
        except RuntimeError:
            self._loop = asyncio.new_event_loop()
            self.log(1, f'Session loop was set with a new event loop {self._loop}')

        nest_asyncio.apply(self._loop)

        # self._streaming_session = None
        self._is_closing = False
        self._login_event = Event()
        self._login_event.clear()

        self.__lock_callback = Lock()
        self._http_session = httpx.AsyncClient()
        self._base_url = u'https://api.edp.thomsonreuters.com'

        self._stream_register_lock = Lock()
        self._all_stream_subscriptions = {}

        # for OMMStreamListener
        self._all_omm_item_stream = dict()
        self._all_omm_stream_listeners = dict()

        # for StreamingChainListener
        self._all_streaming_chains = dict()
        self._all_chains_listeners = dict()

        self._id_request = 0

        def on_config_updated():
            log_level = configure.config.get("log.level")
            log_level = logging._nameToLevel.get(log_level)
            if log_level is not None and log_level != self._log_level:
                self.set_log_level(log_level)

        configure.config.on('update', on_config_updated)
        on_config_updated()

    def __del__(self):
        # Session.unregister_session(self)
        if hasattr(self, "_logger"):
            handlers = self._logger.handlers[:]
            for handler in handlers:
                handler.close()
                self._logger.removeHandler(handler)

    def __delete__(self, instance):
        self.log(1, f'Delete the Session instance {instance}')

    def _set_proxy(self, http, https):
        pass
        # self._http_session.proxies = {"http": http, "https": https}

    def get_open_state(self):
        """
        Returns the session state.
        """
        return self._state

    def is_open(self):
        return self._state == Session.State.Open

    def get_last_event_code(self):
        """
        Returns the last session event code.
        """
        return self._last_event_code

    def get_last_event_message(self):
        """
        Returns the last event message.
        """
        return self._last_event_message

    @property
    def app_key(self):
        """
        Returns the application id.
        """
        return self._app_key

    @app_key.setter
    def app_key(self, app_key):
        """
        Set the application key.
        """
        from refinitiv.dataplatform.legacy.tools import is_string_type

        if app_key is None:
            return
        if not is_string_type(app_key):
            raise AttributeError('application key must be a string')

        self._app_key = app_key

    def set_stream_authentication_token(self, stream_authentication_token):
        """ Set the authentication token to all stream connections """
        #   loop over all stream connection and set authentication token
        for stream_connection in self._stream_connection_name_to_stream_connection_dict.values():
            #   set the authentication token
            stream_connection.set_stream_authentication_token(stream_authentication_token)

    def request_stream_authentication_token(self):
        """ The function is used for requesting new stream authentication token.
                note that currently only Platform session has this functionality.
        """
        pass

    @property
    def session_id(self):
        return self._session_id

    def logger(self):
        return self._logger

    def _get_rdp_url_root(self):
        return ""

    def get_subscription_streams(self, stream_event_id):
        """ get a list of streams that subscription to given id """
        with self._stream_register_lock:
            if stream_event_id is None:
                raise SessionError('Error', 'Try to retrieve undefined stream')
            if stream_event_id in self._all_stream_subscriptions:
                return [self._all_stream_subscriptions[stream_event_id], ]
            return []

    def get_subscription_streams_by_service(self, stream_connection_name: str):
        """ get a lost of streams that subscription on given stream service """
        with self._stream_register_lock:
            #   get a list of stream ids that subscribe to given stream service
            stream_ids = self._stream_connection_name_to_stream_ids_dict.get(stream_connection_name, [])

            #   mapping stream ids to stream objs
            subscription_streams = []
            for stream_id in stream_ids:
                #   get the stream obj from id
                assert (stream_id in self._all_stream_subscriptions)
                stream = self._all_stream_subscriptions[stream_id]

                #   append the stream to the list
                subscription_streams.append(stream)

            #   done
            return subscription_streams

    ############################################################
    #   multi-websockets support

    @abc.abstractmethod
    def _get_stream_status(self, stream_connection_name: str):
        """
        This method is designed for getting a status of given stream service.
        Parameters
        ----------
            a name of stream connection
        Returns
        -------
        enum
            status of stream service.
        """
        pass

    @abc.abstractmethod
    def _set_stream_status(self, stream_connection_name: str, stream_status):
        """
        Set status of given stream service
        Parameters
        ----------
        stream_connection_name
            a name of stream connection
        stream_status
            a status enum of stream
        Returns
        -------
        """
        pass

    @abc.abstractmethod
    def _get_stream_connection_configuration(self, stream_connection_name: str):
        """
        This method is designed to retrieve the stream connection configuration.
        Parameters
        ----------
        stream_connection_name
            a service enum of stream
        Returns
        -------
        obj
            a stream connection configuration object
        """
        pass

    @abc.abstractmethod
    async def _create_and_start_stream_connection(self, stream_connection_name: str):
        """
        This method is designed to construct the stream connection from given stream service
                and start the connection as a separated thread
        Parameters
        ----------
        stream_connection_name
            a service enum of stream
        Returns
        -------
        obj
            a created stream connection object
        """
        pass

    ##################################################
    #   OMM login message for each kind of session ie. desktop, platform or deployed platform

    @abc.abstractmethod
    def get_omm_login_message_key_data(self):
        """
        Return the login message data for omm 'key'
        """
        return None

    ######################################
    # methods to manage log              #
    ######################################
    TRACE = 5
    MAX_LOG_SIZE = 10000000
    FORMAT = '%(asctime)-15s P[%(process)d] [%(threadName)s %(thread)s] %(message)s'

    # FORMAT = '%(asctime) - %(message)s'
    # FORMAT = '%(asctime),%(msecs)d %(levelname)-8s] %(message)s'
    # datefmt = '%Y-%m-%d:%H:%M:%S'
    # FORMAT = '[%(asctime)s] %(levelname)s - %(message)s'

    def set_log_path(self, log_path):
        """
        Set the path where log files will be created.

        Parameters
        ----------
        log_path : path directory

        Default: current directory (beside *.py running file)
        Return True if log_path exists and is writable
        """
        if os.access(log_path, os.W_OK):
            self._log_path = log_path
            return True
        return False

    def _initialize_logger(self):
        # construct the logger object for this session
        self._logger = logging.getLogger(self._LOGGER_NAME)

        # determine log file name
        _filename = self._LOGGER_FILE_NAME_FORMAT.format(datetime.now().strftime('%Y%m%d.%H-%M-%S'))
        # determine log format
        # for file
        _file_formatter = logging.Formatter(
            '[%(asctime)s] - [%(name)s] - [%(levelname)s] - [%(module)s] - [%(funcName)s] - %(message)s'
            )
        # for stream
        _stream_formatter = logging.Formatter(
            '%(asctime)s - Session %(name)s - Thread %(thread)d | %(threadName)s\n%(message)s'
            )

        # construct the file and stream handler
        # file handler
        self._file_handler = logging.handlers.RotatingFileHandler(
            _filename,
            maxBytes=Session.MAX_LOG_SIZE_BYTES,
            backupCount=10,
            encoding='utf-8',
            delay=True
            )
        self._file_handler.setFormatter(_file_formatter)
        self._logger.addHandler(self._file_handler)

        # stream handler
        self._stdout_stream_handler = logging.StreamHandler(sys.stdout)
        self._stdout_stream_handler.setFormatter(_stream_formatter)
        self._logger.addHandler(self._stdout_stream_handler)

        # add an additional level
        logging.addLevelName(5, 'TRACE')

        # redirect log method of this object to the log in logger object
        self.log = self._logger.log
        self.warning = self._logger.warning
        self.error = self._logger.error
        self.debug = self._logger.debug
        self.info = self._logger.info

    def set_log_level(self, log_level):
        """
        Set the log level.
        By default, logs are disabled.

        Parameters
        ----------
        log_level : int
            Possible values from logging module :
            [CRITICAL, FATAL, ERROR, WARNING, WARN, INFO, DEBUG, NOTSET]
        """
        self._logger.setLevel(log_level)
        self._log_level = log_level

        if log_level <= logging.DEBUG:
            # Enable debugging
            self._loop.set_debug(True)

            # Make the threshold for "slow" tasks very very small for
            # illustration. The default is 0.1, or 100 milliseconds.
            self._loop.slow_callback_duration = 0.001

            # Report all mistakes managing asynchronous resources.
            warnings.simplefilter('always', ResourceWarning)

    def get_log_level(self):
        """
        Returns the log level
        """
        return self._logger.level

    def trace(self, message):
        self._logger.log(Session.TRACE, message)

    ######################################
    # methods to open and close session  #
    ######################################
    def open(self):
        if self._state in [Session.State.Pending, Session.State.Open]:
            # session is already opened or is opening
            return self._state
        self._loop.run_until_complete(self.open_async())
        return self._state

    def close(self):
        if self._state == Session.State.Closed:
            return self._state

        if not self._loop.is_closed():
            return self._loop.run_until_complete(self.close_async())
        else:
            return self._close()

    async def open_async(self):
        Session.register_session(self)
        return self._state

    async def close_async(self):
        await self._stop_streaming()
        return self._close()

    def _close(self):
        self._state = Session.State.Closed
        # close all listeners
        self.close_all_omm_streams()
        self.close_all_streaming_chains()
        Session.unregister_session(self)
        return self._state

    async def wait_for_streaming_reconnection(self, stream_connection_name: str):
        """ wait for a streaming reconnection
                Return True if the reconnection is successfully, otherwise False
        """
        #   retrieve the stream connection
        stream_connection = self._stream_connection_name_to_stream_connection_dict[stream_connection_name]

        #   wait for stream connection is ready
        ready_future = stream_connection.ready

        try:
            await ready_future
        except asyncio.CancelledError:
            #   the stream connection is failed to reconnect
            return False

        #   done, connection is ready
        return True

    async def wait_for_streaming(self, stream_connection_name: str):
        await self._start_streaming(stream_connection_name)
        status = self._get_stream_status(stream_connection_name)
        if status is Session.EventCode.StreamConnected:
            return True
        else:
            self.debug("Streaming failed to start")
            return False

    async def _start_streaming(self, stream_connection_name: str):
        """
        Start the stream connection via websocket if the connection doesn't exist,
        otherwise waiting unit the stream connection is ready.
        """
        #   check the current status of this stream service
        status = self._get_stream_status(stream_connection_name)
        stream_connection = None
        if status not in [Session.EventCode.StreamConnected,
                          Session.EventCode.StreamConnecting,
                          Session.EventCode.StreamReconnecting]:
            #   the stream of given service isn't created yet, so create it

            #   set the current status of stream service to pending
            self._set_stream_status(stream_connection_name, Session.EventCode.StreamConnecting)

            #   create new streaming connection by given streaming service
            stream_connection = await self._create_and_start_stream_connection(stream_connection_name)

            #   set as a daemon
            stream_connection.daemon = True

            #   start the stream connection
            stream_connection.start()
        else:
            #   the stream is already started
            stream_connection = self._stream_connection_name_to_stream_connection_dict[stream_connection_name]

        #   waiting for the streaming connection ready
        assert stream_connection is not None
        assert stream_connection.ready is not None
        try:
            await stream_connection.ready
        except asyncio.CancelledError:
            #   cannot connect to the websocket server
            self.error('Streaming connection cannot connect to WebSocket host.')

            #   set the session stream status
            self._set_stream_status(stream_connection_name, Session.EventCode.StreamDisconnected)

            #   join thread
            self.debug('waiting for streaming connection thread terminate properly.')
            stream_connection.join()

        #   get the update status after try to login
        status = self._get_stream_status(stream_connection_name)

        #   done, return status after starting the stream connection
        return status

    def send(self, stream_connection_name: str, message):
        """
        Send message to the corresponding stream service
        """

        #   get the stream connection corresponding to the stream service
        stream_connection = self._stream_connection_name_to_stream_connection_dict.get(stream_connection_name, None)
        if stream_connection:
            #   found the stream connect corresponding to stream service, so send the message via this stream connection
            stream_connection.send(message)
        else:
            #   session doesn't have any stream connection of given stream service
            self.error(f'ERROR!!! session does not has a stream service "{stream_connection_name}".')

    def is_closing(self, stream_connection_name: str):
        assert stream_connection_name in self._stream_connection_name_to_stream_connection_dict
        return self._stream_connection_name_to_stream_connection_dict[stream_connection_name].is_closing

    async def _stop_streaming(self):
        # unblock any wait on login event
        self._is_closing = True
        # if self._streaming_session:
        #     self._streaming_session.is_closing = True
        self._login_event.set()
        self._login_event.clear()
        # self._start_streaming_event.set()

        #   close all stream connection
        for stream_connection_name, stream_connection in self._stream_connection_name_to_stream_connection_dict.items():
            self.debug('closing the stream connection "{}"'.format(stream_connection_name))
            #   call the close() method
            await stream_connection.close_async()

        #   set the session status to be disconnected
        self._status = Session.EventCode.StreamDisconnected

    ##########################################################
    # methods for listeners subscribe / unsubscribe          #
    ##########################################################
    def subscribe(self, listener, with_updates=True):
        if isinstance(listener, OMMStreamListener):
            return self._subscribe_omm_stream(omm_stream_listener=listener, with_updates=with_updates)

        if isinstance(listener, StreamingChainListener):
            return self._subscribe_streaming_chain(chain_listener=listener, with_updates=with_updates)

    async def subscribe_async(self, listener, with_updates=True):
        if isinstance(listener, OMMStreamListener):
            return await self._subscribe_omm_stream_async(omm_stream_listener=listener, with_updates=with_updates)

        if isinstance(listener, StreamingChainListener):
            return await self._subscribe_streaming_chain_async(chain_listener=listener, with_updates=with_updates)

    def unsubscribe(self, listener):
        if isinstance(listener, OMMStreamListener):
            self._unsubscribe_omm_stream(listener)

        if isinstance(listener, StreamingChainListener):
            self._unsubscribe_streaming_chain(chain_listener=listener)

    async def unsubscribe_async(self, listener):
        if isinstance(listener, OMMStreamListener):
            await self.__unsubscribe_omm_stream_async(listener)

        if isinstance(listener, StreamingChainListener):
            await self._unsubscribe_streaming_chain_async(chain_listener=listener)

    ##########################################################
    # Methods for stream register / unregister               #
    ##########################################################
    def _get_new_id(self):
        self._id_request += 1
        return self._id_request

    def _register_stream(self, stream):
        """
        Register new stream to the session.
        The register is done twice (first to the session with stream id, secondly to the service)
        """
        with self._stream_register_lock:
            if stream is None:
                raise SessionError('Error', 'Try to register None subscription')
            if stream.stream_id in self._all_stream_subscriptions:
                # Verify if this stream is attached to a listener
                if self._check_omm_item_stream(stream):
                    return
                raise SessionError('Error', f'Subscription {stream.stream_id} is already registered')

            if stream.stream_id is not None:
                raise SessionError('Error', f'Try to register again subscription {stream.stream_id}')

            ##################################################
            #   register for stream id
            stream._stream_id = self._get_new_id()
            self._all_stream_subscriptions[stream.stream_id] = stream

            ##################################################
            #   register for stream service
            assert stream.connection is not None
            stream_ids = None
            if stream.connection in self._stream_connection_name_to_stream_ids_dict:
                #   append new stream id into the existing stream ids list in the dict
                stream_ids = self._stream_connection_name_to_stream_ids_dict[stream.connection]
            else:
                #   create new list of stream ids for this service
                stream_ids = []
                self._stream_connection_name_to_stream_ids_dict[stream.connection] = stream_ids

            #   append new stream id
            assert stream_ids is not None
            assert stream.stream_id not in stream_ids
            stream_ids.append(stream.stream_id)

    def _unregister_stream(self, stream):
        with self._stream_register_lock:
            if not stream or not stream._stream_id:
                raise SessionError(-1, 'Try to unregister unavailable stream')

            if stream._stream_id not in self._all_stream_subscriptions:
                raise SessionError(-1, f'Try to unregister unknown stream {stream._stream_id} '
                                       f'from session {self.session_id}')

            ##################################################
            #   unregister for stream service
            assert stream.connection is not None
            assert stream.connection in self._stream_connection_name_to_stream_ids_dict

            #   get list of registered stream id for it service
            stream_ids = self._stream_connection_name_to_stream_ids_dict[stream.connection]
            assert stream.stream_id in stream_ids

            #   unregister this stream id
            stream_ids.remove(stream.stream_id)

            ##################################################
            #   unregister for stream id
            self._all_stream_subscriptions.pop(stream._stream_id)
            stream._stream_id = None

    def _get_stream(self, stream_id):
        with self._stream_register_lock:
            if stream_id is None:
                raise SessionError('Error', 'Try to retrieve undefined stream')
            if stream_id in self._all_stream_subscriptions:
                return self._all_stream_subscriptions[stream_id]
            return None

    ##########################################################
    # methods for session callbacks from streaming session   #
    ##########################################################
    def _on_open(self):
        with self.__lock_callback:
            self._state = Session.State.Pending
            pass

    def _on_close(self):
        with self.__lock_callback:
            self._state = Session.State.Closed
            pass

    def _on_state(self, state_code, state_text):
        with self.__lock_callback:
            if isinstance(state_code, Session.State):
                self._state = state_code
                if self._on_state_cb is not None:
                    try:
                        self._on_state_cb(self, state_code, state_text)
                    except Exception as e:
                        self.error(f'on_state user function on session {self.session_id} raised error {e}')

    def _on_event(self, event_code, event_msg, streaming_session_id=None, stream_connection_name=None):
        self.debug(
            f'Session._on_event('
            f'event_code={event_code}, '
            f'event_msg={event_msg}, '
            f'streaming_session_id={streaming_session_id}, '
            f'stream_connection_name={stream_connection_name})'
            )
        with self.__lock_callback:
            #   check the on_event trigger from some of the stream connection or not?
            if stream_connection_name:
                #   this on_event come form stream connection
                assert stream_connection_name in self._stream_connection_name_to_stream_connection_dict
                stream_connection = self._stream_connection_name_to_stream_connection_dict.get(stream_connection_name, None)

                #   validate the event for this session
                if stream_connection:
                    #   valid session that contain the stream connection for this event
                    if streaming_session_id and stream_connection.streaming_session_id == streaming_session_id:

                        #   for session event code
                        if isinstance(event_code, Session.EventCode):
                            #   store the event code to the corresponding stream service
                            self._set_stream_status(stream_connection_name, event_code)

                            #   call the callback function
                            if self._on_event_cb:
                                try:
                                    self._on_event_cb(self, event_code, event_msg)
                                except Exception as e:
                                    self.error(f"on_event user function on session {self.session_id} raised error {e}")
                    else:
                        self.debug(f'Received notification '
                                   f'from another streaming session ({streaming_session_id}) '
                                   f'than current one ({stream_connection.streaming_session_id})')
                else:
                    self.debug(f'Received notification for closed streaming session {streaming_session_id}')
            else:
                #   not stream connection on_event, just call the on_event callback
                #   call the callback function
                if self._on_event_cb:
                    try:
                        self._on_event_cb(self, event_code, event_msg)
                    except Exception as e:
                        self.error(f"on_event user function on session {self.session_id} raised error {e}")

    def process_on_close_event(self):
        self.close()

    ##############################################
    # methods for status reporting               #
    ##############################################
    @staticmethod
    def _report_session_status(self, session, session_status, event_msg):
        _callback = self._get_status_delegate(session_status)
        if _callback is not None:
            json_msg = self._define_results(session_status)[Session.CONTENT] = event_msg
            _callback(session, json_msg)

    def report_session_status(self, session, event_code, event_msg):
        # Report the session status event defined with the eventMsg to the appropriate delegate
        self._last_event_code = event_code
        self._last_event_message = event_msg
        _callback = self._get_status_delegate(event_code)
        if _callback is not None:
            _callback(session, event_code, event_msg)

    def _get_status_delegate(self, event_code):
        _cb = None

        if event_code in [Session.EventCode.SessionAuthenticationSuccess,
                          Session.EventCode.SessionAuthenticationFailed]:
            _cb = self._on_state_cb
        elif event_code not in [self.EventCode.DataRequestOk,
                                self.EventCode.StreamConnecting,
                                self.EventCode.StreamConnected,
                                self.EventCode.StreamDisconnected]:
            _cb = self._on_event_cb
        return _cb

    ############################
    # methods for HTTP request #
    ############################
    async def http_request_async(self, url: str, method=None, headers=None,
                                 data=None, params=None, json=None, closure=None,
                                 auth=None, loop=None, **kwargs):
        if method is None:
            method = 'GET'

        if headers is None:
            headers = {}

        if self._access_token is not None:
            headers["Authorization"] = "Bearer {}".format(self._access_token)

        if closure is not None:
            headers["Closure"] = closure

        headers.update({'x-tr-applicationid': self.app_key})

        _timeout = None
        if "timeout" in kwargs:
            _timeout = kwargs.pop("timeout")
        _allow_redirects = None
        if "allow_redirects" in kwargs:
            _allow_redirects = kwargs.pop("allow_redirects")

        _http_request = httpx.Request(method, url, headers=headers, data=data,
                                      params=params, json=json, **kwargs)

        if _timeout is None:
            _timeout = 60
        kwargs["timeout"] = _timeout
        if _allow_redirects is not None:
            kwargs["allow_redirects"] = _allow_redirects

        self.debug(f'Request to {url}\n'
                   f'\theaders = {headers}\n'
                   f'\tparams = {kwargs.get("params")}')

        try:
            _request_response = await self._http_session.send(_http_request, **kwargs)
            self.log(1, f'HTTP request response {_request_response.status_code}: {_request_response.text}')
            return _request_response

        except Exception as e:
            self.info(f'HTTP request failed: {e!r}')
            response = requests_async.models.Response()
            response.url = url
            response.request = _http_request
            response.code = type(e).__name__
            if hasattr(e, "message"):
                response._content = e.message
                response.reason_phrase = e.message
            else:
                response._content = str(e).encode()
                response.reason_phrase = str(e).encode()
            response.status_code = self._DUMMY_STATUS_CODE
            return response

    def http_request(self, url: str, method=None, headers={}, data=None, params=None,
                     json=None, auth=None, loop=None, **kwargs):
        # Multiple calls to run_until_complete were allowed with nest_asyncio.apply()
        if loop is None:
            loop = self._loop

        response = loop.run_until_complete(self.http_request_async(url, method, headers, data, params, json, auth, **kwargs))
        return response

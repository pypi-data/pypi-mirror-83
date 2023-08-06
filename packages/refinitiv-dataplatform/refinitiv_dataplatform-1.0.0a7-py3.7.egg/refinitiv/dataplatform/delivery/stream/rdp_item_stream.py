# coding: utf-8

###############################################################
#
#   STANDARD IMPORTS
#

import sys

from threading import Lock

###############################################################
#
#   REFINITIV IMPORTS
#

###############################################################
#
#   LOCAL IMPORTS
#

from .rdp_stream import RDPStream
from .rdp_item_stream_callback import RDPItemStreamCallback

###############################################################
#
#   CLASSE DEFINITIONS
#

class RDPItemStream(RDPStream):
    """
    
    Open an RDP item stream.

    Parameters
    ----------
    service: string
    
    universe: list
    
    views: list

    parameters: dict

    extended_params: dict, optional
        Specify optional params
        Default: None

    on_ack: callable object, optional
        Called when an ack is received.
        This callback receives an utf-8 string as argument.
        Default: None

    on_response: callable object, optional
        Called when an reponse is received.
        This callback receives an utf-8 string as argument.
        Default: None

    on_update: callable object, optional
        Called when an update is received.
        This callback receives an utf-8 string as argument.
        Default: None

    on_alarm: callable object, optional
        Called when an alarm is received.
        This callback receives an utf-8 string as argument.
        Default: None

    Raises
    ------
    Exception
        If request fails or if Refinitiv Services return an error

    """

    class Params(object):
        def __init__(self, *args, **kwargs):
            self._service = None
            self._universe = None
            self._views = None
            self._parameters = None
            self._session = None
            self._connection = None
            self._extended_params = None
            self._on_ack = None
            self._on_response = None
            self._on_update = None
            self._on_alarm = None

            if len(args) > 0 and isinstance(args[0], OMMItemStream.Params):
                self.__init_from_params__(args[0])

            if kwargs:
                self._service = kwargs.get('service')
                self._universe = kwargs.get('universe')
                self._views = kwargs.get('views')
                self._parameters = kwargs.get('parameters')
                self._session = kwargs.get('session')
                self._connection = kwargs.get('connection')
                self._extended_params = kwargs.get('extended_params')
                self._on_ack = kwargs.get('on_ack')
                self._on_response = kwargs.get('on_response')
                self._on_update = kwargs.get('on_update')
                self._on_alarm = kwargs.get('on_alarm')

        def __init_from_params__(self, params):
            self._service = getattr(params, 'service', None)
            self._universe = getattr(params, 'universe', None)
            self._views = getattr(params, 'views', None)
            self._parameters = getattr(params, 'parameters', None)
            self._session = getattr(params, 'session', None)
            self._connection = getattr(params, 'connection', None)
            self._extended_params = getattr(params, 'extended_params', None)
            self._on_ack = getattr(params, 'on_ack', None)
            self._on_response = getattr(params, 'on_response', None)
            self._on_update = getattr(params, 'on_update', None)
            self._on_alarm = getattr(params, 'on_alarm', None)

        def service(self, service:str):
            self._service = service
            return self

        def universe(self, universe:list):
            self._universe = universe
            return self

        def views(self, views:list):
            self._views = views
            return self

        def parameters(self, views:dict):
            self._parameters = _parameters
            return self
        
        def session(self, session:object):
            self._session = session
            return self

        def connection(self, connection:str):
            self._connection = connection
            return self

        def with_extended_params(self, extended_params):
            self._extended_params = extended_params
            return self

        def on_ack(self, on_ack):
            self._on_ack = on_ack
            return self

        def on_response(self, on_response):
            self._on_response = on_response
            return self

        def on_update(self, on_update):
            self._on_update = on_update
            return self
        
        def on_alarm(self, on_alarm):
            self._on_alarm = on_alarm
            return self
                
    def __init__(self, session,
                        service:str, universe:list, views:list, parameters:dict,
                        connection:str,
                        extended_params=None,
                        on_ack=None,
                        on_response=None,
                        on_update=None,
                        on_alarm=None):
        RDPStream.__init__(self, session, connection)

        #   lock for callback function
        self.__item_stream_lock = Lock()

        #   set the RDP stream parameters
        #       set in the parent class
        self._service = service
        self._universe = universe
        self._views = views
        self._parameters = parameters

        #   RPD item stream parameters
        self._extended_params = extended_params

        #   callback functions
        self._callback = RDPItemStreamCallback(on_ack_cb=on_ack,
                                                on_response_cb=on_response,
                                                on_update_cb=on_update,
                                                on_alarm_cb=on_alarm)

        #   last callback code and message
        self._message = None
        self._code = None

        #   validate parameters
        if self._session is None:
            raise AttributeError('Session must be defined')


    
    def _on_ack(self, ack):
        with self.__item_stream_lock:
            #   get state of message
            assert 'state' in ack
            ack_state = ack.get('state')
            #   code
            assert 'code' in ack_state
            self._code = ack_state.get('code')
            #   message/text
            assert 'text' in ack_state
            self._message = ack_state.get('text')

            #   call parent class method
            super()._on_ack(ack)

            #   call callback function
            if self._callback.on_ack:
                self._session.debug('RDPItemStream : call on_ack callback.')
                try:
                    self._callback.on_ack(self, ack)
                except Exception as e:
                    self._session.error(f'RDPItemStream on_ack callback raised exception: {e!r}')
                    self._session.debug(f'Traceback:\n {sys.exc_info()[2]}')

    def _on_response(self, response):
        with self.__item_stream_lock:
            #   call parent class method
            super()._on_response(response)

            #   call callback function
            if self._callback.on_response:
                self._session.debug('RDPItemStream : call on_response callback.')
                try:
                    self._callback.on_response(self, response)
                except Exception as e:
                    self._session.error(f'RDPItemStream on_response callback raised exception: {e!r}')
                    self._session.debug(f'Traceback:\n {sys.exc_info()[2]}')

    def _on_update(self, update):
        with self.__item_stream_lock:
            #   call parent class method
            super()._on_update(update)

            #   call callback function
            if self._callback.on_update:
                self._session.debug('RDPItemStream : call on_update callback.')
                try:
                    self._callback.on_update(self, update)
                except Exception as e:
                    self._session.error(f'RDPItemStream on_update callback raised exception: {e!r}')
                    self._session.debug(f'Traceback:\n {sys.exc_info()[2]}')

    def _on_alarm(self, alarm):
        with self.__item_stream_lock:
            #   call parent class method
            super()._on_alarm(alarm)

            #   call callback function
            if self._callback.on_alarm:
                self._session.debug('RDPItemStream : call on_alarm callback.')
                try:
                    self._callback.on_alarm(self, alarm)
                except Exception as e:
                    self._session.error(f'RDPItemStream on_alarm callback raised exception: {e!r}')
                    self._session.debug(f'Traceback:\n {sys.exc_info()[2]}')

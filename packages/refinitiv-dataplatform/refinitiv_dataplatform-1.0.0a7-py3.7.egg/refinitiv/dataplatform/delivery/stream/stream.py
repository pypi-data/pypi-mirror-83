# coding: utf8

__all__ = ['Stream', 'StreamState']

import abc
from enum import Enum, unique
from threading import Lock
from .openable import Openable


@unique
class StreamState(Enum):
    """ Define the state of the Stream.

    Closed  :    The Stream is closed and ready to be opened.
    Pending :    The Stream is in a pending state. Upon success, the Stream will move into an open state,
                    otherwise will be closed.
    Open    :    The Stream is opened.
    Pause   :    The Stream is paused.
    """
    Closed = 1
    Pending = 2
    Open = 3
    Pause = 4


class Stream(Openable, abc.ABC):
    """ This class is designed to be a abstract class. this class manage subscription from websocket.

    It will have a notification message from session when received message from websocket.

    The following are abstract methods
        - async def open_async(self, with_updates=True)
        - async def close_async(self)
    """

    def __init__(self, session, connection=None):
        super().__init__()

        if session is None:
            raise AttributeError("Session is mandatory")

        #   store the streaming connection of this stream
        self._connection = connection if connection is not None else 'pricing'

        self._stream_lock = Lock()
        self._stream_id = None
        self._session = session
        self._loop = session._loop

        self._name = None
        self._service = None
        self._fields = []
        self._domain = None

        self._state = StreamState.Closed

        #   store the subscribe response future
        #       this future is used for waiting until server response from subscription request
        self._subscribe_response_future = None

    @property
    def stream_id(self):
        return self._stream_id

    @property
    def connection(self):
        return self._connection

    # @stream_id.setter
    # def stream_id(self, stream_id):
    #     self._stream_id = stream_id

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    def initialize_subscribe_response_future(self):
        """ Initialize subscribe response future """

        #   check currently subscribe response future
        if self._subscribe_response_future is not None and not self._subscribe_response_future.done():
            #   cancel the previous subscribe response future
            self._loop.call_soon_threadsafe(self._subscribe_response_future.cancel)

        #   create the subscribe response future
        self._subscribe_response_future = self._loop.create_future()

    async def _wait_for_response(self):
        if self.state is StreamState.Open:
            return True

        #   wait for subscribe response future
        await self._subscribe_response_future

        #   stream is ready, so set stream state to open
        self._state = StreamState.Open

    def _send(self, message):
        """ Send a message to the websocket server """
        self._session.debug(f'Stream('
                            f'id={self._stream_id}, name={self._name}, connection={self.connection})'
                            f'.send(message = {message})')
        self._session.send(self.connection, message)

    ################################################
    #    callback functions

    @abc.abstractmethod
    def _on_status(self, status):
        """ callback for status """
        pass

    @abc.abstractmethod
    def _on_reconnect(self, failover_state, stream_state, data_state, state_code, state_text):
        """ Callback when the websocket connection in stream connection is reconnect """
        pass

    def _on_stream_state(self, state):
        self._state = state

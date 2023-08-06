# coding: utf-8

###############################################################
#
#   STANDARD IMPORTS
#

import asyncio

import json

###############################################################
#
#   REFINITIV IMPORTS
#

###############################################################
#
#   LOCAL IMPORTS
#

from .stream import Stream, StreamState

###############################################################
#
#   CLASSE DEFINITIONS
#

class RDPStream(Stream):
    """ this class is designed for the generic RDP stream.

        the following are the subscription message from the stream
    - ack message
    - response message
    - update message
    - alarm message
    """

    def __init__(self, session, connection):
        Stream.__init__(self, session, connection)

        #   store the RDP subscribe description
        self._service = None
        self._universe = None
        self._views = None
        self._parameters = None

        #   store the future object when call the subscribe
        self._subscribe_future = None

    @property
    def service(self):
        return self._service

    @service.setter
    def service(self, val):
        self._service = val
    
    @property
    def universe(self):
        return self._universe

    @universe.setter
    def universe(self, val):
        self._universe = val

    @property
    def views(self):
        return self._views

    @views.setter
    def views(self, val):
        self._views = val

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, val):
        self._parameters = val

    ################################################
    #  methods to open and close asynchronously stream
    
    async def _do_open_async(self, with_updates=True):
        """
        Open asynchronously the data stream
        """
        
        #   register the stream to session
        self._session._register_stream(self)

        #   waiting for stream connection is ready to connect
        assert(self._session is not None)
        assert(callable(self._session.wait_for_streaming))
        result = await self._session.wait_for_streaming(self.connection)
        
        #   check stream connection status
        if result:
        #   successfully connect to the stream, so send the subscription message

            #   initialize response future
            self.initialize_subscribe_response_future()

            #   get the subscription message
            subscription_message = self._get_subscription_request_message()
            self._session.log(5, 'subscription message = {}'.format(subscription_message))
            
            #       send message to stream
            self._send(subscription_message)

        else:
        #   failed to request the stream connection.
            self._state = StreamState.Closed
            self._session.log(1, 'Start streaming failed. Set stream {} as {}'.format(self._stream_id, self._state))

        #   done
        return self._state

    async def _do_close_async(self):
        """
        Close the data stream
            
        example of close for generic RDP streaming
            {
                "streamID": "42", 
                "method": "Close"
            }
        """
        self._session.debug(f'Close Stream subscription {self._stream_id}')

        #   close message
        close_message = {
                            'streamID': f'{self._stream_id:d}',
                            'method': "Close"

                        }

        self._session.debug(f'Sent close subscription:\n'
                            f'{json.dumps(close_message, sort_keys=True, indent=2, separators=(",", ":"))}')
        self._send(close_message)

        #   cancel the previous subscribe response future
        if self._subscribe_response_future:
        #   valid future, so cancel it
            self._loop.call_soon_threadsafe(self._subscribe_response_future.cancel)

        #   unregister stream
        self._session._unregister_stream(self)


    def _do_pause(self):
        # do nothing
        pass

    def _do_resume(self):
        # do nothing
        pass

    ################################################
    #    methods to construct a RDP item subscription

    def _get_subscription_request_message(self):
        """ build the subscription request message 

        example of subscribe messages

            {
                "streamID": "42", 
                "method": "Subscribe",  
                "service": "analytics/bond/contract", 
                "universe": [
                    {
                    "type": "swap", 
                    "definition": {
                        "startDate": "2017-07-28T00:00:00Z", 
                        "swapType": "Vanilla", 
                        "tenor": "3Y"
                    }
                    }
                ], 
                "views": [
                    "InstrumentDescription", 
                    "ValuationDate", 
                    "StartDate", 
                    "EndDate", 
                    "Calendar", 
                    "FixedRate", 
                    "PV01AmountInDealCcy", 
                    "Duration", 
                    "ModifiedDuration", 
                    "ForwardCurveName", 
                    "DiscountCurveName", 
                    "ErrorMessage"
                ]
            }

        or

            {
                "streamID": "43", 
                "method": "Subscribe",  
                "service": "elektron/market-price", 
                "universe": [
                    {
                    "name": "TRI.N"
                    }
                ]
            }

        or

            {
                "streamID": "1",
                "method": "Subscribe",
                "universe": [],
                "parameters": {
                    "universeType": "RIC"
                }
            }
        """

        #   construct subscription message
        subscription_message = { 'streamID': f'{self._stream_id:d}',
                                    'method': 'Subscribe',
                                    'universe': self._universe
                                }
        
        #   check for service and views
        if self._service is not None:
        #   add service into subscription message
            subscription_message['service'] = self._service
        
        #       view
        if self._views is not None:
        #   add views in to subscription message
            subscription_message['views'] = self._views

        #   parameters
        if self._parameters is not None:
        #   add parameters into the subscription message
            subscription_message['parameters'] = self._parameters
        
        #   done
        return subscription_message

    ###############################################################
    #    methods to subscribe/unsubscribe

    async def _subscribe_async(self):
        """
        Subscribe RDP stream.
        The subscription steps are waiting for stream to be ready and send the message to subscribe item.
        """
        self._session.log(5, 'RDPStream.subscribe_async() - waiting for subscribe name = {}'.format(self._name))

        #   waiting for stream to be ready
        result = await self._session.wait_for_streaming_reconnection(self.connection)

        #   check the reconnection result
        if not result:
            # failed to reconnection, so do nothing waiting for next reconnection
            self._session.debug('WARNING!!! the reconnection is failed, so waiting for new reconnection.')
            return

        #   send message to subscribe item
        #       construct open message
        open_message = self._get_subscription_request_message()
        self._session.log(5, 'open message = {}'.format(open_message))

        #       send message to stream
        self._send(open_message)

    ################################################
    #    callback functions

    def _on_status(self, status):
        """ callback for status """
        self._session.debug(f'Stream {self.stream_id} [{self.name}] - Receive status message {status}')

    def _on_reconnect(self, failover_state, stream_state, data_state, state_code, state_text):
        """ callback when the websocket connection in stream connection is reconnect """
        from .stream_connection import StreamConnection

        #   check the failover state for sent the new subscription item
        if failover_state == StreamConnection.FailoverState.FailoverCompleted:
            #   the stream connection failover is completed,
            #       so recover the stream by sent a new subscription item

            #   re-subscribe item
            if self._subscribe_future is None or self._subscribe_future.done():
                #   do a subscription again
                self._subscribe_future = asyncio.run_coroutine_threadsafe(
                    self._subscribe_async(),
                    loop=self._loop)

        #   do call the on_status callback
        #       build status message
        status_message = {'ID': self._stream_id,
                          'Type': 'Status',
                          'Key': {'Name': self.name},
                          'State': {'Stream': stream_state,
                                    'Data': data_state,
                                    'Code': state_code,
                                    'Text': state_text
                                    }
                          }

        #       call a status callback message
        self._on_status(status_message)

    ###############################################################
    #   callback functions when received messages

    def _on_ack(self, ack):
        with self._stream_lock:
            if self._state is StreamState.Open:
                self._session.log(1, f'Stream {self.stream_id} [{self.name}] - Receive ack {ack}')

    def _on_response(self, response):
        with self._stream_lock:
            self._session.log(1, f'Stream {self.stream_id} [{self.name}] - Receive response {response}')
            
            #   change state to be open if it's pending
            if self._state in [StreamState.Pending, StreamState.Closed]:
                self._state = StreamState.Open
                self._session.log(1, 'Set stream {} as {}'.format(self.stream_id, self.state))
                
            #   check this response is a first response of this subscribe item or not
            if self._subscribe_response_future is not None and not self._subscribe_response_future.done():
                #   this is a first subscribe for this stream, so set the future to be True
                self._subscribe_response_future.set_result(True)

    def _on_update(self, update):
        with self._stream_lock:
            if self._state is StreamState.Open:
                self._session.log(1, f'Stream {self.stream_id} [{self.name}] - Receive update {update}')

    def _on_alarm(self, message):
        with self._stream_lock:
            if self._state is StreamState.Open:
                self._session.log(1, f'Stream {self.stream_id} [{self.name}] - Receive alarm {alarm}')

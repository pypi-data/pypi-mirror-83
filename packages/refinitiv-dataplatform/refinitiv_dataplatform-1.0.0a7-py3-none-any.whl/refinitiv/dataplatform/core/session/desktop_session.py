# coding: utf-8

__all__ = ['DesktopSession']

from appdirs import *
import os
import logging
import platform
import socket
import httpx
from refinitiv.dataplatform import __version__, DesktopSessionError
from .session import Session

from refinitiv.dataplatform.core.session.streaming_connection_configuration import StreamingConnectionDesktop
from refinitiv.dataplatform.delivery.stream.omm_stream_connection import OMMStreamConnection


class DesktopSession(Session):
    class Params(Session.Params):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    def __init__(self, app_key, on_state=None, on_event=None, env=None, **kwargs):
        super().__init__(app_key=app_key,
                         on_state=on_state,
                         on_event=on_event,
                         token=kwargs.get("token"),
                         deployed_platform_username=kwargs.get("deployed_platform_username"),
                         dacs_position=kwargs.get("dacs_position"),
                         dacs_application_id=kwargs.get("dacs_application_id"))

        self._port = None
        self._udf_url = None
        self._timeout = 30
        self._user = "root"
        self._check_port_result = False

    def _get_udf_url(self):
        """
        Returns the scripting proxy url.
        """
        return self._udf_url

    def _get_rdp_url_root(self):
        return f"http://127.0.0.1:{self._port}/api/rdp"

    def _get_http_session(self):
        """
        Returns the scripting proxy http session for requests.
        """
        return self._http_session

    def set_timeout(self, timeout):
        """
        Set the timeout for requests.
        """
        self._timeout = timeout

    def get_timeout(self):
        """
        Returns the timeout for requests.
        """
        return self._timeout

    def set_port_number(self, port_number, logger=None):
        """
        Set the port number to reach Desktop API proxy.
        """
        self._port = port_number
        if port_number:
            self._udf_url = f"http://127.0.0.1:{self._port}/api/v1/data"
            self.close()
        else:
            self._udf_url = None

        if logger:
            logger.info(f"Set Proxy port number to {self._port}")

    def get_port_number(self):
        """
        Returns the port number
        """
        return self._port

    def is_session_logged(self, name: str = None):
        """ note that currently the desktop session support only 1 websocket connection """
        name = name or 'pricing'
        assert name in self._stream_connection_name_to_stream_connection_dict
        return self._stream_connection_name_to_stream_connection_dict[name].ready.done()

    ############################################################
    #   multi-websockets support

    def _get_stream_status(self, stream_connection_name: str):
        """ this method is designed for getting a status of given stream service.

        Parameters
        ----------
            a enum of stream service
        Returns
        -------
        enum
            status of stream service.
        """
        return self._status

    def _set_stream_status(self, streaming_connection: str, stream_status):
        """ set status of given stream service

        Parameters
        ----------
        streaming_connection
            a service name of stream
        stream_status
            a status enum of stream
        -------
        """
        self._status = stream_status

    async def _get_stream_connection_configuration(self, stream_connection_name: str):
        """ this method is designed to retrieve the stream connection configuration.
        in the platform session two possible configurations including RDP platform or deployed platform.

        Parameters
        ----------
        stream_connection_name
            a service name of stream
        Returns
        -------
        obj
            a stream connection configuration object
        """
        assert stream_connection_name == 'pricing'

        #  build the streaming connection config
        streaming_connection_config = {'websocket-url': f'127.0.0.1:{self._port}/api/v1/data/streaming/pricing',
                                       'data-format': 'tr_json2',
                                       'header': [f'x-tr-applicationid: {self.app_key}'],
                                       'secure': False,
                                       'dacs_application_id': self._dacs_params.dacs_application_id,
                                       'dacs_username': 'john doe',
                                       'dacs_position': self._dacs_params.dacs_position
                                       }

        #   build new streaming configuration for this desktop session
        streaming_config = StreamingConnectionDesktop(self, name='desktop',
                                                      platform_url=None,
                                                      streaming_connection_config=streaming_connection_config)
        await streaming_config.initialize_streaming_connection_configuration()

        #   done
        return streaming_config

    #   session abstractmethod
    async def _create_and_start_stream_connection(self, stream_connection_name: str):
        """ this method is designed to construct the stream connection from given stream service
                and start the connection as a separated thread

        Parameters
        ----------
        stream_connection_name
            a service name of stream
        Returns
        -------
        obj
            a created stream connection object
        """

        #   get the stream config by given stream service
        stream_config = await self._get_stream_connection_configuration(stream_connection_name)

        #   set the stream connection class by type

        # warning :: DESKTOP SESSION SUPPORT ONLY PRICING
        assert stream_connection_name == 'pricing'
        websocket_thread_name = "WebSocket {}".format(self.session_id)

        stream_connection = OMMStreamConnection(websocket_thread_name, self,
                                                stream_connection_name, stream_config)

        #   store stream connection
        self._stream_connection_name_to_stream_connection_dict[stream_connection_name] = stream_connection

        #   done
        return stream_connection

    ##################################################
    #   OMM login message for each kind of session ie. desktop, platform or deployed platform

    def get_omm_login_message_key_data(self):
        """ return the login message for omm 'key'
        """
        return {
            "Name": "john doe",
            "Elements": {
                "AppKey": self.app_key,
                "ApplicationId": self._dacs_params.dacs_application_id,
                "Position": self._dacs_params.dacs_position
                }
            }

    #######################################
    #  methods to open and close session  #
    #######################################
    def open(self):
        if self._state in [Session.State.Pending, Session.State.Open]:
            # session is already opened or is opening
            return self._state

        # call Session.open() based on open_async() => _init_streaming_config will be called later
        return super(DesktopSession, self).open()

    def close(self):
        return super(DesktopSession, self).close()

    ############################################
    #  methods to open asynchronously session  #
    ############################################
    async def open_async(self):

        def close_state(msg):
            self._state = Session.State.Closed
            self._on_event(Session.EventCode.SessionAuthenticationFailed, msg)
            self._on_state(self._state, "Session is closed.")

        if self._state in [Session.State.Pending, Session.State.Open]:
            # session is already opened or is opening
            return self._state

        error = None
        port_number = await self.identify_scripting_proxy_port()

        if port_number:
            try:
                await self.handshake(port_number)
            except DesktopSessionError as e:
                self.error(e.message)
                error = e

            if not error:
                self.set_port_number(port_number)
                self.info(f"Application ID: {self.app_key}")
                self._state = Session.State.Open
                self._on_state(self._state, "Session is opened.")

        not port_number and close_state("Eikon is not running")
        error and close_state(error.message)
        await super(DesktopSession, self).open_async()
        return self._state

    @staticmethod
    def read_firstline_in_file(filename, logger=None):
        try:
            f = open(filename)
            first_line = f.readline()
            f.close()
            return first_line
        except IOError as e:
            if logger:
                logger.error(f"I/O error({e.errno}): {e.strerror}")
            return ""

    async def identify_scripting_proxy_port(self):
        """
        Returns the port used by the Scripting Proxy stored in a configuration file.
        """

        port = None
        path = []
        app_names = ["Data API Proxy", "Eikon API proxy", "Eikon Scripting Proxy"]
        for app_author in ["Refinitiv", "Thomson Reuters"]:
            if platform.system() == "Linux":
                path = path + [user_config_dir(app_name, app_author, roaming=True)
                               for app_name in app_names
                               if os.path.isdir(user_config_dir(app_name, app_author, roaming=True))]
            else:
                path = path + [user_data_dir(app_name, app_author, roaming=True)
                               for app_name in app_names
                               if os.path.isdir(user_data_dir(app_name, app_author, roaming=True))]

        if len(path):
            port_in_use_file = os.path.join(path[0], ".portInUse")

            # Test if ".portInUse" file exists
            if os.path.exists(port_in_use_file):
                # First test to read .portInUse file
                firstline = self.read_firstline_in_file(port_in_use_file)
                if firstline != "":
                    saved_port = firstline.strip()
                    await self.check_port(saved_port)
                    if self._check_port_result:
                        port = saved_port
                        self.info(f"Port {port} was retrieved from .portInUse file")

        if port is None:
            self.info("Warning: file .portInUse was not found. Try to fallback to default port number.")
            port_list = ["9000", "36036"]
            for port_number in port_list:
                self.info(f"Try defaulting to port {port_number}...")
                await self.check_port(port_number)
                if self._check_port_result:
                    return port_number

        if port is None:
            self.error("Error: no proxy address identified.\nCheck if Desktop is running.")
            return None

        return port

    async def check_port(self, port, timeout=(15.0, 15.0)):
        url = f"http://127.0.0.1:{port}/api/status"
        try:
            response = await self.http_request_async(url=url,
                                                     method="GET",
                                                     # headers=_headers,
                                                     # json=body,
                                                     timeout=timeout,
                                                     allow_redirects=False)

            self.info(f"Checking port {port} response : {response.status_code} - {response.text}")
            self._check_port_result = True
            return
        except (socket.timeout, httpx.ConnectTimeout):
            self.log(logging.INFO, f"Timeout on checking port {port}")
        except ConnectionError as e:
            self.log(logging.INFO, f"Connexion Error on checking port {port} : {e!r}")
        except Exception as e:
            self.debug(f"Error on checking port {port} : {e!r}")
        self._check_port_result = False

    async def handshake(self, port, timeout=(15.0, 15.0)):
        url = f"http://127.0.0.1:{port}/api/handshake"
        self.info(f"Try to handshake on url {url}...")
        try:
            # DAPI for E4 - API Proxy - Handshake
            _body = {
                "AppKey": self.app_key,
                "AppScope": "trapi",
                "ApiVersion": "1",
                "LibraryName": "RDP Python Library",
                "LibraryVersion": __version__
                }

            _headers = {"Content-Type": "application/json"}

            response = None
            try:
                response = await self.http_request_async(url=url,
                                                         method="POST",
                                                         headers=_headers,
                                                         json=_body,
                                                         timeout=timeout,
                                                         allow_redirects=False)

                self.info(f"Response : {response.status_code} - {response.text}")
            except Exception as e:
                self.log(1, f'HTTP request failed: {e!r}')

            if response:
                if response.status_code == httpx.codes.OK:
                    result = response.json()
                    self._access_token = result.get("access_token")
                elif response.status_code == httpx.codes.BAD_REQUEST:
                    self.error(f"Status code {response.status_code}: "
                               f"Bad request on handshake port {port} : {response.text}")
                    key_is_incorrect_msg = f"Status code {response.status_code}: App key is incorrect"
                    self._on_event(Session.EventCode.SessionAuthenticationFailed, key_is_incorrect_msg)
                    raise DesktopSessionError(1, key_is_incorrect_msg)
                else:
                    self.debug(f"Response {response.status_code} on handshake port {port} : {response.text}")

        except (socket.timeout, httpx.ConnectTimeout):
            raise DesktopSessionError(1, f"Timeout on handshake port {port}")
        except Exception as e:
            raise DesktopSessionError(1, f"Error on handshake port {port} : {e!r}")
        except DesktopSessionError as e:
            raise e

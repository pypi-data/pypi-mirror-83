# coding: utf-8

__all__ = ["PlatformSession"]

import logging
from enum import Enum, unique

from refinitiv.dataplatform import configure
from refinitiv.dataplatform.delivery.stream.omm_stream_connection import OMMStreamConnection
from refinitiv.dataplatform.errors import PlatformSessionError
from refinitiv.dataplatform.delivery.stream.rdp_stream_connection import RDPStreamConnection


from .grant import Grant
from .grant_password import GrantPassword
from .grant_refresh import GrantRefreshToken
from .session import Session
from .session_configuration_file_handler import SessionConfigurationFileHandler


class PlatformSession(Session):
    """ This class is designed for handling the session to Refinitiv Data Platform (RDP) or Deployed Platform (TREP)
            - Refinitiv Data Platform are including handling an authentication and a token management (including refreshing token),
                also handling a real-time service discovery to get the service websocket endpoint
                and initialize the login for streaming
            - Deployed Platform is including the login for streaming
    """

    _LOGGER_NAME = "session.platform"

    @unique
    class PlatformConnectionType(Enum):
        """ this enum is designed for connection type because the platform session contains
                both connections to Refinitiv Data Platform (RDP) and Deployed Platform (TREP)
        """
        RefinitivDataplatformConectionOnly = 1
        DeployedPlatformOnly = 2
        RefinitivDataplatformConectionAndDeployedPlatform = 3

    class Params(Session.Params):
        def __init__(self, *args, **kwargs):
            super(PlatformSession.Params, self).__init__(*args, **kwargs)

            self._grant = kwargs.get("grant")
            _signon_control = kwargs.get("signon_control", "False")
            self._take_signon_control = _signon_control.lower() == "true"

            if self._take_signon_control is None:
                self._take_signon_control = False

            #   for deployed platform connection
            self._deployed_platform_host = kwargs.get("deployed_platform_host")

        def get_grant(self):
            return self._grant

        def grant_type(self, grant):
            if isinstance(grant, Grant):
                self._grant = grant
            else:
                raise Exception("wrong Elektron authentication parameter")
            return self

        def take_signon_control(self):
            return self._take_signon_control

        def with_take_signon_control(self, value):
            if value is not None:
                self._take_signon_control = value
            return self

        #   for deployed platform connection
        def deployed_platform_host(self, deployed_platform_host):
            self._deployed_platform_host = deployed_platform_host
            return self

        def with_authentication_token(self, token):
            if token:
                self._dacs_params.authentication_token = token
            return self

    def get_session_params(self):
        return self._session_params

    def session_params(self, session_params):
        self._session_params = session_params
        return session_params

    def _get_rdp_url_root(self):
        return self._env.get_url("platform-url")

    def __init__(
            self,
            app_key=None,
            # for Refinitiv Dataplatform connection
            grant=None, signon_control=None,
            # for Deployed platform connection
            deployed_platform_host=None,
            deployed_platform_connection_name=None,
            authentication_token=None,
            deployed_platform_username=None, dacs_position=None, dacs_application_id=None,
            on_state=None, on_event=None,
            auto_reconnect=None,
            # other
            **kwargs
    ):
        super().__init__(
            app_key,
            on_state=on_state, on_event=on_event,
            deployed_platform_username=deployed_platform_username,
            dacs_position=dacs_position, dacs_application_id=dacs_application_id,
            **kwargs
        )

        #   for Refinitiv Dataplatform connection
        self._ws_endpoints = []

        if grant and isinstance(grant, GrantPassword):
            self._grant = grant

        self._take_signon_control = signon_control if signon_control else True

        self._pending_stream_queue = []
        self._pending_data_queue = []

        self._refresh_grant = GrantRefreshToken()
        self._access_token = None
        self._token_expires_in_secs = 0
        self._token_expires_at = 0

        from .auth_manager import AuthManager

        if auto_reconnect is None:
            auto_reconnect = configure.config.get("auto-reconnect", False)

        self._auth_manager = AuthManager(self, auto_reconnect=auto_reconnect)

        self._websocket_endpoint = None

        # for Deployed platform connection
        self._deployed_platform_connection_name = deployed_platform_connection_name or 'pricing'

        #   building the deployed platform connection dict
        self._deployed_platform_connection_dict = self._create_deployed_platform_connection_dict(deployed_platform_host)

        # classify the connection type
        if grant and deployed_platform_host:
            # both connection to Refinitiv Data Platform (RDP) amd Deployed Platform
            self._connection_type = self.PlatformConnectionType.RefinitivDataplatformConectionAndDeployedPlatform
        elif grant:
            # only RDP connection
            self._connection_type = self.PlatformConnectionType.RefinitivDataplatformConectionOnly
        elif deployed_platform_host:
            # only deployed platform connection
            self._connection_type = self.PlatformConnectionType.DeployedPlatformOnly
        else:
            raise AttributeError(
                f"Error!!! Can't initialize a PlatformSession "
                f"without Refinitiv Data Platform Grant (grant user and password) and Deployed Platform host")

        ############################################################
        #   session configuration 

        #   build the session configuration handler
        self._session_configuration_file_handler = SessionConfigurationFileHandler(self)

        ############################################################
        #   multi-websockets support

        #   a mapping between stream service to config object
        self._stream_connection_name_to_config = {}

        #   initialize all stream status to disconnected
        self._streaming_connection_name_to_status = {}
        for streaming_connection_name in self._session_configuration_file_handler.streaming_connection_names:
            self._streaming_connection_name_to_status[streaming_connection_name] = Session.EventCode.StreamDisconnected

        #   for deployed platform session
        if deployed_platform_host is not None:
            #   initialize the deployed platform status
            self._streaming_connection_name_to_status[self._deployed_platform_connection_name] = Session.EventCode.StreamDisconnected

        #   a mapping between streaming service to endpoint services
        self._endpoint_services_dict = {}

    def _create_deployed_platform_connection_dict(self, deployed_platform_host):
        if deployed_platform_host is not None:
            return {
                f'{self._deployed_platform_connection_name}.type': 'ads-websocket',
                f'{self._deployed_platform_connection_name}.websocket-url': deployed_platform_host,
                f'{self._deployed_platform_connection_name}.dacs_username': self._dacs_params.dacs_application_id,
                f'{self._deployed_platform_connection_name}.dacs_application_id': self._dacs_params.dacs_position,
            }
        else:
            return dict()

    def request_stream_authentication_token(self):
        """ Request new stream authentication token """
        self._loop.run_until_complete(self._auth_manager.authorize())

    ############################################################
    #   session configuration 

    @property
    def authentication_token_endpoint_uri(self):
        """ platform authentication token endpoint uri """
        return self._session_configuration_file_handler.authentication_token_endpoint_uri

    ############################################################
    #   multi-websockets support

    def _get_stream_status(self, streaming_connection_name: str):
        """ this method is designed for getting a status of given streaming connection.

        Parameters
        ----------
            a connection string of stream
        Returns
        -------
        enum
            status of stream service.
        """
        assert streaming_connection_name in self._streaming_connection_name_to_status
        return self._streaming_connection_name_to_status[streaming_connection_name]

    def _set_stream_status(self, streaming_connection_name: str, stream_status):
        """ set status of given streaming connection

        Parameters
        ----------
        string
            a connection string of stream
        enum
            a status enum of stream
        Returns
        -------
        """
        self._streaming_connection_name_to_status[streaming_connection_name] = stream_status

    async def _get_stream_connection_configuration(self, stream_connection_name: str):
        """ this method is designed to retrieve the stream connection configuration.
        in the platform session two possible configurations including RDP platform or deployed platform.

        Parameters
        ----------
        string
            a connection string of stream
        Returns
        -------
        obj
            a stream connection configuration object
        """

        #   build a stream config
        stream_config = await self._session_configuration_file_handler.get_streaming_connection_configuration(
            stream_connection_name,
            override_connection_config_dict=self._deployed_platform_connection_dict,
            dacs_application_id=self._dacs_params.dacs_application_id,
            dacs_position=self._dacs_params.dacs_position,
            dacs_username=self._dacs_params.deployed_platform_username,
        )

        #   done
        return stream_config

    async def _create_and_start_stream_connection(self, stream_connection_name: str):
        """ this method is designed to construct the stream connection from given stream service
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
        assert stream_connection_name not in self._stream_connection_name_to_stream_connection_dict

        #   get the stream config by given stream service
        stream_config = await self._get_stream_connection_configuration(stream_connection_name)

        #   set the stream connection class by type
        if stream_config.protocol == 'OMM':
            #   construct the Pricing stream connection
            #   construct the websocket thread name
            websocket_thread_name = f'WebSocket {self.session_id} - OMM Protocol - {stream_connection_name}'

            #   set the stream connection class to be OMM
            StreamConnectionCls = OMMStreamConnection
        elif stream_config.protocol == 'RDP':
             #   construct the websocket thread name
            websocket_thread_name = f'WebSocket {self.session_id} - RDP Protocol - {stream_connection_name}'

            #   set the stream connection class to be RDP
            StreamConnectionCls = RDPStreamConnection
        else:
            #   unknown streaming service, raise the exception
            raise PlatformSession(
                f'ERROR!!! Cannot create the stream connection because '
                f'"{stream_connection_name}" has a unknown streaming connection protocol "{stream_config.protocol}"')

        assert StreamConnectionCls and websocket_thread_name
        #   create the stream OMM connection for pricing
        stream_connection = StreamConnectionCls(websocket_thread_name, self, stream_connection_name, stream_config)

        #   store stream connection
        self._stream_connection_name_to_stream_connection_dict[stream_connection_name] = stream_connection

        #   done
        return stream_connection

    #################################################
    #   OMM login message for each kind of session ie. desktop, platform or deployed platform

    def get_omm_login_message_key_data(self):
        """ Return the login message for omm 'key' """
        #   check login to platform or deployed platform
        if self._connection_type == self.PlatformConnectionType.RefinitivDataplatformConectionOnly:
            #   connect streaming to platform
            return {
                "NameType": "AuthnToken",
                "Elements": {
                    "AuthenticationToken": self._access_token,
                    "ApplicationId": self._dacs_params.dacs_application_id,
                    "Position": self._dacs_params.dacs_position
                }
            }
        elif self._connection_type == self.PlatformConnectionType.DeployedPlatformOnly \
                or self._connection_type == self.PlatformConnectionType.RefinitivDataplatformConectionAndDeployedPlatform:
            #   connect streaming to deployed platform
            # HACK TRADING TEAM #####################
            return {
                "Name": self._dacs_params.deployed_platform_username,
                # "NameType": "AuthnToken",
                "Elements": {
                    # "AuthenticationToken": self._access_token,
                    "ApplicationId": self._dacs_params.dacs_application_id,
                    "Position": self._dacs_params.dacs_position
                }
            }
        else:
            #   unknown connection type
            raise PlatformSession('ERROR!!! Unknown connection type {}.'.format(self._connection_type))

    #######################################
    #  methods to open and close session  #
    #######################################

    def close(self):
        """ Close all connection from both Refinitiv Data Platform and Deployed Platform (TREP) """
        #   close the RDP connection
        if self._connection_type == self.PlatformConnectionType.RefinitivDataplatformConectionOnly \
                or self._connection_type == self.PlatformConnectionType.RefinitivDataplatformConectionAndDeployedPlatform:
            #   close the connection to Refinitiv Data Platform

            self.log(logging.DEBUG, "Close platform session...")
            self._auth_manager.close()
            return super().close()

        #   close the deployed platform
        if self._connection_type == self.PlatformConnectionType.DeployedPlatformOnly \
                and self._connection_type == self.PlatformConnectionType.RefinitivDataplatformConectionAndDeployedPlatform:
            #   close the connection to deployed platform
            pass

    ############################################
    #  methods to open asynchronously session  #
    ############################################
    async def open_async(self):

        def open_state():
            self._state = Session.State.Open
            self._on_state(self._state, "Session is opened.")

        if self._state in [Session.State.Pending, Session.State.Open]:
            # session is already opened or is opening
            return self._state

        #   do the authentication process based on the connection type
        if self._connection_type == self.PlatformConnectionType.RefinitivDataplatformConectionOnly \
                or self._connection_type == self.PlatformConnectionType.RefinitivDataplatformConectionAndDeployedPlatform:
            #   open the connection to Refinitiv Data Platform (RDP)

            #   do authentication process with Refinitiv Data Platform (RDP)
            try:
                await self._auth_manager.authorize() and open_state()
            except Exception as e:
                failed_msg = f"EDP Authentication failed. {str(e)}"
                self.warning(failed_msg)
                # ReportSessionStatus(this, SessionStatus.AuthenticationFailed, DefineExceptionObj(e))
                self._state = Session.State.Closed
                self._status = Session.EventCode.SessionAuthenticationFailed
                self._on_state(self._state, failed_msg)
                self._on_event(self._status, failed_msg)

            self.debug(f'RDP connection state = {self._state}.')

        #   call parent call open_async
        await super(PlatformSession, self).open_async()

        #   waiting for everything ready
        if self._connection_type == self.PlatformConnectionType.DeployedPlatformOnly \
                or self._connection_type == self.PlatformConnectionType.RefinitivDataplatformConectionAndDeployedPlatform:
            self.debug('waiting for deployed platform streaming ready.')

            #   do waiting for deployed platform session
            await self.wait_for_streaming(self._deployed_platform_connection_name) and open_state()

        #   done, return state
        return self._state

    ############################
    # methods for HTTP request #
    ############################
    async def http_request_async(self, url: str, method=None, headers=None,
                                 data=None, params=None, json=None, closure=None,
                                 auth=None, loop=None, **kwargs):

        #   check the connection is not a deployed platform only
        if self._connection_type == self.PlatformConnectionType.DeployedPlatformOnly:
            #   it is a deployed platform only, not access right to the refinitiv dataplatform
            raise PlatformSessionError(-1,
                                       'Error!!! Platform session cannot connect to refinitiv dataplatform. '
                                       'Please check or provide the access right.')

        if headers is None:
            headers = {}

        #   call the parent class to request a http request to refinitiv data platform
        return await Session.http_request_async(self, url, method=method, headers=headers,
                                                data=data, params=params, json=json, closure=closure,
                                                auth=auth, loop=loop, **kwargs)

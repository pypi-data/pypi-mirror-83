# coding: utf-8

###############################################################
#
#   STANDARD IMPORTS
#

import urllib.parse

###############################################################
#
#   REFINITIV IMPORTS
#

from refinitiv.dataplatform.errors import EnvError

###############################################################
#
#   LOCAL IMPORTS
#

from .streaming_connection_configuration import StreamingConnectionConfiguration


###############################################################
#
#   CLASS DEFINITIONS
#


class SessionConfigurationFileHandler(object):
    """ This class is designed for handle the session config file.
        It's including the platform authentication endpoint, service discovery endpoint for stream connection
            and ads websocket configuration from config file.
    """

    def __init__(self, session):
        self._session = session
        self._config = self._session._env

        #   session configuration url and path
        self._platform_url = None

        #   list of all possible streaming connection from config file
        self._streaming_connection_names = None

        #   mapping between streaming connection name to the configuration
        #       the configuration depends on the type. There are two types of streaming connection.
        #   including 'service-discovery' and 'ads-websocket'
        self._streaming_connection_name_to_configuration = {}

        #   do initialize the platform url and authentication
        self._initialize_platform_url()
        self._initialize_platform_authentication_endpoint()

    @property
    def authentication_token_endpoint_uri(self):
        assert self._platform_url is not None
        assert self._token_endpoint_uri is not None
        return self._token_endpoint_uri

    @property
    def streaming_connection_names(self):
        return self._config.get_keys('streaming.connections')

    def _initialize_platform_url(self):
        """ do initialize platform url from configuration file """

        #   get the platform url possible prod (https://api.refinitiv.com) or beta (https://api.ppe.refinitiv.com)
        self._config.raise_if_not_available('platform-url')
        self._platform_url = self._config.get_url('platform-url')

    def _initialize_platform_authentication_endpoint(self):
        """ do initialize platform authentication endpoint from configuration file """

        #   get the authentication endpoints
        self._config.raise_if_not_available('auth')

        #       base url
        self._config.raise_if_not_available('auth.base-url')
        base_auth_path = self._config.get_url('auth.base-url')

        #       token endpoint
        self._config.raise_if_not_available('auth.token')
        token_resource = self._config.get_url('auth.token')

        #   build the refresh token based on the configuration file
        token_endpoint = urllib.parse.urljoin(base_auth_path, token_resource)
        self._token_endpoint_uri = urllib.parse.urljoin(self._platform_url, token_endpoint)

    def _initialize_stream_connection_names(self):
        """ do initialize streaming connections from configuration file. """

        #   list all streaming connection names
        self._streaming_connection_names = self._config.get_keys('streaming.connections')

    async def get_streaming_connection_configuration(self, name: str,
                                                     override_connection_config_dict: dict = None,
                                                     **kwargs):
        """ get a streaming connection configuration based on given connection name.
        note that it will initialize the streaming connection configuration if it doesn't exists.
            the initialized process may include the request to service discovery endpoint based on type of streaming connection.
        it might raise an error if the connection name doesn't exists in the configuration file.
        """

        #   check the streaming connection configuration exists or not?
        if name in self._streaming_connection_name_to_configuration:
            #   this given connection name already, so use it
            return self._streaming_connection_name_to_configuration[name]

        #   rebuild the streaming connection name from config file
        self._initialize_stream_connection_names()

        #   check the given configuration exists in the config file or not?
        if name not in self._streaming_connection_names:
            #   raise configuration environment error, unknown connection name
            raise EnvError(-1, f'ERROR!!! unknown streaming connection name {name} in config file.')

        #   do a rebuild the configuration based on connection type
        connection_config_dict = self._config.get_dict('streaming.connections')
        #   check and override if it necessary
        if override_connection_config_dict is not None:
            #   do override connection dict
            connection_config_dict.update(override_connection_config_dict)

        #   do build the streaming connection config
        streaming_connection_config = await StreamingConnectionConfiguration.build_streaming_connection_configuration(
            self._session,
            name,
            self._platform_url,
            connection_config_dict,
            **kwargs)
        #   store in the mapping dictionary
        self._streaming_connection_name_to_configuration[name] = streaming_connection_config

        #   done
        return streaming_connection_config

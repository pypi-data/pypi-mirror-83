# coding: utf-8

###############################################################
#
#   STANDARD IMPORTS
#

import abc
import collections


###############################################################
#
#   REFINITIV IMPORTS
#

###############################################################
#
#   LOCAL IMPORTS
#


###############################################################
#
#   CLASSE DEFINITIONS
#

class ServiceDiscoveryInformation(abc.ABC):
    """ this class is designed to store the service endpoint information that retrieved from discovery endpoint """

    #  EndpointInformation class is designed to store a single service endpoint information
    EndpointInformation = collections.namedtuple('EndpointInformation',
                                                 ['data_format_list',
                                                  'endpoint',
                                                  'location_list',
                                                  'port',
                                                  'provider',
                                                  'transport']
                                                 )

    def __init__(self, name: str, discovery_endpoint_response_json: dict):
        #   name of the connection
        self._name = name
        self._endpoint_service_list = None

        #   initialize endpoint service list
        self._initialize(discovery_endpoint_response_json)

    @property
    @abc.abstractmethod
    def DiscoveryEndpointResponseKeyName(self):
        pass

    @property
    def websocket_authority_list(self):
        return None if len(self._endpoint_service_list) == 0 \
            else ['{}:{}'.format(endpoint_service.endpoint, endpoint_service.port)
                  for endpoint_service in self._endpoint_service_list
                  if endpoint_service.transport == 'websocket'
                  and 'tr_json2' in endpoint_service.data_format_list]

    # def get_websocket_authority_list(self, location_list, data_format):
    #     endpoint_services = None if len(self._endpoint_service_list) == 0 \
    #                             else [ '{}:{}'.format(endpoint_service.endpoint, endpoint_service.port) \
    #                                         for endpoint_service in self._endpoint_service_list\
    #                                                 if endpoint_service.transport == 'websocket'\
    #                                                     and data_format in endpoint_service.data_format_list ]
    #     assert endpoint_services is not None

    #     #   not specific locations
    #     if len(location_list) == 0:
    #         return endpoint_services

    #     #   determine websocket authority
    #     websocket_authority_list = None
    #     if location_list is not None:
    #     #   valid location
    #         #   loop over all given location for determine websocket authority
    #         websocket_authority_list = []
    #         for location in location_list:
    #             #   get the websocket authority
    #             this_location_websocket_authority_list = self._get_websocket_authority_list_by_location(endpoint_services, location)
    #             #   check for valid location
    #             if this_location_websocket_authority_list is None:
    #             #   no valid location
    #                 raise ValueError('ERROR!!! region \'{}\' is not valid for the {} streaming connection of it service
    # discovery'.format(
    #                                         location, self._name))
    #             websocket_authority_list.extend(this_location_websocket_authority_list)
    #     else:
    #     #   location is not specific
    #         websocket_authority_list = self._get_websocket_authority_list_by_location(endpoint_services)

    #     #   done
    #     return websocket_authority_list

    def get_websocket_authority_list_by_location(self, location_list=None, data_format=None):
        """ get a websocket authority by specific prefer location """
        assert (self._endpoint_service_list is not None)
        assert (len(self._endpoint_service_list) > 0)

        #   filter only websocket and tr2_json endpoint services
        endpoint_services = [endpoint_service
                             for endpoint_service in self._endpoint_service_list
                             if endpoint_service.transport == 'websocket'
                             and data_format in endpoint_service.data_format_list]

        #   skip filter location
        if location_list is None or len(location_list) == 0:
            #   do not filter
            return [f'{endpoint_service.endpoint}:{endpoint_service.port}' for endpoint_service in endpoint_services]

        #   determine websocket authority
        websocket_authority_list = None
        if location_list is not None:
            #   valid location
            #   loop over all given location for determine websocket authority
            websocket_authority_list = []
            for location in location_list:
                #   get the websocket authority
                this_location_websocket_authority_list = self._get_websocket_authority_list_by_location(endpoint_services, location)
                #   check for valid location
                if this_location_websocket_authority_list is None:
                    #   no valid location
                    raise ValueError(f'ERROR!!! region \'{location}\' is not valid '
                                     f'for the {self._name} streaming connection of it service discovery')
                websocket_authority_list.extend(this_location_websocket_authority_list)
        else:
            #   location is not specific
            websocket_authority_list = self._get_websocket_authority_list_by_location(endpoint_services)

        #   done
        return websocket_authority_list

    @staticmethod
    def _get_websocket_authority_list_by_location(endpoint_services, location=None):
        """ get a endpoint service by location
                return None if no matched location in the endpoint services
        """

        #   search for location
        websocket_authority_to_num_availability_zones = {}
        for endpoint_service in endpoint_services:
            #   check with the prefer location
            if len(endpoint_service.location_list) == 1 \
                        and location in endpoint_service.location_list:
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
        """ initialize the endpoint service from discovery endpoint response """

        #   extract each endpoint service
        assert (self.DiscoveryEndpointResponseKeyName in discovery_endpoint_response_json)
        services = discovery_endpoint_response_json[self.DiscoveryEndpointResponseKeyName]

        #   reset the endpoint service list
        self._endpoint_service_list = []

        #   construct each endpoint service object
        for service in services:
            #   extract service information
            #       data format
            assert ('dataFormat' in service)
            data_format_list = service['dataFormat']
            #       endpoint
            assert ('endpoint' in service)
            endpoint = service['endpoint']
            #       location list
            assert ('location' in service)
            location_list = service['location']
            #       port
            assert ('port' in service)
            port = service['port']
            #       provider
            assert ('provider' in service)
            provider = service['provider']
            #       transport
            assert ('transport' in service)
            transport = service['transport']

            #   construct endpoint service
            endpoint_service = self.EndpointInformation(data_format_list, endpoint, location_list,
                                                        port, provider, transport)
            #   append to a endpoint service list
            self._endpoint_service_list.append(endpoint_service)


class ServiceDiscoveryBeta1Information(ServiceDiscoveryInformation):
    """ this class is designed for handle the trading's service endpoint information """

    #   discovery endpoint response
    DiscoveryEndpointResponseKeyName = 'service'

    def __init__(self, name: str, discovery_endpoint_response_json: dict):
        ServiceDiscoveryInformation.__init__(self, name, discovery_endpoint_response_json)


class ServiceDiscoveryV1Information(ServiceDiscoveryInformation):
    """ this class is designed for handle the trading's service endpoint information """

    #   discovery endpoint response
    DiscoveryEndpointResponseKeyName = 'services'

    def __init__(self, name: str, discovery_endpoint_response_json: dict):
        ServiceDiscoveryInformation.__init__(self, name, discovery_endpoint_response_json)

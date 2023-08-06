# coding: utf-8

###############################################################
#
#   STANDARD IMPORTS
#

from enum import Enum, unique


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
#   CLASS DEFINITIONS
#

@unique
class StreamService(Enum):
    """ This class is designed to distinguish stream connection by their service type.

    ie. Pricing, Trading, Analytic, etc.

    The session map each stream service to the corresponding websocket
    """
    Pricing = 1
    Trading = 2

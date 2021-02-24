"""
Testing script for the engines component.
"""
# Standard library imports 

# Local imports 
from ..suites import TestSuite
from Src.Components.engines import WatsonCore
from Src.Components.io import IO 
from Src.Components.network import Network
# Third party imports 

############################### GLOBALS #####################################
API_KEY = "MSgOPTS9CvbADe49nEg4wm8_gxeRuf4FGUmlHS9QqAw3"

########################## TEST DEFINITIONS ##################################

#### WatsonCore tests

def watson_core_set_api_key_valid() -> bool:
    watson_core = WatsonCore(Network())
    return watson_core.set_api_key(API_KEY)

def watson_core_set_api_key_invalid() -> bool:
    watson_core = WatsonCore(Network())
    return not watson_core.set_api_key("invalid")

# def watson_core


####################### TEST SUITE DEFINITION ################################

def define_engines_test_suite() -> TestSuite:
    suite = TestSuite()
    suite.add_test("watson_core_set_api_key_valid", (), True, True, 
        watson_core_set_api_key_valid)
    suite.add_test("watson_core_set_api_key_invalid", (), True, True, 
        watson_core_set_api_key_invalid)
    return suite 






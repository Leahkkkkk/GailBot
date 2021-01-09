"""
Testing script for the config component.
"""
# Standard library imports

# Local imports 
from Src.Components.config.blackboard import BlackBoard, BlackBoardAttributes
from ..suites import TestSuite, TestSuiteAttributes

############################### GLOBALS #####################################

########################## TEST DEFINITIONS ##################################

def blackboard_set() -> bool:
    blackboard = BlackBoard()
    is_successful = blackboard.set("Dummy key", None)
    return is_successful == False 

####################### TEST SUITE DEFINITION ################################

def define_config_test_suite() -> TestSuite:
    config_test_suite = TestSuite()
    config_test_suite.add_test(
        "blackboard_set", (),True,True,blackboard_set)
    return config_test_suite

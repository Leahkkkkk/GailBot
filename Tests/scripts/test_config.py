"""
Testing script for the config component.
"""
# Standard library imports
from typing import Dict
# Local imports 
from Src.Components.config import BlackBoard, SystemBBAttributes, Config
from ..suites import TestSuite, TestSuiteAttributes
# Third party imports 
import json

############################### GLOBALS #####################################
VALID_CONFIG_FILE_PATH = "/Users/muhammadumair/Documents/Repositories/mumair01-Repos/GailBot-0.3/Test_files/Others/sample_config.json"
INVALID_CONFIG_FILE_PATH = "/Users/muhammadumair/Documents/Repositories/mumair01-Repos/GailBot-0.3/Test_files/Others/invalid_sample_config.json"

############################## HELPER FUNCTIONS ############################

def load_json_file(file_path : str) -> Dict:
    """
    Load a json file.

    Args:
        file_path (str): Path to the json file.
    
    Returns:
        (Dict): Data loaded from the json file.
    """
    with open(file_path) as f:
        return json.load(f)

########################## TEST DEFINITIONS ##################################


#### CONFIG TESTS 

def config_load_blackboard() -> bool:
    """
    Tests the load_blackboard method in Config.
    
    Tests:
        1. Load blackboard of defined type from valid data
        2. Load blackboard of defined type with invalid data.
        3. Load blackboard of undefined type.

    Returns:
        (bool): True if all the tests pass. False otherwise.
    """
    config = Config()
    data = load_json_file(VALID_CONFIG_FILE_PATH)
    return config.load_blackboard("system_blackboard", data)  and \
        not config.load_blackboard("system_blackboard",{}) and \
        not config.load_blackboard("invalid",data)

def config_get_blackboard() -> bool:
    """
    Tests the get_blackboard method in config

    Tests:
        1. Obtain the blackboard after loading correctly.
        2. Obtain a blackboard that has not been loaded 
        3. Obtain blackboard of undefined type.

    Returns:
        (bool): True if all the tests pass. False otherwise.
    """
    config = Config()
    data = load_json_file(VALID_CONFIG_FILE_PATH)
    return not config.get_blackboard("system_blackboard")[0] and \
        config.load_blackboard("system_blackboard", data) and \
        config.get_blackboard("system_blackboard")[0] and \
        not config.get_blackboard("invalid")[0]
 

def config_get_blackboard_types() -> bool:
    """
    Tests the get_blackboard_types method in config

    Tests:
        1. Obtain the list and verify that it is correct.

    Returns:
        (bool): True if all the tests pass. False otherwise.
    """
    config = Config()
    return config.get_blackboard_types() == ("system_blackboard",)


#### BLACKBOARD TESTS

def blackboard_get() -> bool:
    """
    Tests the get method of a blackboard.

    Tests:
        1. Get an attribute that exists.
        2. Get an attribute that does not exist

    Returns:
        (bool): True if all the tests pass. False otherwise.
    """
    config = Config()
    data = load_json_file(VALID_CONFIG_FILE_PATH)
    config.load_blackboard("system_blackboard", data)
    _, blackboard = config.get_blackboard("system_blackboard")
    return blackboard.get(SystemBBAttributes.Test_key)[1] == "I am a test string" and \
        not blackboard.get("invalid")[0]

def blackboard_set() -> bool:
    """
    Test the set method of of a blackboard

    Tests:
        1. Set an attribute that exists.
        2. Set an attribute that does not exist

    Returns:
        (bool): True if all the tests pass. False otherwise.
    """
    config = Config()
    data = load_json_file(VALID_CONFIG_FILE_PATH)
    config.load_blackboard("system_blackboard", data)
    _, blackboard = config.get_blackboard("system_blackboard")
    return blackboard.get(SystemBBAttributes.Test_key)[1] == "I am a test string" and \
        blackboard.set(SystemBBAttributes.Test_key,"Test_key") and \
        blackboard.get(SystemBBAttributes.Test_key)[1] == "Test_key" and \
        not blackboard.set("invalid","apple")
    
# ####################### TEST SUITE DEFINITION ################################

def define_config_test_suite() -> TestSuite:
    config_test_suite = TestSuite()
    config_test_suite.add_test(
        "config_load_blackboard",(), True, True, config_load_blackboard)
    config_test_suite.add_test(
        "config_get_blackboard",(), True, True, config_get_blackboard)
    config_test_suite.add_test("config_get_blackboard_types",(), True, True, 
        config_get_blackboard_types)
    config_test_suite.add_test("blackboard_get",(), True, True, 
        blackboard_get)
    config_test_suite.add_test("blackboard_set",(), True, True, 
        blackboard_set)
    return config_test_suite

"""
Testing script for the config component.
"""
# Standard library imports

# Local imports 
from Src.Components.config import BlackBoard, BlackBoardAttributes, Config
from ..suites import TestSuite, TestSuiteAttributes

############################### GLOBALS #####################################
VALID_CONFIG_FILE_PATH = "Tests/Test_files/Others/sample_config.json"
INVALID_CONFIG_FILE_PATH = "Tests/Test_files/Others/invalid_sample_config.json"
INVALID_JSON_FILE_PATH = "Tests/Test_files/Others/invalid_json.json"
TEXTFILE_FILE_PATH = "Tests/Test_files/Others/textfile.txt"
INVALID_DUPLICATE_FILE_PATH = "Tests/Test_files/Others/duplicate_key.json"
EXTRA_KEYS_JSON_FILE_PATH = "Tests/Test_files/Others/extra_keys.json"
########################## TEST DEFINITIONS ##################################


#### BLACKBOARD TESTS

def blackboard_set() -> bool:
    """
    Tests the set function in blackboard. 

    Tests:
        1. Add a key-value pair where key is not in BlackBoardAttributes.
        2. Add a key-value pair where key is in BlackBoardAttributes.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    blackboard = BlackBoard()
    return not blackboard.set("Dummy key", None) and \
            blackboard.set(BlackBoardAttributes.Test_key, "Test String")

def blackboard_get() -> bool:
    """
    Tests get function in BlackBoard 

    Tests:
        1. Retrieve a key that does not exist in the blackboard but is in 
            BlackBoardAttributes.
        2. Retrieve a key that does exist in the blackboard and is in 
            BlackBoardAttributes.  
        3. Retrieve using a key that does not exist in BlackBoardAttributes.
    
    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    blackboard = BlackBoard()
    return blackboard.get(BlackBoardAttributes.Test_key) == None and \
        (blackboard.set(BlackBoardAttributes.Test_key,"Test") and \
        blackboard.get(BlackBoardAttributes.Test_key) == "Test") and \
        not blackboard.get("Dummy key")

#### CONFIG TESTS

def config_load_from_file() -> bool:
    """
    Tests the load from file function in config.

    Tests:
        1. Load a file that does not exist and the format is valid.
        2. Load a file that does not exist and the format is not valid.
        3. Load a file that does exist and the format is valid and the 
            config file keys are also valid.
        4. Load a file that does exist and the format is not valid. 
        5. Load a file that does exist and the format is valid but the config 
            keys are invalid.
        6. Load a file that does exist and the format is valid, but the 
            text in the file is not in the expected format.
        7. Load a file that does exist but the format arg and the actual 
            type of file do not match
        8. Load a file that does exist, format is valid, and there are extra
           keys
        9. Load a file that does exist and format is valid, but there are
            duplicate keys
    
    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    config = Config()
    return not config.load_from_file("Dummy", "JSON") and \
        not config.load_from_file("Dummy", "YAML") and \
        config.load_from_file(VALID_CONFIG_FILE_PATH,"JSON") and \
        not config.load_from_file(VALID_CONFIG_FILE_PATH,"YAML") and \
        not config.load_from_file(INVALID_CONFIG_FILE_PATH, "JSON") and \
        not config.load_from_file(INVALID_JSON_FILE_PATH, "JSON") and \
        not config.load_from_file(TEXTFILE_FILE_PATH, "JSON") and \
        config.load_from_file(EXTRA_KEYS_JSON_FILE_PATH, "JSON") and \
        not config.load_from_file(INVALID_DUPLICATE_FILE_PATH, "JSON")

def config_get_blackboard() -> bool:
    """
    Tests the get_blackboard function in config 

    Tests:
        1. Get blackboard without loading file.
        2. Get blackboard after loading file.
        3. Check to make sure that the same attribute from both blackboard is 
            not the same.
        4. Check to make sure that the attribute in the initialized blackboard 
            is set correctly
        5. Check to make sure that config.get_blackboard() reflects changes
    """
    config = Config()  
    uninitialized_blackboard =  config.get_blackboard()
    config.load_from_file(VALID_CONFIG_FILE_PATH,"JSON")
    initialized_blackboard = config.get_blackboard()
    return uninitialized_blackboard.get(BlackBoardAttributes.Test_key) != \
            initialized_blackboard.get(BlackBoardAttributes.Test_key) and \
           initialized_blackboard.get(BlackBoardAttributes.Test_key) == \
            "I am a test string" and \
           config.get_blackboard().get(BlackBoardAttributes.Test_key) == \
            "I am a test string"

def config_blackboard_deepcopy() -> bool:
    """
    Tests that get_blackboard return is a deep copy

    Tests:
        1. Get blackboard without loading file.
        2. Set blackboard attribute
        3. Check to make sure that the config.get_blackboard() does not reflect
            changes
    """

    config = Config()
    blackboard = config.get_blackboard()
    blackboard.set(BlackBoardAttributes.Test_key, "Hello!")
    return blackboard.get(BlackBoardAttributes.Test_key) == "Hello!" and \
           config.get_blackboard().get(BlackBoardAttributes.Test_key) != \
            "Hello!"

####################### TEST SUITE DEFINITION ################################

def define_config_test_suite() -> TestSuite:
    config_test_suite = TestSuite()
    # Blackboard tests 
    config_test_suite.add_test(
        "blackboard_set", (),True,True,blackboard_set)
    config_test_suite.add_test(
        "blackboard_get", (), True, True, blackboard_get)
    # Config tests 
    config_test_suite.add_test(
        "config_load_from_file",(), True, True, config_load_from_file)
    config_test_suite.add_test(
        "config_get_blackboard",(), True, True, config_get_blackboard)
    config_test_suite.add_test(
        "config_blackboard_deepcopy",(), True, True, config_blackboard_deepcopy)
    return config_test_suite

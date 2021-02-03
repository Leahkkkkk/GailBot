
# Local imports 
from Src.Components.config import BlackBoard, SystemBB, SystemBBAttributes, Config
from ..suites import TestSuite, TestSuiteAttributes

########################## TEST DEFINITIONS ##################################
#TODO: Define more blackboards to test with more complex data.

#### BLACKBOARD TESTS

def blackboard_is_configured_true() -> bool:
    """
    Tests blackboard configure with good data.

    Tests:
        1. Load valid data into SystemBB.
        2. Confirm board is configured.
    
    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    blackboard_data = { "Test_key" : "I am a test string"}
    blackboard = SystemBB(blackboard_data)
    return blackboard.is_configured()

def blackboard_is_configured_false() -> bool:
    """
    Tests blackboard configure with bad data.

    Tests: 
        1. Load invalid dictionary data into SystemBB.
        2. Confirm board is not configured.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    blackboard_data = { "Not_a_key" : "I am a test string"}
    blackboard = SystemBB(blackboard_data)
    return not blackboard.is_configured()

def blackboard_no_configure_with_bad_data() -> bool:
    """
    Tests blackboard configure with bad data.

    Tests: 
        1. Load invalid non-dictionary data into SystemBB.
        2. Confirm board is not configured.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """

    blackboard_data = {"This is bad data"}
    blackboard = SystemBB(blackboard_data)
    return not blackboard.is_configured()

def blackboard_set_invalid_key() -> bool:
    """
    Tests set function of invalid key in blackboard.

    Tests:
        1. Load valid data into SystemBB.
        2. Set a key-value pair where key is not in SystemBBAttributes.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """

    blackboard_data = { "Test_key" : "I am a test string"}
    blackboard = SystemBB(blackboard_data)
    return not blackboard.set("Dummy key", None)

def blackboard_set_valid_key() -> bool:
    """
    Tests set function of valid key in blackboard.

    Tests:
        1. Load valid data into SystemBB.
        2. Set a key-value pair where key is in SystemBBAttributes.

    Results:
        (bool): True if all the tests pass. False otherwise.
    """
    blackboard_data = { "Test_key" : "I am a test string"}
    blackboard = SystemBB(blackboard_data)
    return blackboard.set(SystemBBAttributes.Test_key, "Test")

def blackboard_get_configured_key() -> bool: #TODO: fix this!
    """
    Test get function with a valid unset key from SystemBBAttributes.

    Tests:
        1. Load data into SystemBB.
        2. Get attribute that was loaded into the blackboard.
    
    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    blackboard_data = {"Test_key" : "I am a test string"}
    blackboard = SystemBB(blackboard_data)
    return blackboard.get(SystemBBAttributes.Test_key) == (True, "I am a test string")

def blackboard_get_set_key() -> bool:
    """
    Test get function with a valid set key from SystemBBAttributes.

    Tests:
        1. Load data into SystemBB.
        2. Set an attribute that exists in SystemBBAttributes.
        3. Get attribute that was set and confirm that the attribute was 
           set correctly.
    
    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    blackboard_data = {"Test_key" : "I am a test string"}
    blackboard = SystemBB(blackboard_data)
    return (blackboard.set(SystemBBAttributes.Test_key,"Test") and \
        blackboard.get(SystemBBAttributes.Test_key) == (True, "Test"))

def blackboard_get_invalid_key() -> bool:
    """
    Test get function with an invalid key from SystemBBAttributes.

    Tests:
        1. Load data in SystemBB.
        2. Check failture to retrieve using a key that does not exist in 
           SystemBBAttributes.
    
    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    blackboard_data = {"Test_key" : "I am a test string"}
    blackboard = SystemBB(blackboard_data)
    return blackboard.get("Dummy key") == (False, None)

#### CONFIG TESTS

def config_load_into_nonexistent_board() -> bool:
    """
    Tests loading an invalid blackboard type in Config.

    Tests:
        1. Loads data into an undefined blackboard.
        2. Confirms that load was unsucessful.
    
    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    config = Config()
    return not config.load_blackboard("notABoard", {"Key" : "key"})

def config_load_into_existent_board() -> bool:
    """
    Tests sucessful load into a valid blackboard type in Config.

    Tests
        1. Loads valid data into a defined SystemBB.
        2. Confirms that load was sucessful.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    config = Config()
    return config.load_blackboard("system_blackboard", {"Test_key" : "key"})

def config_load_with_bad_data() -> bool:
    """
    Tests unsucessful load with invalid data in a valid blackboard type in 
    Config.

    Tests:
        1. Loads invalid data into SystemBB.
        2. Confirms that load was unsucessful.
    
    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    config = Config()
    return not config.load_blackboard("system_blackboard", {"bad data!"})

def config_load_with_bad_key() -> bool:
    """
    Tests unsuccessful load with invalid key data in a valid blackboard type in 
    Config.

    Tests:
        1. Loads invalid dictionary into SystemBB.
        2. Confirms that load was unsucessful.
    
    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    config = Config()
    return not config.load_blackboard("system_blackboard", {"Bad_key" : "key"})

def config_get_nonexistent_board() -> bool:
    """
    Tests get of invalid blackboard type in Config.

    Tests:
        1. Gets blackboard with invalid type.
        2. Confirms get was unsucessful.
    
    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    config = Config()
    return config.get_blackboard("notABoard") == (False, None)

def config_get_existent_unloaded_board() -> bool:
    """
    Tests get of unloaded valid blackboard type in Config,

    Tests:
        1. Gets unloaded blackboard with valid type.
        2. Confirms get was unsucessful.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    config = Config()
    return config.get_blackboard("system_blackboard") == (False, None)

def config_get_loaded_board() -> bool:
    """
    Tests sucessful get of loaded valid blackboard type in Config.

    Tests: 
        1. Loads valid blackboard data in SystemBB.
        2. Gets SystemBB.
        3. Confirms get was sucessful and the board was set properly.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    config = Config()
    config.load_blackboard("system_blackboard", {"Test_key" : "key"})
    success, system_bb = config.get_blackboard("system_blackboard")
    return success and \
           system_bb.get(SystemBBAttributes.Test_key) == (True, "key")

####################### TEST SUITE DEFINITION ################################

def define_config_test_suite() -> TestSuite:
    config_test_suite = TestSuite()
    # Blackboard tests 
    config_test_suite.add_test(
        "blackboard_is_configured_true", (),True,True,blackboard_is_configured_true)
    config_test_suite.add_test(
        "blackboard_is_configured_false", (),True,True,blackboard_is_configured_false)
    config_test_suite.add_test(
        "blackboard_no_configure_with_bad_data", (),True,True,blackboard_no_configure_with_bad_data)
    config_test_suite.add_test(
        "blackboard_set_invalid_key", (),True,True,blackboard_set_invalid_key)
    config_test_suite.add_test(
        "blackboard_set_valid_key", (),True,True,blackboard_set_valid_key)
    config_test_suite.add_test(
        "blackboard_get_configured_key", (), True, True, 
         blackboard_get_configured_key)
    config_test_suite.add_test(
        "blackboard_get_set_key", (), True, True, 
         blackboard_get_set_key)
    config_test_suite.add_test(
        "blackboard_get_invalid_key", (), True, True, 
         blackboard_get_invalid_key)
    # Config tests 
    config_test_suite.add_test(
        "config_load_into_nonexistent_board", (),True,True,config_load_into_nonexistent_board)
    config_test_suite.add_test(
        "config_load_into_existent_board", (),True,True,config_load_into_existent_board)
    config_test_suite.add_test(
        "config_load_with_bad_data", (),True,True,config_load_with_bad_data)
    config_test_suite.add_test(
        "config_load_with_bad_key", (),True,True,config_load_with_bad_key)
    config_test_suite.add_test(
        "config_get_nonexistent_board", (),True,True,config_get_nonexistent_board)
    config_test_suite.add_test(
        "config_get_existent_unloaded_board", (),True,True,config_get_existent_unloaded_board)
    config_test_suite.add_test(
        "config_get_loaded_board", (),True,True,config_get_loaded_board)
    return config_test_suite


# Local imports
from Src.Components.config import SystemBBAttributes, Config

########################## TEST DEFINITIONS ##################################


def test_config_load_into_nonexistent_board() -> None:
    """
    Tests loading an invalid blackboard type in Config.

    Tests:
        1. Loads data into an undefined blackboard.
        2. Confirms that load was unsucessful.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    config = Config()
    assert not config.load_blackboard("notABoard", {"Key" : "key"})

def test_config_load_into_existent_board() -> None:
    """
    Tests sucessful load into a valid blackboard type in Config.

    Tests
        1. Loads valid data into a defined SystemBB.
        2. Confirms that load was sucessful.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    config = Config()
    assert config.load_blackboard("system_blackboard", {"Test_key" : "key"})

def test_config_load_with_bad_data() -> None:
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
    assert not config.load_blackboard("system_blackboard", {"bad data!"})

def test_config_load_with_bad_key() -> None:
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
    assert not config.load_blackboard("system_blackboard", {"Bad_key" : "key"})

def test_config_get_nonexistent_board() -> None:
    """
    Tests get of invalid blackboard type in Config.

    Tests:
        1. Gets blackboard with invalid type.
        2. Confirms get was unsucessful.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    config = Config()
    assert config.get_blackboard("notABoard") == (False, None)

def test_config_get_existent_unloaded_board() -> None:
    """
    Tests get of unloaded valid blackboard type in Config,

    Tests:
        1. Gets unloaded blackboard with valid type.
        2. Confirms get was unsucessful.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    config = Config()
    assert config.get_blackboard("system_blackboard") == (False, None)

def test_config_get_loaded_board() -> None:
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
    assert success and \
           system_bb.get(SystemBBAttributes.Test_key) == (True, "key")
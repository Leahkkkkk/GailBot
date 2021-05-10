
# Local imports
from Src.Components.config import BlackBoard, SystemBB, SystemBBAttributes

#### BLACKBOARD TESTS

def test_blackboard_is_configured_true() -> None:
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
    assert blackboard.is_configured()

def test_blackboard_is_configured_false() -> None:
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
    assert not blackboard.is_configured()

def test_blackboard_no_configure_with_bad_data() -> None:
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
    assert not blackboard.is_configured()

def test_blackboard_set_invalid_key() -> None:
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
    assert not blackboard.set("Dummy key", None)

def test_blackboard_set_valid_key() -> None:
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
    assert blackboard.set(SystemBBAttributes.Test_key, "Test")

def test_blackboard_get_configured_key() -> None:
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
    assert blackboard.get(SystemBBAttributes.Test_key) ==\
        (True, "I am a test string")

def test_blackboard_get_set_key() -> None:
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
    assert (blackboard.set(SystemBBAttributes.Test_key,"Test") and \
        blackboard.get(SystemBBAttributes.Test_key) == (True, "Test"))

def test_blackboard_get_invalid_key() -> None:
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
    assert blackboard.get("Dummy key") == (False, None)
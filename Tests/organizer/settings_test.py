# Local imports
from Src.Components.organizer import Settings

############################### GLOBALS #####################################

########################## TEST DEFINITIONS #################################

def test_settings_create_valid_data() -> None:
    """
    Tests the settings object.

    Tests:
        1. Create a settings object with valid data and determine if it is
            configured.

    Returns:
        (bool): True if all tests pass. False otherwise
    """
    data = {
        "sample_attribute_1" : 1,
        "sample_attribute_2" : 2
    }
    settings = Settings(data.keys())
    for k,v in data.items():
        settings._set_value(k,v)
    assert settings.is_configured()

def test_settings_create_invalid_data() -> None:
    """
    Tests the settings object.

    Tests:
        1. Create a settings object with invalid data and determine if it is
            configured.

    Returns:
        (bool): True if all tests pass. False otherwise
    """
    data = {
        "sample_attribute_1" : None,
        "sample_attribute_2" : None,
        "bad_attribute_1" : None}
    settings = Settings(data.keys())
    assert settings._set_value("sample_attribute_1",1)
    assert not settings.is_configured()

def test_settings_create_invalid_data_missing_keys() -> None:
    """
    Tests the settings object.

    Test:
        1. Create a settings object with invalid missing keys data and
           confirm it is not configured

    Returns:
        (bool): True if all tests pass. False otherwise
    """
    data = {
        "sample_attribute_1" : None}
    settings = Settings(data.keys())
    assert not settings.is_configured()

def test_settings_create_invalid_data_misnamed_keys() -> None:
    """
    Tests the settings object.

    Test:
        1. Create a settings object with misnamed keys data and
           confirm it is not configured

    Returns:
        (bool): True if all tests pass. False otherwise
    """
    data = {
        "sample_attribute_1" : None,
        "sample_attribute" : None}
    settings = Settings(data.keys())
    assert not settings._set_value("sample_attribute_2", 2)
    assert not settings.is_configured()

# def test_settings_set_attribute_manually() -> None:
#     """
#     Tests the set method for settings.

#     Tests:
#         1. Attempt to set a settings attribute, which should not be possible.

#     Returns:
#         (bool): True if all tests pass. False otherwise.
#     """
#     data = {
#         "sample_attribute_1" : None,
#         "sample_attribute_2" : None}
#     settings = Settings(data)
#     assert not settings.set(SettingsAttributes,None) and \
#           not settings.set("invalid", "1")

def test_settings_get_valid() -> None:
    """
    Tests the get method of Settings

    Tests:
        1. Obtain an valid attribute data

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "sample_attribute_1" : "1",
        "sample_attribute_2" : "2"}
    settings = Settings(data.keys())
    for k,v in data.items():
        settings._set_value(k,v)
    assert settings.is_configured()
    assert settings.get("sample_attribute_1")[0]
    assert settings.get("sample_attribute_1")[1] == "1"
    assert settings.get("sample_attribute_2")[0]
    assert settings.get("sample_attribute_2")[1] == "2"

def test_settings_get_invalid() -> None:
    """
    Tests the get method of Settings

    Tests:
        1. Obtain an invalid attribute data

    Returns:
        (bool): True if all tests pass. False otherwise
    """
    data = {
        "sample_attribute_1" : "1",
        "sample_attribute_2" : "2"}
    settings = Settings(data.keys())
    for k,v in data.items():
        settings._set_value(k,v)
    assert settings.is_configured()
    assert not settings.get("invalid")[0]

# Local imports
from Src.Components.organizer import SettingsBuilder, SettingsAttributes, Settings

############################### GLOBALS #####################################

########################## TEST DEFINITIONS #################################

def test_settings_builder_create_settings_valid() -> None:
    """
    Tests the create_settings method in SettingsBuilder

    Tests:
        1. Passes valid data to the builder.
        2. Check the constructed object for data.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "sample_attribute_1" : "1",
        "sample_attribute_2" : "2"}
    builder = SettingsBuilder()
    success, settings = builder.create_settings(data)
    assert success and \
        type(settings) == Settings and \
        settings.get(SettingsAttributes.sample_attribute_1)[1] == "1" and \
        settings.get(SettingsAttributes.sample_attribute_2)[1] == "2"


def test_settings_builder_create_settings_invalid() -> None:
    """
    Tests the create_settings method in SettingsBuilder

    Tests:
        1. Passes invalid data to the builder

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data_1 = {
        "sample_attribute_1" : "1"}
    data_2 = {
        "sample_attribute_1" : "1",
        "sample_attribute_2" : "2",
        "additional" : "3"}
    builder = SettingsBuilder()
    success_1, settings_1 = builder.create_settings(data_1)
    success_2, settings_2 = builder.create_settings(data_2)
    assert not success_1 and \
        not success_2 and \
        settings_1 == None and \
        settings_2 == None

def test_settings_builder_create_settings_invalid_missing_keys() -> None:
    """
    Tests the create_settings method in SettingsBuilder

    Tests:
        1. Passes invalid missing keys data to the builder

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "sample_attribute_1" : "1"}
    builder = SettingsBuilder()
    success, settings = builder.create_settings(data)
    assert not success and settings == None

def test_settings_builder_create_settings_invalid_extra_keys() -> None:
    """
    Tests the create_settings method in SettingsBuilder

    Tests:
        1. Passes invalid extra keys data to the builder

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "sample_attribute_1" : "1",
        "sample_attribute_2" : "2",
        "additional" : "3"}
    builder = SettingsBuilder()
    success, settings = builder.create_settings(data)
    assert not success and settings == None

def test_settings_builder_create_settings_invalid_misnamed_keys() -> None:
    """
    Tests the create_settings method in SettingsBuilder

    Tests:
        1. Passes invalid misnamed keys data to the builder

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "sample_attribute_1" : "1",
        "sample_attribute" : "2"}
    builder = SettingsBuilder()
    success, settings = builder.create_settings(data)
    assert not success and settings == None

def test_settings_builder_create_settings_invalid_empty() -> None:
    """
    Tests the create_settings method in SettingsBuilder

    Tests:
        1. Passes invalid empty data to the builder

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {}
    builder = SettingsBuilder()
    success, settings = builder.create_settings(data)
    assert not success and settings == None

def test_settings_builder_copy_settings() -> None:
    """
    Tests the copy_settings method in SettingsBuilder

    Tests:
        1. Copy the settings object and check attributes for equality.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "sample_attribute_1" : "1",
        "sample_attribute_2" : "2"}
    builder = SettingsBuilder()
    success, settings = builder.create_settings(data)
    copied_settings = builder.copy_settings(settings)
    assert success and \
        settings != copied_settings and \
        settings.get(SettingsAttributes.sample_attribute_1) == \
            copied_settings.get(SettingsAttributes.sample_attribute_1) and \
        settings.get(SettingsAttributes.sample_attribute_2) == \
            copied_settings.get(SettingsAttributes.sample_attribute_2)

def test_settings_builder_copy_settings_not_configured() -> None:
    """
    Tests the copy_settings method in SettingsBuilder

    Tests:
        1. Copy the settings object after settings is not configured, confirms
           the create does no succeed and the copied settings does not throw
           error

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "sample_attribute_1" : "1"}
    builder = SettingsBuilder()
    success, settings = builder.create_settings(data)
    copied_settings = builder.copy_settings(settings)
    assert not success and \
        copied_settings == None

def test_settings_builder_change_settings_valid() -> None:
    """
    Tests the change_settings method in SettingsBuilder

    Tests:
        1. Change settings of only some attributes.
        2. Chaneg settings of all attributes.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "sample_attribute_1" : "1",
        "sample_attribute_2" : "2"}
    new_data_1 = {
        "sample_attribute_1" : "3"}
    new_data_2 = {
        "sample_attribute_1" : "4",
        "sample_attribute_2" : "5"}
    builder = SettingsBuilder()
    _, settings = builder.create_settings(data)
    copied_1 = builder.copy_settings(settings)
    copied_2 = builder.copy_settings(settings)
    builder.change_settings(copied_1, new_data_1)
    builder.change_settings(copied_2, new_data_2)
    assert copied_1 != copied_2 and \
        copied_1.get(SettingsAttributes.sample_attribute_1)[1] == "3" and \
        copied_1.get(SettingsAttributes.sample_attribute_2)[1] == "2" and \
        copied_2.get(SettingsAttributes.sample_attribute_1)[1] == "4" and \
        copied_2.get(SettingsAttributes.sample_attribute_2)[1] == "5"

def test_settings_builder_change_settings_invalid() -> None:
    """
    Tests the change_settings method in SettingsBuilder

    Tests:
        1. Pass data with all invalid keys
        2. Pass data with some invalid keys.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "sample_attribute_1" : "1",
        "sample_attribute_2" : "2"}
    invalid_data_1 = {
        "sample_attribute_1" : "1",
        "invalid" : None}
    invalid_data_2 = {
        "invalid" : None }
    builder = SettingsBuilder()
    _, settings = builder.create_settings(data)
    assert not builder.change_settings(settings, invalid_data_1) and \
        not builder.change_settings(settings,invalid_data_2) and \
        settings.get(SettingsAttributes.sample_attribute_1)[1] == "1" and \
        settings.get(SettingsAttributes.sample_attribute_2)[1] == "2"

def test_settings_builder_change_settings_empty() -> None:
    """
    Tests the change_settings method in SettingsBuilder

    Tests:
        1. Pass empty data to change settings
        2. Confirm no data is changed

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "sample_attribute_1" : "1",
        "sample_attribute_2" : "2"}
    invalid_data = {}
    builder = SettingsBuilder()
    _, settings = builder.create_settings(data)
    assert builder.change_settings(settings, invalid_data) and \
        settings.get(SettingsAttributes.sample_attribute_1)[1] == "1" and \
        settings.get(SettingsAttributes.sample_attribute_2)[1] == "2"

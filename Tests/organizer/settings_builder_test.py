# Standard library imports
from typing import Dict, Any, Callable
# Local imports
from Src.Components.organizer import SettingsBuilder, Settings, settings
from Tests.organizer.vardefs import *

############################### GLOBALS #####################################

############################### SETUP #######################################


class CustomSettings(Settings):

    ATTRS = ("attr_1", "attr_2")

    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__(attrs=self.ATTRS)
        self._parse_data(data)

    def get_attr_1(self) -> Any:
        return self.get("attr_1")[1]

    def get_attr_2(self) -> Any:
        return self.get("attr_2")[1]

    def _parse_data(self, data: Dict[str, Any]) -> bool:
        if not all([k in data.keys() for k in self.ATTRS]):
            return False
        for k, v in data.items():
            self._set_value(k, v)
        return True


def settings_creator() -> Callable[[], Settings]:
    return lambda data: CustomSettings(data)


def get_valid_data() -> Dict[str, Any]:
    return {
        "attr_1": 1,
        "attr_2": 2
    }


########################## TEST DEFINITIONS #################################

def test_settings_builder_register_setting_type_valid() -> None:
    """
    Tests:
        1. Add a valid settings creator
    """
    builder = SettingsBuilder()
    assert builder.register_setting_type("custom", settings_creator())


def test_settings_builder_register_setting_type_invalid() -> None:
    """
    Tests:
        1. Add a settings creator that has been added before.
    """
    builder = SettingsBuilder()
    assert builder.register_setting_type("custom", settings_creator())
    assert not builder.register_setting_type("custom", settings_creator())


def test_settings_builder_create_settings_valid() -> None:
    """
    Tests the create_settings method in SettingsBuilder

    Tests:
        1. Passes valid data to the builder.
        2. Check the constructed object for data.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    settings_name = "custom"
    builder = SettingsBuilder()
    builder.register_setting_type(settings_name, settings_creator())
    data = get_valid_data()
    success, settings = builder.create_settings(settings_name, data)
    print(success, settings)
    assert success
    assert isinstance(settings, Settings)
    assert settings.get("attr_1")[1] == 1
    assert settings.get("attr_2")[1] == 2


def test_settings_builder_create_settings_invalid() -> None:
    """
    Tests the create_settings method in SettingsBuilder

    Tests:
        1. Passes invalid data to the builder

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data_1 = {
        "attr_1": "1"}
    data_2 = {
        "attr_1": "1",
        "attr_2": "2",
        "additional": "3"}
    settings_name = "custom"
    builder = SettingsBuilder()
    builder.register_setting_type(settings_name, settings_creator())
    success_1, _ = builder.create_settings(settings_name, data_1)
    success_2, _ = builder.create_settings(settings_name, data_2)
    assert not success_1
    assert success_2


def test_settings_builder_create_settings_invalid_missing_keys() -> None:
    """
    Tests the create_settings method in SettingsBuilder

    Tests:
        1. Passes invalid missing keys data to the builder

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "attr_1": "1"}
    builder = SettingsBuilder()
    builder.register_setting_type("custom", settings_creator())
    success, settings = builder.create_settings("custom", data)
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
        "attr_1": "1",
        "attr_2": "2",
        "additional": "3"}
    builder = SettingsBuilder()
    builder.register_setting_type("custom", settings_creator())
    success, settings = builder.create_settings("custom", data)
    assert success and settings != None


def test_settings_builder_create_settings_invalid_misnamed_keys() -> None:
    """
    Tests the create_settings method in SettingsBuilder

    Tests:
        1. Passes invalid misnamed keys data to the builder

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "attr_1": "1",
        "attr": "2"}
    builder = SettingsBuilder()
    builder.register_setting_type("custom", settings_creator())
    success, settings = builder.create_settings("custom", data)
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
    builder.register_setting_type("custom", settings_creator())
    success, settings = builder.create_settings("custom", data)
    assert not success and settings == None


def test_settings_builder_copy_settings() -> None:
    """
    Tests the copy_settings method in SettingsBuilder

    Tests:
        1. Copy the settings object and check attributes for equality.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = get_valid_data()
    builder = SettingsBuilder()
    builder.register_setting_type("custom", settings_creator())
    success, settings = builder.create_settings("custom", data)
    copied_settings = builder.copy_settings(settings)
    assert success and \
        settings != copied_settings and \
        settings.get("attr_1") == \
        copied_settings.get("attr_1") and \
        settings.get("attr_2") == \
        copied_settings.get("attr_2")


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
        "attr_1": "1"}
    builder = SettingsBuilder()
    builder.register_setting_type("custom", settings_creator())
    success, settings = builder.create_settings("custom", data)
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
        "attr_1": "1",
        "attr_2": "2"}
    new_data_1 = {
        "attr_1": "3"}
    new_data_2 = {
        "attr_1": "4",
        "attr_2": "5"}

    builder = SettingsBuilder()
    builder.register_setting_type("custom", settings_creator())
    _, settings = builder.create_settings("custom", data)
    copied_1 = builder.copy_settings(settings)
    copied_2 = builder.copy_settings(settings)
    builder.change_settings(copied_1, new_data_1)
    builder.change_settings(copied_2, new_data_2)
    assert copied_1 != copied_2 and \
        copied_1.get("attr_1")[1] == "3" and \
        copied_1.get("attr_2")[1] == "2" and \
        copied_2.get("attr_1")[1] == "4" and \
        copied_2.get("attr_2")[1] == "5"


def test_settings_builder_change_settings_invalid() -> None:
    """
    Tests the change_settings method in SettingsBuilder

    Tests:
        1. Pass data with all invalid keys
        2. Pass data with some invalid keys.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = get_valid_data()
    invalid_data_1 = {
        "attr_1": "1",
        "invalid": None}
    invalid_data_2 = {
        "attr_3": "2",
        "invalid": None}
    builder = SettingsBuilder()
    builder.register_setting_type("custom", settings_creator())
    _, settings = builder.create_settings("custom", data)
    assert not builder.change_settings(settings, invalid_data_1)
    assert not builder.change_settings(settings, invalid_data_2)
    assert not settings.get("attr_1")[1] == "1"
    assert not settings.get("attr_2")[1] == "2"


def test_settings_builder_change_settings_empty() -> None:
    """
    Tests the change_settings method in SettingsBuilder

    Tests:
        1. Pass empty data to change settings
        2. Confirm no data is changed

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = get_valid_data()
    invalid_data = {}
    builder = SettingsBuilder()
    builder.register_setting_type("custom", settings_creator())
    _, settings = builder.create_settings("custom", data)
    assert builder.change_settings(settings, invalid_data) and \
        settings.get("attr_1")[1] == 1 and \
        settings.get("attr_2")[1] == 2


def test_settings_builder_get_registered_setting_types() -> None:
    """
    Tests:
        1. Make sure there are no registered settings initially.
        2. Make sure name is valid when a settings is registered.
        3. Make sure the type of creator is valid
    """
    builder = SettingsBuilder()
    assert len(builder.get_registered_setting_types().keys()) == 0
    builder.register_setting_type("custom", settings_creator())
    assert "custom" in builder.get_registered_setting_types()
    assert type(builder.get_registered_setting_types()["custom"]) \
        == type(settings_creator())

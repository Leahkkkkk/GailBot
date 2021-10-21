# Standard library imports
from typing import Dict, Any, List
from enum import Enum
from copy import deepcopy
# Local imports
from Src.components.io import IO
from Src.components.organizer import Settings
from Src.components.services import SettingsHook
from Tests.services.vardefs import *

############################### SETUP #####################################
SOURCE_NAME = "source"


def get_settings_data() -> Dict:
    return {
        GBSettingAttrs.engine_type: "watson",
        GBSettingAttrs.watson_api_key: "MSgOPTS9CvbADe49nEg4wm8_gxeRuf4FGUmlHS9QqAw3",
        GBSettingAttrs.watson_language_customization_id: "41e54a38-2175-45f4-ac6a-1c11e42a2d54",
        GBSettingAttrs.watson_base_language_model: "en-US_BroadbandModel",
        GBSettingAttrs.watson_region: "dallas",
        GBSettingAttrs.analysis_plugins_to_apply: ["second_analysis"],
        GBSettingAttrs.output_format: "normal"}


class GBSettingAttrs(Enum):
    engine_type = "engine_type"
    watson_api_key = "watson_api_key"
    watson_language_customization_id = "watson_language_customization_id"
    watson_base_language_model = "watson_base_language_model"
    watson_region = "watson_region"
    output_format = "output_format"
    analysis_plugins_to_apply = "analysis_plugins_to_apply"


class GailBotSettings(Settings):

    def __init__(self, data: Dict[GBSettingAttrs, Any]) -> None:
        self.io = IO()
        self.save_extension = "json"
        self.attrs = list([x for x in GBSettingAttrs])
        self.data = dict()
        self.configured = False
        if not all([attr in data for attr in self.attrs]):
            return
        for attr in self.attrs:
            self.data[attr] = None
        for attr, value in data.items():
            self.set_value(attr, value)
        self.configured = True

    ############################ MODIFIERS ####################################

    def save_to_file(self, save_path: str) -> bool:
        try:
            path_with_extension = "{}.{}".format(
                save_path, self.save_extension)
            data = dict()
            for k, v in self.data.items():
                data[k.value] = v
            return self.io.write(path_with_extension, data, True)
        except Exception as e:
            print(e)
            return False

    ############################ SETTERS ####################################

    def set_value(self, attr: GBSettingAttrs, value: Any) -> bool:
        if self.has_attribute(attr) and \
                self.is_configured():
            self.data[attr] = value
            return True
        return False

    ############################ GETTERS ####################################

    def is_configured(self) -> bool:
        return self.configured

    def has_attribute(self, attr: GBSettingAttrs) -> bool:
        return attr in self.attrs

    def get_value(self, attr: GBSettingAttrs) -> Any:
        if self.has_attribute(attr) and \
                self.is_configured():
            return self.data[attr]

    def get_all_values(self) -> Dict:
        return deepcopy(self.data)


########################## TEST DEFINITIONS ##################################


def test_save() -> None:
    """
    Tests:
        1. Save settings.
    """
    hook = SettingsHook("test", SETTINGS_DIR_PATH)
    assert hook.save(GailBotSettings(get_settings_data()))


def test_load() -> None:
    """
    Tests:
        1. Load without saving.
        2. Load after saving.
    """
    pass


def test_cleanup() -> None:
    """
    Tests:
        1. Cleanup before saving.
        2. Cleanup after saving.
    """
    pass


def test_is_saved() -> None:
    """
    Tests:
        1. Check before saving.
        2. Check after saving.
    """
    pass

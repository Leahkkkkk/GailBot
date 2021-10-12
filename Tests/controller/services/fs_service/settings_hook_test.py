# Standard library imports
from Src.Components.organizer.settings import Settings
from typing import Dict
# Local imports
from Src.Components.io import IO
from Src.Components.controller.services.fs_service.settings_hook import SettingsHook
from Src.Components.controller.services.organizer_service import GailBotSettings, GBSettingAttrs
from Src.utils.observer import Subscriber
from Tests.controller.vardefs import *

############################### GLOBALS #####################################

# SETTINGS_DIR_PATH = "TestData/workspace/temp_ws"
# EMPTY_DIR_PATH = "TestData/workspace/empty_dir_1"
# WAV_FILE_PATH = "TestData/media/overlayed.wav"
# SETTINGS_PROFILE_EXTENSION = "json"

############################### SETUP #####################################


class TestSubscriber(Subscriber):
    def handle(self, event_type: str, data: Dict):
        print(data)


def get_settings_data() -> Dict:
    return {
        GBSettingAttrs.engine_type: "watson",
        GBSettingAttrs.watson_api_key: "MSgOPTS9CvbADe49nEg4wm8_gxeRuf4FGUmlHS9QqAw3",
        GBSettingAttrs.watson_language_customization_id: "41e54a38-2175-45f4-ac6a-1c11e42a2d54",
        GBSettingAttrs.watson_base_language_model: "en-US_BroadbandModel",
        GBSettingAttrs.watson_region: "dallas",
        GBSettingAttrs.analysis_plugins_to_apply: ["second_analysis"],
        GBSettingAttrs.output_format: "normal"}

########################## TEST DEFINITIONS ##################################


def test_save() -> None:
    """
    Tests:
        1. Save a settings.
    """
    hook = SettingsHook("test", SETTINGS_DIR_PATH, SETTINGS_PROFILE_EXTENSION)
    settings = GailBotSettings(get_settings_data())
    hook.save(settings)
    hook.cleanup()


def test_load() -> None:
    """
    Tests:
        1. Load without saving.
        2. Load after saving.
    """
    hook = SettingsHook("test", SETTINGS_DIR_PATH, SETTINGS_PROFILE_EXTENSION)
    settings = GailBotSettings(get_settings_data())
    assert hook.load() == {}
    hook.save(settings)
    assert hook.load() != {}
    hook.cleanup()


def test_cleanup() -> None:
    """
    Tests:
        1. Cleanup before saving.
        2. Cleanup after saving.
    """
    hook = SettingsHook("test", SETTINGS_DIR_PATH, SETTINGS_PROFILE_EXTENSION)
    settings = GailBotSettings(get_settings_data())
    hook.cleanup()
    hook.save(settings)
    hook.cleanup()


def test_register_listener() -> None:
    """
    Tests:
        1. Add a listener of all three types and check if it works.
    """
    hook = SettingsHook("test", SETTINGS_DIR_PATH, SETTINGS_PROFILE_EXTENSION)
    subscriber = TestSubscriber()
    hook.register_listener("save", subscriber)
    hook.register_listener("load", subscriber)
    hook.register_listener("cleanup", subscriber)
    settings = GailBotSettings(get_settings_data())
    hook.save(settings)
    hook.load()
    hook.cleanup()


def test_is_saved() -> None:
    """
    Tests:
        1. Check before saving.
        2. Check after saving.
    """
    hook = SettingsHook("test", SETTINGS_DIR_PATH, SETTINGS_PROFILE_EXTENSION)
    settings = GailBotSettings(get_settings_data())
    assert not hook.is_saved()
    hook.save(settings)
    assert hook.is_saved()
    hook.cleanup()


from typing import Dict
from Src.components.controller import GailBotController, GBSettingAttrs, \
    GailBotSettings
from Src.components.io import IO
from Tests.controller.vardefs import *
import pytest

############################### GLOBALS #####################################


############################### SETUP #####################################

def obtain_settings_profile_data() -> Dict:
    return {
        GBSettingAttrs.engine_type: "watson",
        GBSettingAttrs.watson_api_key: WATSON_API_KEY,
        GBSettingAttrs.watson_language_customization_id: WATSON_LANG_CUSTOM_ID,
        GBSettingAttrs.watson_base_language_model: WATSON_BASE_LANG_MODEL,
        GBSettingAttrs.watson_region: WATSON_REGION,
        GBSettingAttrs.plugins_to_apply: [
            'turn_construct', 'combine_turns', 'overlaps', 'pauses', 'fto', 'gaps']
    }


@pytest.fixture(scope='session', autouse=True)
def reset_workspace() -> None:
    io = IO()
    io.delete(RESULT_DIR_PATH)
    io.create_directory(RESULT_DIR_PATH)


# def test_transcription() -> None:
#     controller = GailBotController(WS_DIR_PATH)
#     assert controller.add_source("audio", MP3_FILE_PATH, RESULT_DIR_PATH)
#     assert controller.create_new_settings_profile(
#         "s1", obtain_settings_profile_data())
#     assert controller.apply_settings_profile_to_source("audio", "s1")
#     controller.transcribe()


def test_plugins() -> None:
    controller = GailBotController(WS_DIR_PATH)
    assert controller.add_source("audio", MP3_FILE_PATH, RESULT_DIR_PATH)
    assert controller.create_new_settings_profile(
        "s1", obtain_settings_profile_data())
    assert controller.apply_settings_profile_to_source("audio", "s1")
    print(controller.register_plugins(DEFAULT_ANALYSIS_PLUGIN_CONFIG))
    controller.transcribe()


def test_retranscription() -> None:
    pass

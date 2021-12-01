# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-10-22 09:07:35
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-11-30 17:46:42

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


def test_transcription_audio_file() -> None:
    controller = GailBotController(WS_DIR_PATH)
    assert controller.add_source("audio", MP3_FILE_PATH, RESULT_DIR_PATH)
    assert controller.create_new_settings_profile(
        "s1", obtain_settings_profile_data())
    assert controller.apply_settings_profile_to_source("audio", "s1")
    controller.register_plugins(DEFAULT_ANALYSIS_PLUGIN_CONFIG)
    controller.transcribe()


def test_transcription_audio_directory() -> None:
    """
    Output stage not working for this currently.
    """
    controller = GailBotController(WS_DIR_PATH)
    assert controller.add_source("audio_dir", MIXED_DIR_PATH, RESULT_DIR_PATH)
    assert controller.create_new_settings_profile(
        "s1", obtain_settings_profile_data())
    assert controller.apply_settings_profile_to_source("audio_dir", "s1")
    controller.register_plugins(DEFAULT_ANALYSIS_PLUGIN_CONFIG)
    controller.transcribe()


def test_transcription_dual_channel_video() -> None:

    controller = GailBotController(WS_DIR_PATH)
    assert controller.add_source(
        "dual_channel_video", MXF_FILE_PATH_SHORT, RESULT_DIR_PATH)
    assert controller.create_new_settings_profile(
        "s1", obtain_settings_profile_data())
    assert controller.apply_settings_profile_to_source(
        "dual_channel_video", "s1")
    controller.register_plugins(DEFAULT_ANALYSIS_PLUGIN_CONFIG)
    controller.transcribe()


def test_plugins() -> None:
    controller = GailBotController(WS_DIR_PATH)
    assert controller.add_source("audio", MP3_FILE_PATH, RESULT_DIR_PATH)
    assert controller.create_new_settings_profile(
        "s1", obtain_settings_profile_data())
    assert controller.apply_settings_profile_to_source("audio", "s1")
    print(controller.register_plugins(DEFAULT_ANALYSIS_PLUGIN_CONFIG))
    controller.transcribe()


def test_retranscription() -> None:
    controller = GailBotController(WS_DIR_PATH)
    assert controller.add_source(
        "prev_mp3_short", PREV_AUDIO_MP3_SHORT, RESULT_DIR_PATH)
    assert controller.create_new_settings_profile(
        "s1", obtain_settings_profile_data())
    assert controller.apply_settings_profile_to_source("prev_mp3_short", "s1")
    print(controller.register_plugins(DEFAULT_ANALYSIS_PLUGIN_CONFIG))
    controller.transcribe()

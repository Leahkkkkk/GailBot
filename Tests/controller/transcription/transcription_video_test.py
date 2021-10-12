'''
Contains tests for only the actual transcription process.
'''
# Standard library imports
import pytest
from typing import Dict
# Local imports
from Src.Components.io import IO
from Src.Components.controller import GailBotController, SettingsDetails,\
    SourceDetails, GBSettingAttrs, PipelineServiceSummary
from Tests.controller.vardefs import *

############################### GLOBALS #####################################

############################### SETUP #####################################


@pytest.fixture(scope='session', autouse=True)
def reset_workspace() -> None:
    io = IO()
    io.delete(RESULT_DIR_PATH)
    io.create_directory(RESULT_DIR_PATH)

########################## TEST DEFINITIONS ##################################

# AUDIO TESTS


def test_transcribe_video_mov_short() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("short_mov", MOV_FILE_PATH_SHORT, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("short_mov", "default")
    controller.transcribe()


def test_transcribe_video_mov_medium() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("medium_mov", MOV_FILE_PATH_MEDIUM, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("medium_mov", "default")
    controller.transcribe()


def test_transcribe_video_mov_long() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("long_mov", MOV_FILE_PATH_LONG, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("long_mov", "default")
    controller.transcribe()


def test_transcribe_video_mxf_short() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("short_mxf", MXF_FILE_PATH_SHORT, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("short_mxf", "default")
    controller.transcribe()


def test_transcribe_video_mxf_medium() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("medium_mxf", MXF_FILE_PATH_MEDIUM, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("medium_mxf", "default")
    controller.transcribe()


def test_transcribe_video_mxf_long() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("long_mxf", MXF_FILE_PATH_LONG, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("long_mxf", "default")
    controller.transcribe()


def test_transcribe_video_wmv_short() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("short_wmv", WMV_FILE_PATH_SHORT, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("short_wmv", "default")
    controller.transcribe()


def test_transcribe_video_wmv_medium() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("medium_wmv", WMV_FILE_PATH_MEDIUM, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("medium_wmv", "default")
    controller.transcribe()


def test_transcribe_video_wmv_long() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("long_wav", WMV_FILE_PATH_LONG, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("long_wmv", "default")
    controller.transcribe()


def test_transcribe_video_flv_short() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("short_flv", FLV_FILE_PATH_SHORT, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("short_flv", "default")
    controller.transcribe()


def test_transcribe_video_flv_medium() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("medium_flv", FLV_FILE_PATH_MEDIUM, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("medium_flv", "default")
    controller.transcribe()


def test_transcribe_video_flv_long() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("long_flv", FLV_FILE_PATH_LONG, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("long_flv", "default")
    controller.transcribe()


def test_transcribe_video_avi_short() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("short_avi", AVI_FILE_PATH_SHORT, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("short_avi", "default")
    controller.transcribe()


def test_transcribe_video_avi_medium() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("medium_avi", AVI_FILE_PATH_MEDIUM, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("medium_avi", "default")
    controller.transcribe()


def test_transcribe_video_avi_long() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("long_avi", AVI_FILE_PATH_LONG, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("long_avi", "default")
    controller.transcribe()


def test_transcribe_video_swf_short() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("short_swf", SWF_FILE_PATH_SHORT, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("short_swf", "default")
    controller.transcribe()


def test_transcribe_video_swf_medium() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("medium_swf", SWF_FILE_PATH_MEDIUM, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("medium_swf", "default")
    controller.transcribe()


def test_transcribe_video_swf_long() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("long_swf", SWF_FILE_PATH_LONG, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("long_swf", "default")
    controller.transcribe()


def test_transcribe_video_m4v_short() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("short_m4v", M4V_FILE_PATH_SHORT, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("short_m4v", "default")
    controller.transcribe()


def test_transcribe_video_m4v_medium() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("medium_m4v", M4V_FILE_PATH_MEDIUM, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("medium_m4v", "default")
    controller.transcribe()


def test_transcribe_video_m4v_long() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("long_m4v", M4V_FILE_PATH_LONG, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("long_m4v", "default")
    controller.transcribe()


def test_video_formats_combined_short() -> None:
    controller = GailBotController(WS_DIR_PATH)
    # Adding sources.
    controller.add_source("short_mov", MOV_FILE_PATH_SHORT, RESULT_DIR_PATH)
    controller.add_source("short_mxf", MXF_FILE_PATH_SHORT, RESULT_DIR_PATH)
    controller.add_source("short_wmv", WMV_FILE_PATH_SHORT, RESULT_DIR_PATH)
    controller.add_source("short_flv", FLV_FILE_PATH_SHORT, RESULT_DIR_PATH)
    controller.add_source("short_avi", AVI_FILE_PATH_SHORT, RESULT_DIR_PATH)
    controller.add_source("short_m4v", M4V_FILE_PATH_SHORT, RESULT_DIR_PATH)
    # Applying profiles.
    assert controller.apply_settings_profile_to_source("short_mov", "default")
    assert controller.apply_settings_profile_to_source("short_mxf", "default")
    assert controller.apply_settings_profile_to_source("short_wmv", "default")
    assert controller.apply_settings_profile_to_source("short_flv", "default")
    assert controller.apply_settings_profile_to_source("short_avi", "default")
    assert controller.apply_settings_profile_to_source("short_m4v", "default")
    # Transcribing
    controller.transcribe()


def test_video_formats_combined_medium() -> None:
    controller = GailBotController(WS_DIR_PATH)
    # Adding sources.
    controller.add_source("medium_mov", MOV_FILE_PATH_MEDIUM, RESULT_DIR_PATH)
    controller.add_source("medium_mxf", MXF_FILE_PATH_MEDIUM, RESULT_DIR_PATH)
    controller.add_source("medium_wmv", WMV_FILE_PATH_MEDIUM, RESULT_DIR_PATH)
    controller.add_source("medium_flv", FLV_FILE_PATH_MEDIUM, RESULT_DIR_PATH)
    controller.add_source("medium_avi", AVI_FILE_PATH_MEDIUM, RESULT_DIR_PATH)
    controller.add_source("medium_m4v", M4V_FILE_PATH_MEDIUM, RESULT_DIR_PATH)
    # Applying profiles.
    assert controller.apply_settings_profile_to_source("medium_mov", "default")
    assert controller.apply_settings_profile_to_source("medium_mxf", "default")
    assert controller.apply_settings_profile_to_source("medium_wmv", "default")
    assert controller.apply_settings_profile_to_source("medium_flv", "default")
    assert controller.apply_settings_profile_to_source("medium_avi", "default")
    assert controller.apply_settings_profile_to_source("medium_m4v", "default")
    # Transcribing
    controller.transcribe()


def test_video_formats_combined_long() -> None:
    controller = GailBotController(WS_DIR_PATH)
    # Adding sources.
    controller.add_source("long_mov", MOV_FILE_PATH_LONG, RESULT_DIR_PATH)
    controller.add_source("long_mxf", MXF_FILE_PATH_LONG, RESULT_DIR_PATH)
    controller.add_source("long_wmv", WMV_FILE_PATH_LONG, RESULT_DIR_PATH)
    controller.add_source("long_flv", FLV_FILE_PATH_LONG, RESULT_DIR_PATH)
    controller.add_source("long_avi", AVI_FILE_PATH_LONG, RESULT_DIR_PATH)
    controller.add_source("long_m4v", M4V_FILE_PATH_LONG, RESULT_DIR_PATH)
    # Applying profiles.
    assert controller.apply_settings_profile_to_source("long_mov", "default")
    assert controller.apply_settings_profile_to_source("long_mxf", "default")
    assert controller.apply_settings_profile_to_source("long_wmv", "default")
    assert controller.apply_settings_profile_to_source("long_flv", "default")
    assert controller.apply_settings_profile_to_source("long_avi", "default")
    assert controller.apply_settings_profile_to_source("long_m4v", "default")
    # Transcribing
    controller.transcribe()

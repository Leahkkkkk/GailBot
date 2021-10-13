'''
Contains tests for only the actual re-transcription process, meaning that
the inputs are previous GailBot outputs.
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


def test_transcribe_mixed_type_directory() -> None:
    """
    This is from a directory


    NOTE:
        This uses DirectorySourceLoader
        This transcribes correctly
    """
    controller = GailBotController(WS_DIR_PATH)
    # Adding sources
    controller.add_source("conversation_1_dir",
                          MIXED_DIR_PATH, RESULT_DIR_PATH)
    # Applying profiles.
    assert controller.apply_settings_profile_to_source(
        "conversation_1_dir", "default")
    # Transcribing
    controller.transcribe()


def test_transcribe_audio_mp3_short() -> None:
    """
    This is from a file.

    NOTES:
        This def. uses the FileLoader!
        This transcribes correctly!
    """
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("mp3_short", MP3_FILE_PATH_SHORT, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("mp3_short", "default")
    controller.transcribe()


def test() -> None:
    """
    This is from a previous GailBot output.
    """
    controller = GailBotController(WS_DIR_PATH)
    assert controller.add_source(
        "prev_mp3_short", PREV_AUDIO_MP3_SHORT, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source(
        "prev_mp3_short", "default")
    print(controller.transcribe())

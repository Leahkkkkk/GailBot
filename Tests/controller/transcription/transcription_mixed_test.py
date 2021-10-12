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


def test_transcribe_mixed_type_directory() -> None:
    controller = GailBotController(WS_DIR_PATH)
    # Adding sources
    controller.add_source("conversation_1_dir",
                          MIXED_DIR_PATH, RESULT_DIR_PATH)
    # Applying profiles.
    assert controller.apply_settings_profile_to_source(
        "conversation_1_dir", "default")
    # Transcribing
    controller.transcribe()

# def test_transcribe_valid_and_invalid_files_directory() -> None:
#     pass

# def test_transcribe_empty_directory() -> None:
#     pass

# def test_transcribe_large_directory() -> None:
#     pass

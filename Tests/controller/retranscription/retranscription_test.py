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


def test() -> None:
    controller = GailBotController(WS_DIR_PATH)
    assert controller.add_source(
        "prev_mp3_short", PREV_AUDIO_MP3_SHORT, RESULT_DIR_PATH)

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

# VARS

PLUGINS_TO_APPLY = [
    "tcu_analysis",
    "overlap_analysis",
    "pause_analysis",
    "fto_analysis",
    "gaps_analysis",
    "conversation_gap_analysis"
]


# SETUP #####################################s

@pytest.fixture(scope='session', autouse=True)
def reset_workspace() -> None:
    io = IO()
    io.delete(RESULT_DIR_PATH)
    io.create_directory(RESULT_DIR_PATH)

########################## TEST DEFINITIONS ##################################


def test_plugins_audio_short() -> None:
    """
    Test all analysis plugins with a short audio file.
    """
    controller = GailBotController(WS_DIR_PATH)
    print(controller.register_analysis_plugins(ANALYSIS_PLUGINS_CONFIG))
    print(controller.register_format(FORMAT_PLUGINS_CONFIG))
    controller.add_source("mp3_short", MP3_FILE_PATH_SHORT, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("mp3_short", "default")
    assert controller.set_settings_profile_attribute(
        "default", GBSettingAttrs.analysis_plugins_to_apply, PLUGINS_TO_APPLY)
    controller.transcribe()

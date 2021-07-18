'''
Contains tests for only the actual transcription process.
'''
# Standard library imports
import pytest
from typing import Dict
# Local imports
from Src.Components.io import IO
from Src.Components.controller import GailBotController, SettingsDetails,\
    SourceDetails,GBSettingAttrs,PipelineServiceSummary


############################### GLOBALS #####################################

# DIR PATHS
WS_DIR_PATH = "TestData/workspace/controller_workspace/gb_workspace"
RESULT_DIR_PATH = "TestData/workspace/controller_workspace/results"
# FILE PATHS
WAV_FILE_PATH = "TestData/media/test2a.wav"
MP3_FILE_PATH = "TestData/media/sample1.mp3"
MOV_FILE_PATH = "TestData/media/sample_video_conversation.mov"
MIXED_DIR_PATH = "TestData/media/audio_video_conversation"
ANALYSIS_PLUGINS_CONFIG = "TestData/plugins/pipeline_service_test/analysis_config.json"
FORMAT_PLUGINS_CONFIG = "TestData/plugins/pipeline_service_test/format_config.json"
EMPTY_JSON = "TestData/configs/empty_json.json"
NUM_THREADS = 4


############################### SETUP #####################################


@pytest.fixture(scope='session', autouse=True)
def reset_workspace() -> None:
    io = IO()
    io.delete(RESULT_DIR_PATH)
    io.create_directory(RESULT_DIR_PATH)

########################## TEST DEFINITIONS ##################################

def test_transcribe() -> None:
    """
    Tests:
        1. Transcribe without adding any sources.
        2. Transcribe multiple sources.
    """
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("audio_transcribing",MP3_FILE_PATH,RESULT_DIR_PATH)
    controller.add_source("video_transcribing",MOV_FILE_PATH,RESULT_DIR_PATH)
    controller.add_source("mixed_transcribing",MIXED_DIR_PATH,RESULT_DIR_PATH)
    summary = controller.transcribe()
    print(summary)
    # Add settings profile to sources and then re-try.
    assert controller.apply_settings_profile_to_sources(
        ["audio_transcribing","video_transcribing","mixed_transcribing"],"default")
    print(controller.is_source_ready_to_transcribe("audio"))
    summary = controller.transcribe()
    print(summary)

# TODO: Add individual transcription tests for all supported formats.

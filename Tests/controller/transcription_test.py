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
# CONFIG FILE PATHS
ANALYSIS_PLUGINS_CONFIG = "TestData/plugins/pipeline_service_test/analysis_config.json"
FORMAT_PLUGINS_CONFIG = "TestData/plugins/pipeline_service_test/format_config.json"
# AUDIO FILE PATHS
WAV_FILE_PATH = ""
MP3_FILE_PATH_SHORT = "TestData/transcription_tests_media/audio/mp3/sample1.mp3"
MP3_FILE_PATH_MEDIUM = "TestData/transcription_tests_media/audio/mp3/medium.mp3"
MP3_FILE_PATH_LONG = "TestData/transcription_tests_media/audio/mp3/07assassination1.mp3"
# VIDEO FILE PATHS
MOV_FILE_PATH = ""
# MEDIA DIRECTORY PATHS
MIXED_DIR_PATH = ""
# VARS
NUM_THREADS = 4


############################### SETUP #####################################


@pytest.fixture(scope='session', autouse=True)
def reset_workspace() -> None:
    io = IO()
    io.delete(RESULT_DIR_PATH)
    io.create_directory(RESULT_DIR_PATH)

########################## TEST DEFINITIONS ##################################

def test_transcribe_audio_mp3() -> None:
    """
    Tests:
        1. Transcribe multiple mp3 files of different lengths
    """
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("mp3_short",MP3_FILE_PATH_SHORT,RESULT_DIR_PATH)
    controller.add_source("mp3_medium",MP3_FILE_PATH_MEDIUM,RESULT_DIR_PATH)
    # TODO: Run the long file for some tests only.
    controller.add_source("mp3_long",MP3_FILE_PATH_LONG,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_sources(
        ["mp3_short","mp3_medium","mp3_long"],"default")
    controller.transcribe()

def test_transcribe_audio_mpeg() -> None:
    pass

def test_transcribe_audio_opus() -> None:
    pass

def test_transcribe_audio_wav() -> None:
    pass

def test_transcribe_video_mxf() -> None:
    pass

def test_transcribe_video_mov() -> None:
    pass

def test_transcribe_video_wmv() -> None:
    pass

def test_transcribe_video_flv() -> None:
    pass

def test_transcribe_video_avi() -> None:
    pass

def test_transcribe_video_swf() -> None:
    pass

def test_transcribe_video_m4v() -> None:
    pass

def test_transcribe_mixed_type_directory() -> None:
    pass

def test_transcribe_valid_and_invalid_files_directory() -> None:
    pass

def test_transcribe_empty_directory() -> None:
    pass

def test_transcribe_large_directory() -> None:
    pass

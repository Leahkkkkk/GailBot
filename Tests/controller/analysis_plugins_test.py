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
ANALYSIS_PLUGINS_CONFIG = "Src/default_plugins/analysis_plugins/analysis_config.json"
FORMAT_PLUGINS_CONFIG = "Src/default_plugins/chat_format/format_config.json"
# AUDIO FILE PATHS
MP3_FILE_PATH_SHORT = "TestData/transcription_tests_media/audio/mp3/sample1.mp3"
MP3_FILE_PATH_MEDIUM = "TestData/transcription_tests_media/audio/mp3/medium.mp3"
MP3_FILE_PATH_LONG = "TestData/transcription_tests_media/audio/mp3/07assassination1.mp3"
OPUS_FILE_PATH_SHORT = "TestData/transcription_tests_media/audio/opus/sample1.opus"
OPUS_FILE_PATH_MEDIUM = "TestData/transcription_tests_media/audio/opus/medium.opus"
OPUS_FILE_PATH_LONG = "TestData/transcription_tests_media/audio/opus/07assassination1.opus"
MPEG_FILE_PATH_SHORT = "TestData/transcription_tests_media/audio/mpeg/sample1.mpeg"
MPEG_FILE_PATH_MEDIUM = "TestData/transcription_tests_media/audio/mpeg/medium.mpeg"
MPEG_FILE_PATH_LONG = "TestData/transcription_tests_media/audio/mpeg/07assassination1.mpeg"
WAV_FILE_PATH_SHORT = "TestData/transcription_tests_media/audio/wav/test.wav"
WAV_FILE_PATH_MEDIUM = "TestData/transcription_tests_media/audio/wav/test2a.wav"
WAV_FILE_PATH_LONG = "TestData/transcription_tests_media/audio/wav/07assassination1.wav"
# VIDEO FILE PATHS
MOV_FILE_PATH_SHORT = "TestData/transcription_tests_media/audio/mov/short.mov"
MOV_FILE_PATH_MEDIUM = ""
MOV_FILE_PATH_LONG = ""
MXF_FILE_PATH_SHORT = "TestData/transcription_tests_media/audio/mxf/short.mxf"
MXF_FILE_PATH_MEDIUM = ""
MXF_FILE_PATH_LONG = ""
WMV_FILE_PATH_SHORT = "TestData/transcription_tests_media/audio/wmv/short.wmv"
WMV_FILE_PATH_MEDIUM = ""
WMV_FILE_PATH_LONG = ""
FLV_FILE_PATH_SHORT = "TestData/transcription_tests_media/audio/flv/short.flv"
FLV_FILE_PATH_MEDIUM = ""
FLV_FILE_PATH_LONG = ""
AVI_FILE_PATH_SHORT = "TestData/transcription_tests_media/audio/avi/short.avi"
AVI_FILE_PATH_MEDIUM = ""
AVI_FILE_PATH_LONG = ""
SWF_FILE_PATH_SHORT = "TestData/transcription_tests_media/audio/swf/short.swf"
SWF_FILE_PATH_MEDIUM = ""
SWF_FILE_PATH_LONG = ""
M4V_FILE_PATH_SHORT = "TestData/transcription_tests_media/audio/m4v/short.m4v"
M4V_FILE_PATH_MEDIUM = ""
M4V_FILE_PATH_LONG = ""
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

def test_plugins_audio_short() -> None:
    """
    Test all analysis plugins with a short audio file.
    """
    controller = GailBotController(WS_DIR_PATH)
    print(controller.register_analysis_plugins(ANALYSIS_PLUGINS_CONFIG))
    controller.add_source("mp3_short",MP3_FILE_PATH_SHORT,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("mp3_short","default")
    assert controller.set_settings_profile_attribute(
        "default",GBSettingAttrs.analysis_plugins_to_apply,
        ["tcu","overlaps"])
    controller.transcribe()


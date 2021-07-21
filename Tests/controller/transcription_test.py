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

#### AUDIO TESTS

def test_transcribe_audio_mp3_short() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("mp3_short",MP3_FILE_PATH_SHORT,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("mp3_short","default")
    controller.transcribe()

def test_transcribe_audio_mp3_medium() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("mp3_medium",MP3_FILE_PATH_MEDIUM,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("mp3_medium","default")
    controller.transcribe()

def test_transcribe_audio_mp3_long():
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("mp3_long",MP3_FILE_PATH_LONG,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("mp3_long","default")
    controller.transcribe()

def test_transcribe_audio_mpeg_short() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("short_mpeg",WAV_FILE_PATH_SHORT,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("short_mpeg","default")
    controller.transcribe()

def test_transcribe_audio_mpeg_medium() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("medium_mpeg",WAV_FILE_PATH_MEDIUM,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("medium_mpeg","default")
    controller.transcribe()

def test_transcribe_audio_mpeg_long() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("long_mpeg",WAV_FILE_PATH_LONG,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("long_mpeg","default")
    controller.transcribe()

def test_transcribe_audio_opus_short() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("short_opus",OPUS_FILE_PATH_SHORT,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("short_opus","default")
    controller.transcribe()

def test_transcribe_audio_opus_medium() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("medium_opus",OPUS_FILE_PATH_MEDIUM,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("medium_opus","default")
    controller.transcribe()

def test_transcribe_audio_opus_long() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("long_opus",OPUS_FILE_PATH_LONG,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("long_opus","default")
    controller.transcribe()

def test_transcribe_audio_wav_short() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("short_wav",WAV_FILE_PATH_SHORT,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("short_wav","default")
    controller.transcribe()

def test_transcribe_audio_wav_medium() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("medium_wav",WAV_FILE_PATH_MEDIUM,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("medium_wav","default")
    controller.transcribe()

def test_transcribe_audio_wav_long() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("long_wav",WAV_FILE_PATH_LONG,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("long_wav","default")
    controller.transcribe()

def test_audio_formats_combined_short() -> None:
    controller = GailBotController(WS_DIR_PATH)
    # Adding sources.
    controller.add_source("short_mp3",MP3_FILE_PATH_SHORT,RESULT_DIR_PATH)
    controller.add_source("short_mpeg",WAV_FILE_PATH_SHORT,RESULT_DIR_PATH)
    controller.add_source("short_opus",OPUS_FILE_PATH_SHORT,RESULT_DIR_PATH)
    controller.add_source("short_wav",WAV_FILE_PATH_SHORT,RESULT_DIR_PATH)
    # Applying settings profiles
    assert controller.apply_settings_profile_to_source("short_mp3","default")
    assert controller.apply_settings_profile_to_source("short_mpeg","default")
    assert controller.apply_settings_profile_to_source("short_opus","default")
    assert controller.apply_settings_profile_to_source("short_wav","default")
    # Transcribing.
    controller.transcribe()

def test_audio_formats_combined_medium() -> None:
    controller = GailBotController(WS_DIR_PATH)
    # Adding sources.
    controller.add_source("medium_mp3",MP3_FILE_PATH_MEDIUM,RESULT_DIR_PATH)
    controller.add_source("medium_mpeg",WAV_FILE_PATH_MEDIUM,RESULT_DIR_PATH)
    controller.add_source("medium_opus",OPUS_FILE_PATH_MEDIUM,RESULT_DIR_PATH)
    controller.add_source("medium_wav",WAV_FILE_PATH_MEDIUM,RESULT_DIR_PATH)
    # Applying settings profiles
    assert controller.apply_settings_profile_to_source("medium_mp3","default")
    assert controller.apply_settings_profile_to_source("medium_mpeg","default")
    assert controller.apply_settings_profile_to_source("medium_opus","default")
    assert controller.apply_settings_profile_to_source("medium_wav","default")
    # Transcribing.
    controller.transcribe()

def test_audio_formats_combined_long() -> None:
    controller = GailBotController(WS_DIR_PATH)
    # Adding sources.
    controller.add_source("long_mp3",MP3_FILE_PATH_LONG,RESULT_DIR_PATH)
    controller.add_source("long_mpeg",WAV_FILE_PATH_LONG,RESULT_DIR_PATH)
    controller.add_source("long_opus",OPUS_FILE_PATH_LONG,RESULT_DIR_PATH)
    controller.add_source("long_wav",WAV_FILE_PATH_LONG,RESULT_DIR_PATH)
    # Applying settings profiles
    assert controller.apply_settings_profile_to_source("long_mp3","default")
    assert controller.apply_settings_profile_to_source("long_mpeg","default")
    assert controller.apply_settings_profile_to_source("long_opus","default")
    assert controller.apply_settings_profile_to_source("long_wav","default")
    # Transcribing.
    controller.transcribe()

#### VIDEO TESTS

def test_transcribe_video_mov_short() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("short_mov",MOV_FILE_PATH_SHORT,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("short_mov","default")
    controller.transcribe()

def test_transcribe_video_mov_medium() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("medium_mov",MOV_FILE_PATH_MEDIUM,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("medium_mov","default")
    controller.transcribe()

def test_transcribe_video_mov_long() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("long_mov",MOV_FILE_PATH_LONG,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("long_mov","default")
    controller.transcribe()

def test_transcribe_video_mxf_short() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("short_mxf",MXF_FILE_PATH_SHORT,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("short_mxf","default")
    controller.transcribe()

def test_transcribe_video_mxf_medium() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("medium_mxf",MXF_FILE_PATH_MEDIUM,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("medium_mxf","default")
    controller.transcribe()

def test_transcribe_video_mxf_long() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("long_mxf",MXF_FILE_PATH_LONG,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("long_mxf","default")
    controller.transcribe()

def test_transcribe_video_wmv_short() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("short_wmv",WMV_FILE_PATH_SHORT,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("short_wmv","default")
    controller.transcribe()

def test_transcribe_video_wmv_medium() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("medium_wmv",WMV_FILE_PATH_MEDIUM,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("medium_wmv","default")
    controller.transcribe()

def test_transcribe_video_wmv_long() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("long_wav",WMV_FILE_PATH_LONG,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("long_wmv","default")
    controller.transcribe()

def test_transcribe_video_flv_short() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("short_flv",FLV_FILE_PATH_SHORT,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("short_flv","default")
    controller.transcribe()

def test_transcribe_video_flv_medium() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("medium_flv",FLV_FILE_PATH_MEDIUM,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("medium_flv","default")
    controller.transcribe()

def test_transcribe_video_flv_long() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("long_flv",FLV_FILE_PATH_LONG,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("long_flv","default")
    controller.transcribe()

def test_transcribe_video_avi_short() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("short_avi",AVI_FILE_PATH_SHORT,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("short_avi","default")
    controller.transcribe()

def test_transcribe_video_avi_medium() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("medium_avi",AVI_FILE_PATH_MEDIUM,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("medium_avi","default")
    controller.transcribe()

def test_transcribe_video_avi_long() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("long_avi",AVI_FILE_PATH_LONG,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("long_avi","default")
    controller.transcribe()

def test_transcribe_video_swf_short() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("short_swf",SWF_FILE_PATH_SHORT,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("short_swf","default")
    controller.transcribe()

def test_transcribe_video_swf_medium() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("medium_swf",SWF_FILE_PATH_MEDIUM,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("medium_swf","default")
    controller.transcribe()

def test_transcribe_video_swf_long() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("long_swf",SWF_FILE_PATH_LONG,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("long_swf","default")
    controller.transcribe()

def test_transcribe_video_m4v_short() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("short_m4v",M4V_FILE_PATH_SHORT,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("short_m4v","default")
    controller.transcribe()

def test_transcribe_video_m4v_medium() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("medium_m4v",M4V_FILE_PATH_MEDIUM,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("medium_m4v","default")
    controller.transcribe()

def test_transcribe_video_m4v_long() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("long_m4v",M4V_FILE_PATH_LONG,RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("long_m4v","default")
    controller.transcribe()

def test_video_formats_combined_short() -> None:
    controller = GailBotController(WS_DIR_PATH)
    # Adding sources.
    controller.add_source("short_mov",MOV_FILE_PATH_SHORT,RESULT_DIR_PATH)
    controller.add_source("short_mxf",MXF_FILE_PATH_SHORT,RESULT_DIR_PATH)
    controller.add_source("short_wmv",WMV_FILE_PATH_SHORT,RESULT_DIR_PATH)
    controller.add_source("short_flv",FLV_FILE_PATH_SHORT,RESULT_DIR_PATH)
    controller.add_source("short_avi",AVI_FILE_PATH_SHORT,RESULT_DIR_PATH)
    controller.add_source("short_m4v",M4V_FILE_PATH_SHORT,RESULT_DIR_PATH)
    # Applying profiles.
    assert controller.apply_settings_profile_to_source("short_mov","default")
    assert controller.apply_settings_profile_to_source("short_mxf","default")
    assert controller.apply_settings_profile_to_source("short_wmv","default")
    assert controller.apply_settings_profile_to_source("short_flv","default")
    assert controller.apply_settings_profile_to_source("short_avi","default")
    assert controller.apply_settings_profile_to_source("short_m4v","default")
    # Transcribing
    controller.transcribe()

def test_video_formats_combined_medium() -> None:
    controller = GailBotController(WS_DIR_PATH)
    # Adding sources.
    controller.add_source("medium_mov",MOV_FILE_PATH_MEDIUM,RESULT_DIR_PATH)
    controller.add_source("medium_mxf",MXF_FILE_PATH_MEDIUM,RESULT_DIR_PATH)
    controller.add_source("medium_wmv",WMV_FILE_PATH_MEDIUM,RESULT_DIR_PATH)
    controller.add_source("medium_flv",FLV_FILE_PATH_MEDIUM,RESULT_DIR_PATH)
    controller.add_source("medium_avi",AVI_FILE_PATH_MEDIUM,RESULT_DIR_PATH)
    controller.add_source("medium_m4v",M4V_FILE_PATH_MEDIUM,RESULT_DIR_PATH)
    # Applying profiles.
    assert controller.apply_settings_profile_to_source("medium_mov","default")
    assert controller.apply_settings_profile_to_source("medium_mxf","default")
    assert controller.apply_settings_profile_to_source("medium_wmv","default")
    assert controller.apply_settings_profile_to_source("medium_flv","default")
    assert controller.apply_settings_profile_to_source("medium_avi","default")
    assert controller.apply_settings_profile_to_source("medium_m4v","default")
    # Transcribing
    controller.transcribe()

def test_video_formats_combined_long() -> None:
    controller = GailBotController(WS_DIR_PATH)
    # Adding sources.
    controller.add_source("long_mov",MOV_FILE_PATH_LONG,RESULT_DIR_PATH)
    controller.add_source("long_mxf",MXF_FILE_PATH_LONG,RESULT_DIR_PATH)
    controller.add_source("long_wmv",WMV_FILE_PATH_LONG,RESULT_DIR_PATH)
    controller.add_source("long_flv",FLV_FILE_PATH_LONG,RESULT_DIR_PATH)
    controller.add_source("long_avi",AVI_FILE_PATH_LONG,RESULT_DIR_PATH)
    controller.add_source("long_m4v",M4V_FILE_PATH_LONG,RESULT_DIR_PATH)
    # Applying profiles.
    assert controller.apply_settings_profile_to_source("long_mov","default")
    assert controller.apply_settings_profile_to_source("long_mxf","default")
    assert controller.apply_settings_profile_to_source("long_wmv","default")
    assert controller.apply_settings_profile_to_source("long_flv","default")
    assert controller.apply_settings_profile_to_source("long_avi","default")
    assert controller.apply_settings_profile_to_source("long_m4v","default")
    # Transcribing
    controller.transcribe()

##### DIRECTORY TESTS

# def test_transcribe_mixed_type_directory() -> None:
#     pass

# def test_transcribe_valid_and_invalid_files_directory() -> None:
#     pass

# def test_transcribe_empty_directory() -> None:
#     pass

# def test_transcribe_large_directory() -> None:
#     pass

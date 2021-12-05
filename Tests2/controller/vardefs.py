# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-10-21 10:29:49
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-05 14:59:09

""" DIRECTORIES """


WS_DIR_PATH = "test_data/controller_data/workspaces/temp_ws"
RESULT_DIR_PATH = "test_data/controller_data/workspaces/results"
IMAGES_DIR_PATH = "test_data/controller_data/images"
CONV_DIR_PATH = "test_data/controller_data/media/conversations/conversation"
MIXED_DIR_PATH = "test_data/controller_data/media/conversations/conversation_1"
EMPTY_DIR_PATH = "test_data/controller_data/workspaces/empty"
SETTINGS_DIR_PATH = "test_data/controller_data/workspaces/temp_ws"
SOURCE_DIR_PATH = "test_data/controller_data/workspaces/temp_ws"
DIR_CONV_PATH = "test_data/controller_data/media/conversations/conversation"
AUDIO_VIDEO_DIR_PATH = "test_data/controller_data/media/conversations/audio_video_conversation"
TRANSCRIBED_DIR = "test_data/controller_data/media/conversations/transcribed_audio_video_dir"
""" MEDIA FILES """


# Mp3 files
MP3_FILE_PATH = "test_data/controller_data/media/audio/mp3/sample1.mp3"
MP3_FILE_PATH_SHORT = "test_data/controller_data/media/audio/mp3/sample1.mp3"
MP3_FILE_PATH_MEDIUM = "test_data/controller_data/media/audio/mp3/medium.mp3"
MP3_FILE_PATH_LONG = "test_data/controller_data/media/audio/mp3/07assassination1.mp3"

# Opus files
OPUS_FILE_PATH_SHORT = "test_data/controller_data/media/audio/opus/sample1.opus"
OPUS_FILE_PATH_MEDIUM = "test_data/controller_data/media/audio/opus/medium.opus"
OPUS_FILE_PATH_LONG = "test_data/controller_data/media/audio/opus/07assassination1.opus"

# MPEG files
MPEG_FILE_PATH_SHORT = "test_data/controller_data/media/audio/mpeg/sample1.mpeg"
MPEG_FILE_PATH_MEDIUM = "test_data/controller_data/media/audio/mpeg/medium.mpeg"
MPEG_FILE_PATH_LONG = "test_data/controller_data/media/audio/mpeg/07assassination1.mpeg"

# Wav files
WAV_FILE_PATH = "test_data/controller_data/media/audio/wav/test.wav"
WAV_FILE_PATH_SHORT = "test_data/controller_data/media/audio/wav/test.wav"
WAV_FILE_PATH_MEDIUM = "test_data/controller_data/media/audio/wav/test2a.wav"
WAV_FILE_PATH_LONG = "test_data/controller_data/media/audio/wav/07assassination1.wav"

# Flv files
FLV_FILE_PATH_SHORT = "test_data/controller_data/media/audio/flv/short.flv"
FLV_FILE_PATH_MEDIUM = ""
FLV_FILE_PATH_LONG = ""

# Avi files
AVI_FILE_PATH_SHORT = "test_data/controller_data/media/audio/avi/short.avi"
AVI_FILE_PATH_MEDIUM = ""
AVI_FILE_PATH_LONG = ""

# Swf files
SWF_FILE_PATH_SHORT = "test_data/controller_data/media/audio/swf/short.swf"
SWF_FILE_PATH_MEDIUM = ""
SWF_FILE_PATH_LONG = ""

# M4V files
M4V_FILE_PATH_SHORT = "test_data/controller_data/media/audio/m4v/short.m4v"
M4V_FILE_PATH_MEDIUM = ""
M4V_FILE_PATH_LONG = ""

# MOV files
MOV_FILE_PATH = "test_data/controller_data/media/audio/mov/short.mov"
MOV_FILE_PATH_SHORT = "test_data/controller_data/media/audio/mov/short.mov"
MOV_FILE_PATH_MEDIUM = ""
MOV_FILE_PATH_LONG = ""

# MXF files
MXF_FILE_PATH_SHORT = "test_data/controller_data/media/audio/mxf/vid2.MXF"
MXF_FILE_PATH_MEDIUM = ""
MXF_FILE_PATH_LONG = ""

# WMV files
WMV_FILE_PATH_SHORT = "test_data/controller_data/media/audio/wmv/short.wmv"
WMV_FILE_PATH_MEDIUM = ""
WMV_FILE_PATH_LONG = ""

""" PREVIOUS GAILBOT OUTPUT """
PREV_AUDIO_MP3_SHORT = "test_data/controller_data/gb_output/mp3_short_0"
PREV_MIXED_DIR_PATH = "test_data/controller_data/gb_output/conversation_1_dir_0"


""" CONFIGURATION FILES """
CONFIG_FILE_PATH = "test_data/controller_data/configs/config.json"
ANALYSIS_PLUGINS_CONFIG = "test_data/controller_data/configs/plugins/analysis_config.json"
FORMAT_PLUGINS_CONFIG = "test_data/controller_data/configs/plugins/format_config.json"
EMPTY_JSON = "test_data/controller_data/configs/empty_json.json"
DEFAULT_ANALYSIS_PLUGIN_CONFIG = "Src2/plugins/analysis/config.json"


""" OTHER FILES """
TXT_FILE_PATH = "test_data/controller_data/configs/textfile.txt"

""" VARS """

NUM_THREADS = 4
SETTINGS_PROFILE_EXTENSION = "json"
WATSON_API_KEY = "MSgOPTS9CvbADe49nEg4wm8_gxeRuf4FGUmlHS9QqAw3"
WATSON_LANG_CUSTOM_ID = "41e54a38-2175-45f4-ac6a-1c11e42a2d54"
WATSON_BASE_LANG_MODEL = "en-US_BroadbandModel"
WATSON_REGION = "dallas"
PLUGINS_TO_APPLY = [
    "turn_construct",
    "overlaps",
    "pauses",
    "combine_turns",
    "fto",
    "gaps",
    "chat"]

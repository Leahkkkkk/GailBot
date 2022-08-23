# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-23 11:56:06
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-23 13:51:07

# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-04-29 13:45:19
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-04-29 15:55:55
import os
import sys

# --------------------------- OUTPUT DIR STRUCTURE -----------------------------
# --------------  Paths
# Roots
TESTING_FRAMEWORK_ROOT = "./tests/test_results"
RESULTS_ROOT_DIR = os.path.join(TESTING_FRAMEWORK_ROOT, "results")
WORKSPACES_ROOT_DIR = os.path.join(TESTING_FRAMEWORK_ROOT, "workspaces")
# Component results
CONTROLLER_RESULTS = os.path.join(RESULTS_ROOT_DIR, "controller")
ENGINES_RESULTS = os.path.join(RESULTS_ROOT_DIR, "engines")
IO_RESULTS = os.path.join(RESULTS_ROOT_DIR, "io")
NETWORK_RESULTS = os.path.join(RESULTS_ROOT_DIR, "network")
ORGANIZER_SERVICE_RESULTS = os.path.join(RESULTS_ROOT_DIR, "organizer_service")
PIPELINE_RESULTS = os.path.join(RESULTS_ROOT_DIR, "pipeline")
PIPELINE_SERVICE_RESULTS = os.path.join(RESULTS_ROOT_DIR, "pipeline_service")
PLUGIN_MANAGER_RESULTS = os.path.join(RESULTS_ROOT_DIR, "plugin_manager")
SHARED_MODELS_RESULT = os.path.join(RESULTS_ROOT_DIR, "shared_models")
TRANSCRIPTION_RESULT = os.path.join(RESULTS_ROOT_DIR, "transcription")
# Component workspaces
CONTROLLER_WORKSPACE = os.path.join(WORKSPACES_ROOT_DIR, "controller")
ENGINES_WORKSPACE = os.path.join(WORKSPACES_ROOT_DIR, "engines")
IO_WORKSPACE = os.path.join(WORKSPACES_ROOT_DIR, "io")
NETWORK_WORKSPACE = os.path.join(WORKSPACES_ROOT_DIR, "network")
ORGANIZER_SERVICE_WORKSPACE = os.path.join(
    WORKSPACES_ROOT_DIR, "organizer_service")
PIPELINE_WORKSPACE = os.path.join(WORKSPACES_ROOT_DIR, "pipeline")
PIPELINE_SERVICE_WORKSPACE = os.path.join(
    WORKSPACES_ROOT_DIR, "pipeline_service")
PLUGIN_MANAGER_WORKSPACE = os.path.join(WORKSPACES_ROOT_DIR, "plugin_manager")
SHARED_MODELS_WORKSPACE = os.path.join(WORKSPACES_ROOT_DIR, "shared_models")
TRANSCRIPTION_WORKSPACE = os.path.join(WORKSPACES_ROOT_DIR, "transcription")


# --------------------------- INPUT DIR STRUCTURE -----------------------------
# ---- ROOT DIRS
# TODO: This needs to change based on the input data directory.
DEV_TEST_DATA_DIR = "/Users/muhammadumair/Documents/Research/Projects Data/gailbot/dev_test_data"
# ---- AUDIO_DATA
#  -- MP3
MP3_ASSASSINATION_FILE = os.path.join(
    DEV_TEST_DATA_DIR, "media/audio/mp3/07assassination1.mp3")
MP3_MEDIUM_FILE = os.path.join(DEV_TEST_DATA_DIR, "media/audio/mp3/medium.mp3")
MP3_SAMPLE1_FILE = os.path.join(
    DEV_TEST_DATA_DIR, "media/audio/mp3/sample1.mp3")
#  -- OPUS
OPUS_ASSASSINATION_FILE = os.path.join(
    DEV_TEST_DATA_DIR, "media/audio/opus/07assassination1.opus")
OPUS_MEDIUM_FILE = os.path.join(
    DEV_TEST_DATA_DIR, "media/audio/opus/medium.opus")
OPUS_SAMPLE1_FILE = os.path.join(
    DEV_TEST_DATA_DIR, "media/audio/opus/sample1.opus")
# -- WAV
WAV_ASSASSINATION_FILE = os.path.join(
    DEV_TEST_DATA_DIR, "media/audio/wav/07assassination1.wav")
WAV_SINE_FILE = os.path.join(
    DEV_TEST_DATA_DIR, "media/audio/wav/SineWaveMinus16.wav")
WAV_TEST_OUTPUT_FILE = os.path.join(
    DEV_TEST_DATA_DIR, "media/audio/wav/test_output.wav")
WAV_TEST2A_FILE = os.path.join(
    DEV_TEST_DATA_DIR, "media/audio/wav/test2a.wav")
WAV_TEST2B_FILE = os.path.join(
    DEV_TEST_DATA_DIR, "media/audio/wav/test2b.wav")
# ---- VIDEO DATA
# ---- CONVERSATION DATA
SHORT_CONVERSATION_2_AUDIO = os.path.join(
    DEV_TEST_DATA_DIR, "media/conversations/small_conversation")

# ---- PREVIOUS OUTPUT DATA
# ---- IMAGES
JPG_KITTEN_TONGUE = os.path.join(
    DEV_TEST_DATA_DIR, "dev_test_data/images/kitten_tongue.jpg")
JPG_PANDA = os.path.join(
    DEV_TEST_DATA_DIR, "dev_test_data/images/PANDA.jpg")
JPG_RACOON_MATH = os.path.join(
    DEV_TEST_DATA_DIR, "dev_test_data/images/racoon_math.jpg")
JPG_SAD_BDAY_CAT = os.path.join(
    DEV_TEST_DATA_DIR, "dev_test_data/images/sad_bday_cat.jpg")
JPG_SKATER_GOAT = os.path.join(
    DEV_TEST_DATA_DIR, "dev_test_data/images/skater_goat.jpg")
# ---- OTHER FILES
CONFIG_JSON = os.path.join(
    DEV_TEST_DATA_DIR, "dev_test_data/files/config.json")
FRUITS_YAML = os.path.join(
    DEV_TEST_DATA_DIR, "dev_test_data/files/fruits.yaml")
NORMAN_TEXT_PDF = os.path.join(
    DEV_TEST_DATA_DIR, "dev_test_data/files/norman_text.pdf")
SAMPLE_PDF_1 = os.path.join(
    DEV_TEST_DATA_DIR, "dev_test_data/files/sample_pdf_1.pdf")
SAMPLE_TEXT = os.path.join(
    DEV_TEST_DATA_DIR, "dev_test_data/files/sample_text.txt")
SAMPLE_YAML = os.path.join(
    DEV_TEST_DATA_DIR, "dev_test_data/files/sample_yaml.yaml")
TEXTFILE = os.path.join(
    DEV_TEST_DATA_DIR, "dev_test_data/files/textfile.txt")

# --------------------------- COMPONENT PARAMETERS --------------------------


# --------------- Engines
# IBM Watson Vars.
WATSON_API_KEY = "MSgOPTS9CvbADe49nEg4wm8_gxeRuf4FGUmlHS9QqAw3"
WATSON_LANG_CUSTOM_ID = "41e54a38-2175-45f4-ac6a-1c11e42a2d54"
WATSON_REGION = "dallas"
WATSON_BASE_LANG_MODEL = "en-US_NarrowbandModel"


#  ------------- Controller

SETTINGS_PROFILE_NAME = "test_profile"
SETTINGS_PROFILE_EXTENSION = "json"


import pytest

from gailbot import GailBotController, GailBotSettings

def test_initialize():
    controller = GailBotController("./")
    controller.add_source(
        "test",
        "/Users/muhammadumair/Desktop/sample1.mp3",
        "./gb_results"
    )
    controller.create_new_settings_profile(
        "test_profile",
        {
            "core": {},
            "plugins": {
                "plugins_to_apply": []
            },
            "engines": {
                "engine_type": "watson",
                "watson_engine": {
                    "watson_api_key": WATSON_API_KEY,
                    "watson_language_customization_id": WATSON_LANG_CUSTOM_ID,
                    "watson_base_language_model": WATSON_BASE_LANG_MODEL,
                    "watson_region": WATSON_REGION,

                }
            }
        }
    )
    controller.apply_settings_profile_to_source("test","test_profile")

    controller.register_plugins(
        "/Users/muhammadumair/Documents/Repositories/mumair01-repos/GailBot/plugins/HiLabSuite/src"
    )


    assert controller.is_source_ready_to_transcribe("test")
    # controller.transcribe()

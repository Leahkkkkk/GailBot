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

# AUDIO TESTS


def test_transcribe_audio_mp3_short() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("mp3_short", MP3_FILE_PATH_SHORT, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("mp3_short", "default")
    controller.transcribe()


def test_transcribe_audio_mp3_medium() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("mp3_medium", MP3_FILE_PATH_MEDIUM, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("mp3_medium", "default")
    controller.transcribe()


def test_transcribe_audio_mp3_long():
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("mp3_long", MP3_FILE_PATH_LONG, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("mp3_long", "default")
    controller.transcribe()


def test_transcribe_audio_mpeg_short() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("short_mpeg", WAV_FILE_PATH_SHORT, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("short_mpeg", "default")
    controller.transcribe()


def test_transcribe_audio_mpeg_medium() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("medium_mpeg", WAV_FILE_PATH_MEDIUM, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source(
        "medium_mpeg", "default")
    controller.transcribe()


def test_transcribe_audio_mpeg_long() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("long_mpeg", WAV_FILE_PATH_LONG, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("long_mpeg", "default")
    controller.transcribe()


def test_transcribe_audio_opus_short() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("short_opus", OPUS_FILE_PATH_SHORT, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("short_opus", "default")
    controller.transcribe()


def test_transcribe_audio_opus_medium() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source(
        "medium_opus", OPUS_FILE_PATH_MEDIUM, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source(
        "medium_opus", "default")
    controller.transcribe()


def test_transcribe_audio_opus_long() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("long_opus", OPUS_FILE_PATH_LONG, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("long_opus", "default")
    controller.transcribe()


def test_transcribe_audio_wav_short() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("short_wav", WAV_FILE_PATH_SHORT, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("short_wav", "default")
    controller.transcribe()


def test_transcribe_audio_wav_medium() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("medium_wav", WAV_FILE_PATH_MEDIUM, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("medium_wav", "default")
    controller.transcribe()


def test_transcribe_audio_wav_long() -> None:
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("long_wav", WAV_FILE_PATH_LONG, RESULT_DIR_PATH)
    assert controller.apply_settings_profile_to_source("long_wav", "default")
    controller.transcribe()


def test_audio_formats_combined_short() -> None:
    controller = GailBotController(WS_DIR_PATH)
    # Adding sources.
    controller.add_source("short_mp3", MP3_FILE_PATH_SHORT, RESULT_DIR_PATH)
    controller.add_source("short_mpeg", WAV_FILE_PATH_SHORT, RESULT_DIR_PATH)
    controller.add_source("short_opus", OPUS_FILE_PATH_SHORT, RESULT_DIR_PATH)
    controller.add_source("short_wav", WAV_FILE_PATH_SHORT, RESULT_DIR_PATH)
    # Applying settings profiles
    assert controller.apply_settings_profile_to_source("short_mp3", "default")
    assert controller.apply_settings_profile_to_source("short_mpeg", "default")
    assert controller.apply_settings_profile_to_source("short_opus", "default")
    assert controller.apply_settings_profile_to_source("short_wav", "default")
    # Transcribing.
    controller.transcribe()


def test_audio_formats_combined_medium() -> None:
    controller = GailBotController(WS_DIR_PATH)
    # Adding sources.
    controller.add_source("medium_mp3", MP3_FILE_PATH_MEDIUM, RESULT_DIR_PATH)
    controller.add_source("medium_mpeg", WAV_FILE_PATH_MEDIUM, RESULT_DIR_PATH)
    controller.add_source(
        "medium_opus", OPUS_FILE_PATH_MEDIUM, RESULT_DIR_PATH)
    controller.add_source("medium_wav", WAV_FILE_PATH_MEDIUM, RESULT_DIR_PATH)
    # Applying settings profiles
    assert controller.apply_settings_profile_to_source("medium_mp3", "default")
    assert controller.apply_settings_profile_to_source(
        "medium_mpeg", "default")
    assert controller.apply_settings_profile_to_source(
        "medium_opus", "default")
    assert controller.apply_settings_profile_to_source("medium_wav", "default")
    # Transcribing.
    controller.transcribe()


def test_audio_formats_combined_long() -> None:
    controller = GailBotController(WS_DIR_PATH)
    # Adding sources.
    controller.add_source("long_mp3", MP3_FILE_PATH_LONG, RESULT_DIR_PATH)
    controller.add_source("long_mpeg", WAV_FILE_PATH_LONG, RESULT_DIR_PATH)
    controller.add_source("long_opus", OPUS_FILE_PATH_LONG, RESULT_DIR_PATH)
    controller.add_source("long_wav", WAV_FILE_PATH_LONG, RESULT_DIR_PATH)
    # Applying settings profiles
    assert controller.apply_settings_profile_to_source("long_mp3", "default")
    assert controller.apply_settings_profile_to_source("long_mpeg", "default")
    assert controller.apply_settings_profile_to_source("long_opus", "default")
    assert controller.apply_settings_profile_to_source("long_wav", "default")
    # Transcribing.
    controller.transcribe()

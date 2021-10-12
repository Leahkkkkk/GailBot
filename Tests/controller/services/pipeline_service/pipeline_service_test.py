# Standard library imports
from typing import Dict
import pytest
# Local imports
from Src.Components.io import IO
from Src.Components.controller.services.organizer_service import GailBotSettings, \
    GBSettingAttrs, Source
from Src.Components.controller.services import FileSystemService, OrganizerService,\
    SourceDetails, SettingsDetails, PipelineService, PipelineServiceSummary
from Tests.controller.vardefs import *

############################### GLOBALS #####################################

# WS_DIR_PATH = "TestData/workspace/temp_ws"
# WAV_FILE_PATH = "TestData/media/test2a.wav"
# MP3_FILE_PATH = "TestData/media/sample1.mp3"
# MOV_FILE_PATH = "TestData/media/sample_video_conversation.mov"
# MIXED_DIR_PATH = "TestData/media/audio_video_conversation"
# RESULT_DIR_PATH = "TestData/workspace/transcription_results"
# ANALYSIS_PLUGINS_CONFIG = "TestData/plugins/pipeline_service_test/analysis_config.json"
# FORMAT_PLUGINS_CONFIG = "TestData/plugins/pipeline_service_test/format_config.json"
# NUM_THREADS = 4

############################### SETUP #####################################


def initialize_organizer_service() -> OrganizerService:
    fs_service = FileSystemService()
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    service = OrganizerService(fs_service)
    return service


def obtain_settings_profile_data() -> Dict:
    return {
        GBSettingAttrs.engine_type: "watson",
        GBSettingAttrs.watson_api_key: "MSgOPTS9CvbADe49nEg4wm8_gxeRuf4FGUmlHS9QqAw3",
        GBSettingAttrs.watson_language_customization_id: "41e54a38-2175-45f4-ac6a-1c11e42a2d54",
        GBSettingAttrs.watson_base_language_model: "en-US_BroadbandModel",
        GBSettingAttrs.watson_region: "dallas",
        GBSettingAttrs.analysis_plugins_to_apply: ['tcu_analysis', 'second_analysis'],
        GBSettingAttrs.output_format: "normal"}


def add_source(organizer_service: OrganizerService, source_name: str,
               source_path: str, result_dir_path: str) -> None:
    organizer_service.add_source(source_name, source_path, result_dir_path)
    organizer_service.create_new_settings_profile(
        "s1", obtain_settings_profile_data())
    organizer_service.apply_settings_profile_to_source(source_name, "s1")


@pytest.fixture(scope='session', autouse=True)
def reset_workspace() -> None:
    io = IO()
    io.delete(RESULT_DIR_PATH)
    io.create_directory(RESULT_DIR_PATH)

########################## TEST DEFINITIONS ##################################


def test_add_source() -> None:
    """
    Tests:
        1. Add a source.
        2. Add a source with repeated identifier.
    """
    organizer_service = initialize_organizer_service()
    service = PipelineService(NUM_THREADS)
    add_source(organizer_service, "file", MP3_FILE_PATH, RESULT_DIR_PATH)
    add_source(organizer_service, "dir", MIXED_DIR_PATH, RESULT_DIR_PATH)
    sources = organizer_service.get_configured_sources()
    for source_name, source in sources.items():
        assert service.add_source(source_name, source)
        assert not service.add_source(source_name, source)


def test_add_sources() -> None:
    """
    Tests:
        1. Add multiple sources.
    """
    organizer_service = initialize_organizer_service()
    service = PipelineService(NUM_THREADS)
    add_source(organizer_service, "file", MP3_FILE_PATH, RESULT_DIR_PATH)
    add_source(organizer_service, "dir", MIXED_DIR_PATH, RESULT_DIR_PATH)
    sources = organizer_service.get_configured_sources()
    assert service.add_sources(sources)


def test_remove_source() -> None:
    """
    Tests:
        1. Remove a valid source.
        2. Remove an invalid source.
    """
    organizer_service = initialize_organizer_service()
    service = PipelineService(NUM_THREADS)
    add_source(organizer_service, "file", MP3_FILE_PATH, RESULT_DIR_PATH)
    add_source(organizer_service, "dir", MIXED_DIR_PATH, RESULT_DIR_PATH)
    sources = organizer_service.get_configured_sources()
    service.add_sources(sources)
    assert service.remove_source("file")
    assert service.remove_source("dir")
    assert not service.remove_source("invalid")


def test_register_analysis_plugins() -> None:
    """
    Tests:
        1. Register some plugins.
        2. Register from invalid path.
    """
    service = PipelineService(NUM_THREADS)
    assert len(service.register_analysis_plugins(ANALYSIS_PLUGINS_CONFIG)) > 0
    assert len(service.register_analysis_plugins("invalid")) == 0


def test_register_format() -> None:
    """
    Tests:
        1. Register a valid format.
        2. Register from invalid path.
    """
    service = PipelineService(NUM_THREADS)
    assert service.register_format(FORMAT_PLUGINS_CONFIG)[0] != ""
    assert service.register_format("invalid")[0] == None

# TODO: These tests need to be  uncommented!!!!!
# def test_start_audio() -> None:
#     organizer_service = initialize_organizer_service()
#     service = PipelineService(NUM_THREADS)
#     add_source(organizer_service, "file", MP3_FILE_PATH, RESULT_DIR_PATH)
#     sources = organizer_service.get_configured_sources()
#     service.add_sources(sources)
#     service.start()


# def test_start_video() -> None:
#     organizer_service = initialize_organizer_service()
#     service = PipelineService(NUM_THREADS)
#     add_source(organizer_service, "mixed", MIXED_DIR_PATH, RESULT_DIR_PATH)
#     sources = organizer_service.get_configured_sources()
#     service.add_sources(sources)
#     service.start()


# def test_start_multiple() -> None:
#     organizer_service = initialize_organizer_service()
#     service = PipelineService(NUM_THREADS)
#     add_source(organizer_service, "file_multiple",
#                MP3_FILE_PATH, RESULT_DIR_PATH)
#     add_source(organizer_service, "mixed_multiple",
#                MIXED_DIR_PATH, RESULT_DIR_PATH)
#     sources = organizer_service.get_configured_sources()
#     service.add_sources(sources)
#     service.start()


# def test_start_with_audio_plugins_only() -> None:
#     organizer_service = initialize_organizer_service()
#     service = PipelineService(NUM_THREADS)
#     add_source(organizer_service, "file", MP3_FILE_PATH, RESULT_DIR_PATH)
#     sources = organizer_service.get_configured_sources()
#     assert len(service.register_analysis_plugins(ANALYSIS_PLUGINS_CONFIG)) > 0
#     service.add_sources(sources)
#     service.start()


# def test_start_with_format_only() -> None:
#     organizer_service = initialize_organizer_service()
#     service = PipelineService(NUM_THREADS)
#     add_source(organizer_service, "file", MP3_FILE_PATH, RESULT_DIR_PATH)
#     sources = organizer_service.get_configured_sources()
#     service.register_format(FORMAT_PLUGINS_CONFIG)
#     service.add_sources(sources)
#     service.start()


# def test_start_analysis_and_format_plugins() -> None:
#     organizer_service = initialize_organizer_service()
#     service = PipelineService(NUM_THREADS)
#     add_source(organizer_service, "file", MP3_FILE_PATH, RESULT_DIR_PATH)
#     sources = organizer_service.get_configured_sources()
#     service.register_analysis_plugins(ANALYSIS_PLUGINS_CONFIG)
#     service.register_format(FORMAT_PLUGINS_CONFIG)
#     service.add_sources(sources)
#     print(service.start())


def test_get_analysis_plugin_names() -> None:
    """
    Tests:
        1. Check the analysis plugin names.
    """
    service = PipelineService(NUM_THREADS)
    service.register_analysis_plugins(ANALYSIS_PLUGINS_CONFIG)
    assert len(service.get_analysis_plugin_names()) > 0


def test_get_format_names() -> None:
    """
    Tests:
        1. Check after adding a format
    """
    service = PipelineService(NUM_THREADS)
    service.register_format(FORMAT_PLUGINS_CONFIG)
    assert len(service.get_format_names()) == 1


def test_get_format_plugin_names() -> None:
    """
    Tests:
        1. Check for valid format.
        2. Check for invalid format.
    """
    service = PipelineService(NUM_THREADS)
    name, plugins = service.register_format(FORMAT_PLUGINS_CONFIG)
    service.get_format_plugin_names(name) == plugins

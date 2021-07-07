# Standard library imports
from typing import Dict
# Local imports
from Src.Components.controller.services.gb_settings import GailBotSettings, GBSettingAttrs
from Src.Components.controller.services import FileSystemService,OrganizerService,\
    SourceDetails,SettingsDetails, PipelineService, PipelineServiceSummary, organizer_service
from Src.Components.controller.services.source import Source


############################### GLOBALS #####################################

WS_DIR_PATH = "TestData/workspace/temp_ws"
WAV_FILE_PATH = "TestData/media/test2a.wav"
MP3_FILE_PATH = "TestData/media/sample1.mp3"
MOV_FILE_PATH = "TestData/media/sample_video_conversation.mov"
MIXED_DIR_PATH = "TestData/media/audio_video_conversation"
RESULT_DIR_PATH = "TestData/workspace/transcription_results"
ANALYSIS_PLUGINS_CONFIG = "TestData/plugins/pipeline_service_test/analysis_config.json"
FORMAT_PLUGINS_CONFIG = "TestData/plugins/pipeline_service_test/format_config.json"
NUM_THREADS = 4

############################### SETUP #####################################

def initialize_organizer_service() -> OrganizerService:
    fs_service = FileSystemService()
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    service = OrganizerService(fs_service)
    return service

def obtain_settings_profile_data() -> Dict:
    return {
        GBSettingAttrs.engine_type : "watson",
        GBSettingAttrs.watson_api_key : "MSgOPTS9CvbADe49nEg4wm8_gxeRuf4FGUmlHS9QqAw3",
        GBSettingAttrs.watson_language_customization_id : "41e54a38-2175-45f4-ac6a-1c11e42a2d54",
        GBSettingAttrs.watson_base_language_model : "en-US_BroadbandModel",
        GBSettingAttrs.watson_region : "dallas",
        GBSettingAttrs.analysis_plugins_to_apply : ["tcu_analysis","second_analysis"],
        GBSettingAttrs.output_format : "normal"}

########################## TEST DEFINITIONS ##################################

def test_add_source() -> None:
    """
    Tests:
        1. Add a source.
        2. Add a source with repeated identifier.
    """
    organizer_service = initialize_organizer_service()
    service = PipelineService(NUM_THREADS)
    organizer_service.add_source("file",MP3_FILE_PATH,RESULT_DIR_PATH)
    organizer_service.add_source("dir",MIXED_DIR_PATH,RESULT_DIR_PATH)
    organizer_service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    organizer_service.apply_settings_profile_to_sources(["file","dir"],"s1")
    sources = organizer_service.get_configured_sources()
    for source_name, source in sources.items():
        assert service.add_source(source_name, source)
        assert not service.add_source(source_name, source)
    organizer_service.remove_sources(["file","dir"])

def test_add_sources() -> None:
    """
    Tests:
        1. Add multiple sources.
    """
    organizer_service = initialize_organizer_service()
    service = PipelineService(NUM_THREADS)
    organizer_service.add_source("file",MP3_FILE_PATH,RESULT_DIR_PATH)
    organizer_service.add_source("dir",MIXED_DIR_PATH,RESULT_DIR_PATH)
    organizer_service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    organizer_service.apply_settings_profile_to_sources(["file","dir"],"s1")
    sources = organizer_service.get_configured_sources()
    assert service.add_sources(sources)
    organizer_service.remove_sources(["file","dir"])

def test_remove_source() -> None:
    """
    Tests:
        1. Remove a valid source.
        2. Remove an invalid source.
    """
    organizer_service = initialize_organizer_service()
    service = PipelineService(NUM_THREADS)
    organizer_service.add_source("file",MP3_FILE_PATH,RESULT_DIR_PATH)
    organizer_service.add_source("dir",MIXED_DIR_PATH,RESULT_DIR_PATH)
    organizer_service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    organizer_service.apply_settings_profile_to_sources(["file","dir"],"s1")
    service.add_sources(organizer_service.get_configured_sources())
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

def test_start_multiple() -> None:
    """
    Tests:
        1. Start the transcription service with multiple inputs.
    """
    organizer_service = initialize_organizer_service()
    service = PipelineService(NUM_THREADS)
    # Adding plugins
    service.register_analysis_plugins(ANALYSIS_PLUGINS_CONFIG)
    service.register_format(FORMAT_PLUGINS_CONFIG)
    assert organizer_service.add_source("file",MP3_FILE_PATH,RESULT_DIR_PATH)
    # assert organizer_service.add_source("mixed",MIXED_DIR_PATH,RESULT_DIR_PATH)
    # assert organizer_service.add_source("mov",MOV_FILE_PATH,RESULT_DIR_PATH)
    assert organizer_service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    assert organizer_service.apply_settings_profile_to_source("file","s1")
    # assert organizer_service.apply_settings_profile_to_source("mixed","s1")
    # assert organizer_service.apply_settings_profile_to_source("mov","s1")
    assert service.add_sources(organizer_service.get_configured_sources())
    summary = service.start()
    print(summary)

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

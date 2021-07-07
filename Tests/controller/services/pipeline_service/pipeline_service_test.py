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
        GBSettingAttrs.analysis_plugins_to_apply : ["second_analysis"],
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
    pass

def test_register_format() -> None:
    """
    Tests:
        1. Register a valid format.
        2. Register from invalid path.
    """
    pass

def test_start_audio_source() -> None:
    """
    Tests:
        1. Start the transcription service.
    """
    organizer_service = initialize_organizer_service()
    service = PipelineService(NUM_THREADS)
    assert organizer_service.add_source("file",MP3_FILE_PATH,RESULT_DIR_PATH)
    assert organizer_service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    assert organizer_service.apply_settings_profile_to_source("file","s1")
    assert service.add_sources(organizer_service.get_configured_sources())
    summary = service.start()
    print(summary)


def test_start_audio_video() -> None:
    """
    Tests:
        1. Start the transcription service.
    """
    organizer_service = initialize_organizer_service()
    service = PipelineService(NUM_THREADS)
    assert organizer_service.add_source("mov",MOV_FILE_PATH,RESULT_DIR_PATH)
    assert organizer_service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    assert organizer_service.apply_settings_profile_to_source("mov","s1")
    assert service.add_sources(organizer_service.get_configured_sources())
    summary = service.start()
    print(summary)


def test_start_audio_mixed() -> None:
    """
    Tests:
        1. Start the transcription service.
    """
    organizer_service = initialize_organizer_service()
    service = PipelineService(NUM_THREADS)
    assert organizer_service.add_source("mixed",MIXED_DIR_PATH,RESULT_DIR_PATH)
    assert organizer_service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    assert organizer_service.apply_settings_profile_to_source("mixed","s1")
    assert service.add_sources(organizer_service.get_configured_sources())
    summary = service.start()
    print(summary)

def test_audio_JP() -> None:
    pass


def test_get_analysis_plugin_names() -> None:
    """
    Tests:
        1. Check the analysis plugin names.
    """
    pass

def test_get_format_names() -> None:
    """
    Tests:
        1. Check after adding a format
    """
    pass

def test_get_format_plugin_names() -> None:
    """
    Tests:
        1. Check for valid format.
        2. Check for invalid format.
    """
    pass

def test_is_source() -> None:
    """
    Tests:
        1. Check for valid source.
        2. Check for invalid source.
    """
    pass

def test_get_source() -> None:
    """
    Tests:
        1. Obtain a valid identifier.
        2. Obtain an invalid identifier.
    """
    pass

def test_get_sources() -> None:
    """
    Tests:
        1. Obtain all sources.
    """
    pass
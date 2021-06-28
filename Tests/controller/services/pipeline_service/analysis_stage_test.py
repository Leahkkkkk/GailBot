# Standard library imports
from typing import Dict, Any, List
# Local imports
from Src.Components.controller.services import OrganizerService, FileSystemService,\
                                                GBSettingAttrs
from Src.Components.controller.services.pipeline_service \
    import AnalysisStage, Transcribable
from Src.Components.organizer import Conversation
from Src.Components.engines import Utterance, UtteranceAttributes
from Src.Components.io import IO
# Third party imports

############################### GLOBALS #####################################

WS_DIR_PATH = "TestData/workspace/fs_workspace"
WAV_FILE_PATH = "TestData/media/test.wav"
MP3_FILE_PATH = "TestData/media/sample1.mp3"
CONV_DIR_PATH = "TestData/media/conversation"
MIXED_CONV_DIR_PATH = "TestData/media/audio_video_conversation"
SMALL_CONV_DIR_PATH = "TestData/media/small_conversation"
RESULT_DIR_PATH = "TestData/workspace/dir_2"
MOV_FILE_PATH = "TestData/media/sample_video_conversation.mov"
PLUGINS_DIR = "Tests/analyzer/plugins"
NUM_DIR_PLUGINS = 2

############################### SETUP ########################################


def cleanup_sources() -> None:
    io = IO()
    dir_paths = io.paths_of_subdirectories(WS_DIR_PATH + "/source_ws")[1]
    for path in dir_paths:
        io.delete(path)

def obtain_settings_profile_data() -> Dict[str,Any]:
    return {
        GBSettingAttrs.engine_type : "watson",
        GBSettingAttrs.watson_api_key : "MSgOPTS9CvbADe49nEg4wm8_gxeRuf4FGUmlHS9QqAw3",
        GBSettingAttrs.watson_language_customization_id : "41e54a38-2175-45f4-ac6a-1c11e42a2d54",
        GBSettingAttrs.watson_base_language_model : "en-US_BroadbandModel",
        GBSettingAttrs.watson_region : "dallas"
    }

def initialize_conversation(source_path : str) -> Conversation:
    fs_service = FileSystemService()
    io = IO()
    assert fs_service.configure_from_workspace_path(WS_DIR_PATH)
    organizer_service = OrganizerService(fs_service)
    assert organizer_service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    source_name = io.get_name(source_path)
    assert organizer_service.add_source(source_name,source_path,RESULT_DIR_PATH)
    assert organizer_service.apply_settings_profile_to_source(source_name,"s1")
    conv = organizer_service.get_configured_source_conversation(source_name)
    assert type(conv) == Conversation
    return conv

def initialize_transcribable(conversation : Conversation) -> Transcribable:
    return Transcribable(
        conversation.get_conversation_name(),conversation)

def transcribable_from_source(source_path : str) -> Transcribable:
    return initialize_transcribable(initialize_conversation(source_path))

########################## TEST DEFINITIONS ##################################


def test_register_plugins_from_directory() -> None:
    """
    Tests:
        1. Register from valid directory.
        2. Register from invalid directory.
    """
    stage = AnalysisStage()
    assert stage.register_plugins_from_directory(PLUGINS_DIR) == NUM_DIR_PLUGINS
    assert stage.register_plugins_from_directory("invalid") == 0

def test_add_transcribable_audio_source() -> None:
    """
    Tests:
        1. Set an audio file source.
    """
    stage = AnalysisStage()
    transcribable = transcribable_from_source(MP3_FILE_PATH)
    assert stage.add_transcribable(transcribable)
    cleanup_sources()

def test_add_transcribable_video_source() -> None:
    """
    Tests:
        1. Set a video file source.
    """
    stage = AnalysisStage()
    transcribable = transcribable_from_source(MOV_FILE_PATH)
    assert stage.add_transcribable(transcribable)
    cleanup_sources()

def test_add_transcribable_mixed_source() -> None:
    """
    Tests:
        1. Set a directory source with both audio and video files.
        2. Set an invalid directory path.
    """
    stage = AnalysisStage()
    transcribable = transcribable_from_source(MIXED_CONV_DIR_PATH)
    assert stage.add_transcribable(transcribable)
    cleanup_sources()

def test_add_transcribables() -> None:
    """
    Tests:
        1. Add multiple transcribables.
    """
    stage = AnalysisStage()
    transcribable_1 = transcribable_from_source(MP3_FILE_PATH)
    transcribable_2 = transcribable_from_source(MOV_FILE_PATH)
    transcribable_3 = transcribable_from_source(MIXED_CONV_DIR_PATH)
    assert stage.add_transcribables(
        [transcribable_1,transcribable_2,transcribable_3])
    cleanup_sources()

def test_analyze() -> None:
    stage = AnalysisStage()
    stage.register_plugins_from_directory(PLUGINS_DIR)
    transcribable_1 = transcribable_from_source(MP3_FILE_PATH)
    transcribable_2 = transcribable_from_source(MOV_FILE_PATH)
    transcribable_3 = transcribable_from_source(MIXED_CONV_DIR_PATH)
    assert stage.add_transcribables(
        [transcribable_1,transcribable_2,transcribable_3])
    summaries = stage.analyze()
    names = [transcribable_1.identifier, transcribable_2.identifier,
        transcribable_3.identifier]
    assert all([name in summaries.keys() for name in names])


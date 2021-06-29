# Standard library imports
from typing import Dict, Any
# Local imports
from Src.Components.controller.services import OrganizerService, FileSystemService,\
                                                GBSettingAttrs
from Src.Components.controller.services.pipeline_service \
    import AnalysisStage, TranscriptionStage
from Src.Components.organizer import Conversation
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
PLUGINS_DIR = "TestData/plugins/random_plugins"
NUM_DIR_PLUGINS = 2
ANALYSIS_PLUGINS_DIR = "TestData/plugins/analysis_plugins"

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

########################## TEST DEFINITIONS ##################################

# def test_register_plugins_from_directory() -> None:
#     """
#     Tests:
#         1. Register from valid directory.
#         2. Register from invalid directory.
#     """
#     stage = AnalysisStage()
#     assert stage.register_plugins_from_directory(PLUGINS_DIR) == NUM_DIR_PLUGINS
#     assert stage.register_plugins_from_directory("invalid") == 0

def test_analyze_audio_source() -> None:
    """
    Tests:
        1. Analyze with valid plugins.
    """
    # Conversations
    c1 = initialize_conversation(MP3_FILE_PATH)
    # Running the transcriptionStage
    transcription_stage = TranscriptionStage()
    conversations = {
        c1.get_conversation_name() : c1
    }
    analysis_stage = AnalysisStage()
    assert analysis_stage.register_plugins_from_directory(ANALYSIS_PLUGINS_DIR) > 0
    results = transcription_stage.generate_utterances(conversations)
    results = analysis_stage.analyze(
        conversations,results)
    print(results)

def test_analyze_video_source() -> None:
    """
    Tests:
        1. Analyze with valid plugins.
    """
    # Conversations
    c1 = initialize_conversation(MOV_FILE_PATH)
    # Running the transcriptionStage
    transcription_stage = TranscriptionStage()
    conversations = {
        c1.get_conversation_name() : c1
    }
    analysis_stage = AnalysisStage()
    assert analysis_stage.register_plugins_from_directory(ANALYSIS_PLUGINS_DIR) > 0
    results = transcription_stage.generate_utterances(conversations)
    results = analysis_stage.analyze(
        conversations,results)
    print(results)

def test_analyze_mixed_source() -> None:
    """
    Tests:
        1. Analyze with valid plugins.
    """
    # Conversations
    c1 = initialize_conversation(MIXED_CONV_DIR_PATH)
    # Running the transcriptionStage
    transcription_stage = TranscriptionStage()
    conversations = {
        c1.get_conversation_name() : c1
    }
    analysis_stage = AnalysisStage()
    assert analysis_stage.register_plugins_from_directory(ANALYSIS_PLUGINS_DIR) > 0
    results = transcription_stage.generate_utterances(conversations)
    results = analysis_stage.analyze(
        conversations,results)
    print(results)
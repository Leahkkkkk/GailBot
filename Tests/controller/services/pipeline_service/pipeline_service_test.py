# Standard library imports
from typing import List, Dict, Any
from Src.Components.controller import services
# Local imports
from Src.Components.controller.services import TranscriptionPipelineService, \
    OrganizerService, FileSystemService, TranscriptionStatus, GBSettingAttrs, \
    PipelineServiceSummary
from Src.Components.organizer import Conversation
from Src.Components.engines import Utterance, UtteranceAttributes
from Src.Components.io import IO

############################### GLOBALS #####################################

WS_DIR_PATH = "TestData/workspace/fs_workspace"
WAV_FILE_PATH = "TestData/media/test.wav"
MP3_FILE_PATH = "TestData/media/sample1.mp3"
CONV_DIR_PATH = "TestData/media/conversation"
SMALL_CONV_DIR_PATH = "TestData/media/small_conversation"
RESULT_DIR_PATH = "TestData/workspace/dir_2"
MOV_FILE_PATH = "TestData/media/sample_video_conversation.mov"
PLUGINS_DIR_PATH = "Tests/analyzer/plugins"
MIXED_CONV_DIR_PATH = "TestData/media/audio_video_conversation"

############################### SETUP #######################################

def obtain_settings_profile_data() -> Dict[str,Any]:
    return {
        GBSettingAttrs.engine_type : "watson",
        GBSettingAttrs.watson_api_key : "MSgOPTS9CvbADe49nEg4wm8_gxeRuf4FGUmlHS9QqAw3",
        GBSettingAttrs.watson_language_customization_id : "41e54a38-2175-45f4-ac6a-1c11e42a2d54",
        GBSettingAttrs.watson_base_language_model : "en-US_BroadbandModel",
        GBSettingAttrs.watson_region : "dallas"
    }

def create_conversation(source_path : str) -> Conversation:
    io = IO()
    source_name = io.get_name(source_path)
    fs_service = FileSystemService()
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    service = OrganizerService(fs_service)
    service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    service.add_source(source_name,source_path,RESULT_DIR_PATH)
    service.apply_settings_profile_to_source(source_name,"s1")
    return service.get_configured_source_conversation(source_name)

def cleanup_sources() -> None:
    io = IO()
    dir_paths = io.paths_of_subdirectories(WS_DIR_PATH + "/source_ws")[1]
    for path in dir_paths:
        io.delete(path)

def print_utterance_map(utterance_map : Dict[str,List[Utterance]]) -> None:
    for name, utterances in utterance_map.items():
        print("source name: {}".format(name))
        print_utterances(utterances)

def print_utterances(utterances : List[Utterance]) -> None:
    for utterance in utterances:
        print_utterance(utterance)

def print_utterance(utterance : Utterance) -> None:
    print("{}: {} {}_{}".format(
        utterance.get(UtteranceAttributes.speaker_label)[1],
        utterance.get(UtteranceAttributes.transcript)[1],
        utterance.get(UtteranceAttributes.start_time)[1],
        utterance.get(UtteranceAttributes.end_time)[1]))

########################## TEST DEFINITIONS ##################################

def test_register_analysis_plugins_from_directory() -> None:
    """
    Tests:
        1. Register from a valid directory.
        2/ Register from an invalid directory.
    """
    service = TranscriptionPipelineService()
    assert service.register_analysis_plugins_from_directory(PLUGINS_DIR_PATH) \
        == 2
    assert service.register_analysis_plugins_from_directory("invalid") == 0

def test_add_conversation() -> None:
    """
    Tests:
        1. Add a conversation.
        2. Add a conversation that already exists.
    """
    service = TranscriptionPipelineService()
    assert service.add_conversation(create_conversation(SMALL_CONV_DIR_PATH))
    assert not service.add_conversation(create_conversation(SMALL_CONV_DIR_PATH))
    cleanup_sources()

def test_add_conversations() -> None:
    """
    Tests:
        1. Add multiple sources.
    """
    service = TranscriptionPipelineService()
    c1 = create_conversation(SMALL_CONV_DIR_PATH)
    c2 = create_conversation(WAV_FILE_PATH)
    assert service.add_conversations([c1,c2])
    cleanup_sources()

def test_remove_conversation() -> None:
    """
    Tests:
        1. Remove invalid conversation.
        2. Remove valid conversations.
    """
    service = TranscriptionPipelineService()
    conversation = create_conversation(MP3_FILE_PATH)
    service.add_conversation(conversation)
    assert service.remove_conversation(conversation.get_conversation_name())
    assert not service.remove_conversation("invalid")
    cleanup_sources()

def test_clear_conversation() -> None:
    """
    Tests:
        1. Remove all conversations.
    """
    service = TranscriptionPipelineService()
    c1 = create_conversation(MP3_FILE_PATH)
    c2 = create_conversation(WAV_FILE_PATH)
    service.add_conversation(c1)
    service.add_conversation(c2)
    assert service.clear_conversations()
    cleanup_sources()

def test_start_pipeline_service_audio() -> None:
    """
    Tests:
        1. Start the pipeline service with a single audio source converstion.
    """
    service = TranscriptionPipelineService()
    service.register_analysis_plugins_from_directory(PLUGINS_DIR_PATH)
    c1 = create_conversation(MP3_FILE_PATH)
    service.add_conversations([c1])
    summary = service.start_pipeline_service()
    print(summary)
    assert len(summary.successful_conversations) > 0

def test_start_pipeline_service_video() -> None:
    """
    Tests:
        1. Start the pipeline service with a single video source converstion.
    """
    service = TranscriptionPipelineService()
    service.register_analysis_plugins_from_directory(PLUGINS_DIR_PATH)
    c1 = create_conversation(MOV_FILE_PATH)
    service.add_conversations([c1])
    summary = service.start_pipeline_service()
    print(summary)
    assert len(summary.successful_conversations) > 0

def test_start_pipeline_service_mixed() -> None:
    """
    Tests:
        1. Start the pipeline service with a single mixed source converstion.
    """
    service = TranscriptionPipelineService()
    service.register_analysis_plugins_from_directory(PLUGINS_DIR_PATH)
    c1 = create_conversation(MIXED_CONV_DIR_PATH)
    service.add_conversations([c1])
    summary = service.start_pipeline_service()
    print(summary)
    assert len(summary.successful_conversations) > 0

def test_start_pipeline_service_multiple() -> None:
    service = TranscriptionPipelineService()
    service.register_analysis_plugins_from_directory(PLUGINS_DIR_PATH)
    c1 = create_conversation(MIXED_CONV_DIR_PATH)
    c2 = create_conversation(MP3_FILE_PATH)
    c3 = create_conversation(MOV_FILE_PATH)
    service.add_conversations([c1,c2,c3])
    summary = service.start_pipeline_service()
    print(summary)
    assert len(summary.successful_conversations) > 0

def test_is_conversation() -> None:
    """
    Tests:
        1. Check valid conversation.
        2. Check invalid conversation.
    """
    service = TranscriptionPipelineService()
    c1 = create_conversation(MIXED_CONV_DIR_PATH)
    service.add_conversation(c1)
    assert service.is_conversation(c1.get_conversation_name())
    assert not service.is_conversation("invalid")

def test_get_all_conversations() -> None:
    """
    Tests:
        1. Get all the conversations.
    """
    service = TranscriptionPipelineService()
    c1 = create_conversation(MIXED_CONV_DIR_PATH)
    c2 = create_conversation(MP3_FILE_PATH)
    c3 = create_conversation(MOV_FILE_PATH)
    service.add_conversations([c1,c2,c3])
    names = [c1.get_conversation_name(), c2.get_conversation_name(),
        c3.get_conversation_name()]
    assert all([name in service.get_all_conversations().keys() \
        for name in names])


# Standard library imports
from typing import Dict, Any, List
# Local imports
from Src.Components.controller.services import OrganizerService, FileSystemService,\
            GBSettingAttrs
from Src.Components.organizer import Conversation
from Src.Components.io import IO
from Src.Components.controller.services.pipeline_service import \
    PipelineServicePayload
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

def test_add_conversation() -> None:
    """
    Tests:
        1. Add a conversation.
    """
    payload = PipelineServicePayload()
    conversation = initialize_conversation(MP3_FILE_PATH)
    assert payload.add_conversation(conversation)
    cleanup_sources()

def test_add_conversations() -> None:
    """
    Tests:
        1. Add multiple conversations.
    """
    payload = PipelineServicePayload()
    c1 = initialize_conversation(MP3_FILE_PATH)
    c2 = initialize_conversation(MOV_FILE_PATH)
    assert payload.add_conversations([c1,c2])
    cleanup_sources()

def test_remove_conversation() -> None:
    """
    Tests:
        1. Remove a valid conversation
        2. Remove an invalid conversation.
    """
    payload = PipelineServicePayload()
    c1 = initialize_conversation(MP3_FILE_PATH)
    c2 = initialize_conversation(MOV_FILE_PATH)
    payload.add_conversations([c1,c2])
    assert payload.remove_conversation(c1.get_conversation_name())
    assert not payload.remove_conversation("invalid")

def test_clear_conversations() -> None:
    """
    Tests:
        1. Clear all conversations
    """
    payload = PipelineServicePayload()
    c1 = initialize_conversation(MP3_FILE_PATH)
    c2 = initialize_conversation(MOV_FILE_PATH)
    payload.add_conversations([c1,c2])
    assert payload.clear_conversations()

def test_is_conversation() -> None:
    """
    Tests:
        1. Check a valid conversation.
        2. Check an invalid conversation.
    """
    payload = PipelineServicePayload()
    c1 = initialize_conversation(MP3_FILE_PATH)
    c2 = initialize_conversation(MOV_FILE_PATH)
    payload.add_conversations([c1,c2])
    assert payload.is_conversation(c1.get_conversation_name())
    assert payload.is_conversation(c2.get_conversation_name())
    assert not payload.is_conversation("invalid")

def test_get_conversations() -> None:
    """
    Tests:
        1. Check added conversations.
    """
    payload = PipelineServicePayload()
    c1 = initialize_conversation(MP3_FILE_PATH)
    c2 = initialize_conversation(MOV_FILE_PATH)
    payload.add_conversations([c1,c2])
    assert c1.get_conversation_name() in payload.get_conversations()
    assert c2.get_conversation_name() in payload.get_conversations()

def test_get_transcription_stage_output() -> None:
    """
    Tests:
        1. Set and get a random output.
    """
    payload = PipelineServicePayload()
    payload.set_transcription_stage_output("ts")
    assert payload.get_transcription_stage_output() == "ts"

def test_get_analysis_stage_output() -> None:
    """
    Tests:
        1. Set and get a random output
    """
    payload = PipelineServicePayload()
    payload.set_analysis_stage_output('as')
    payload.get_analysis_stage_output() == "as"

def test_get_format_stage_output() -> None:
    """
    Tests:
        1. Set and get a random output.
    """
    payload = PipelineServicePayload()
    payload.set_format_stage_output("fs")
    assert payload.get_format_stage_output() == "fs"

def test_set_transcription_stage_output() -> None:
    payload = PipelineServicePayload()
    payload.set_transcription_stage_output("ts")

def test_set_analysis_stage_output() -> None:
    payload = PipelineServicePayload()
    payload.set_analysis_stage_output('as')

def test_set_formatter_stage_output() -> None:
    payload = PipelineServicePayload()
    payload.set_format_stage_output("fs")
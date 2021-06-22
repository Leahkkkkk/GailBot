# Standard library imports
from Src.Components.controller import services
from Src.Components.pipeline.pipeline import Pipeline
from typing import List, Dict, Any
# Local imports
from Src.Components.controller.services import TranscriptionPipelineService, \
    OrganizerService, TranscriptionSummary,TranscriptionStatus, FileSystemService, \
    GBSettingAttrs
from Src.Components.organizer import Conversation
from Src.Components.engines import Utterance, UtteranceAttributes
############################### GLOBALS #####################################

WS_DIR_PATH = "TestData/workspace/fs_workspace"
WAV_FILE_PATH = "TestData/media/test2a.wav"
MP3_FILE_PATH = "TestData/media/sample1.mp3"
CONV_DIR_PATH = "TestData/media/conversation"
SMALL_CONV_DIR_PATH = "TestData/media/small_conversation"
RESULT_DIR_PATH = "TestData/workspace/dir_2"


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
    source_name = source_path
    fs_service = FileSystemService()
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    service = OrganizerService(fs_service)
    service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    service.add_source(source_name,source_path,RESULT_DIR_PATH)
    service.apply_settings_profile_to_source(source_name,"s1")
    return service.get_configured_source_conversation(source_name)

def create_conversations(source_paths : List[str]) -> Dict[str,Conversation]:
    fs_service = FileSystemService()
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    service = OrganizerService(fs_service)
    service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    for i,path in enumerate(source_paths):
        source_name = "source_{}".format(i)
        service.add_source(source_name,path,RESULT_DIR_PATH)
        service.apply_settings_profile_to_source(source_name,"s1")
    return service.get_all_configured_source_conversations()

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

def test_pipeline_service_add_conversation() -> None:
    """
    Tests:
        1. Add a conversation.
        2. Add a conversation that already exists.
    """
    service = TranscriptionPipelineService()
    assert service.add_conversation(create_conversation(SMALL_CONV_DIR_PATH))
    assert not service.add_conversation(create_conversation(SMALL_CONV_DIR_PATH))
    summary = service.get_transcription_summary()
    assert summary.number_ready_to_transcribe_conversations == 1

def test_pipeline_service_add_conversations() -> None:
    """
    Tests:
        1. Add multiple conversations.
    """
    service = TranscriptionPipelineService()
    assert service.add_conversations(list(create_conversations(
        [SMALL_CONV_DIR_PATH,WAV_FILE_PATH]).values()))

def test_pipeline_service_start_transcription_pipeline() -> None:
    """
    Tests:
        1. Transcribe a single conversation.
        2. Transcribe from a directory.
        3. Transcribe with no conversations.
    """
    service = TranscriptionPipelineService()
    conversation = create_conversation(MP3_FILE_PATH)
    service.add_conversation(conversation)
    service.start_transcription_pipeline()
    assert service.get_transcription_summary().\
        number_successfully_transcribed_conversations == 1
    c2 = create_conversation(SMALL_CONV_DIR_PATH)
    assert service.add_conversation(c2)
    service.start_transcription_pipeline()
    assert c2.get_transcription_status() != TranscriptionStatus.ready
    num_successful = service.get_transcription_summary().\
        number_successfully_transcribed_conversations
    service.start_transcription_pipeline()
    assert service.get_transcription_summary().\
        number_successfully_transcribed_conversations == num_successful

def test_pipeline_service_remove_conversation() -> None:
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

def test_pipeline_service_remove_conversations() -> None:
    """
    Tests:
        1. Remove multiple conversations.
    """
    service = TranscriptionPipelineService()
    c1 = create_conversation(MP3_FILE_PATH)
    c2 = create_conversation(WAV_FILE_PATH)
    service.add_conversation(c1)
    service.add_conversation(c2)
    assert service.remove_conversations(
        [c1.get_conversation_name(),c2.get_conversation_name()])

def test_pipeline_service_clear_conversations() -> None:
    """
    Tests:
        1. Remove all conversations.
    """
    service = TranscriptionPipelineService()
    c1 = create_conversation(MP3_FILE_PATH)
    c2 = create_conversation(WAV_FILE_PATH)
    service.add_conversation(c1)
    service.add_conversation(c2)
    service.clear_conversations()
    service.get_transcription_summary().\
        number_ready_to_transcribe_conversations == 0

def test_pipeline_service_get_transcription_summary() -> None:
    """
    Tests:
        1. Obtain the summary.
    """
    service = TranscriptionPipelineService()
    assert type(service.get_transcription_summary()) == TranscriptionSummary

def test_pipeline_service_is_added_conversation() -> None:
    """
    Tests:
        1. Check if an added conversation exists.
        2. Check if an invalid conversation exists.
    """
    service = TranscriptionPipelineService()
    c1 = create_conversation(MP3_FILE_PATH)
    service.add_conversation(c1)
    assert service.is_added_conversation(c1.get_conversation_name())
    service.remove_conversation(c1.get_conversation_name())
    assert not service.is_added_conversation(c1.get_conversation_name())

def test_pipeline_service_get_successfully_transcribed_conversations() -> None:
    """
    Tests:
        1. Obtain conversations that were successfully tanscribed.
    """
    service = TranscriptionPipelineService()
    assert len(service.get_successfully_transcribed_conversations().values()) == 0
    c1 = create_conversation(MP3_FILE_PATH)
    service.add_conversation(c1)
    service.start_transcription_pipeline()
    assert len(service.get_successfully_transcribed_conversations().values()) == 1

def test_pipeline_service_get_unsuccessfully_transcribed_conversations() -> None:
    """
    Tests:
        1. Get unsuccessfully transcribed conversations.
    """
    service = TranscriptionPipelineService()
    assert len(service.get_unsuccessfully_transcribed_conversations().values()) == 0
    c1 = create_conversation(WAV_FILE_PATH)
    service.add_conversation(c1)
    service.start_transcription_pipeline()
    assert len(service.get_unsuccessfully_transcribed_conversations().values()) == 1

def test_pipeline_service_get_ready_to_transcribe_conversations() -> None:
    """
    Tests:
        1. Get conversations that are ready to transcribe.
    """
    service = TranscriptionPipelineService()
    assert len(service.get_ready_to_transcribe_conversations().values()) == 0
    c1 = create_conversation(MP3_FILE_PATH)
    service.add_conversation(c1)
    service.start_transcription_pipeline()
    service.add_conversation(create_conversation(SMALL_CONV_DIR_PATH))
    assert len(service.get_ready_to_transcribe_conversations().values()) == 1
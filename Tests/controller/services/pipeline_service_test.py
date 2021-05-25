# Standard library imports
from typing import List
# Local imports
from Src.Components.controller.services import TranscriptionPipelineService, \
    OrganizerService, TranscriptionSummary,TranscriptionStatus
from Src.Components.organizer import Conversation
from Src.Components.engines import Utterance, UtteranceAttributes
############################### GLOBALS #####################################

TEMP_WS_PATH = "TestData/workspace"
SETTINGS_DIR_PATH = "TestData/configs/settings"
WAV_FILE_PATH = "TestData/media/test2a.wav"
MP3_FILE_PATH = "TestData/media/sample1.mp3"
CONV_DIR_PATH = "TestData/media/conversation"
SMALL_CONV_DIR_PATH = "TestData/media/small_conversation"


############################### SETUP #######################################

def create_conversations(source_path : str) -> List[Conversation]:
    service = OrganizerService()
    assert service.set_workspace_path(SETTINGS_DIR_PATH)
    assert service.set_conversation_workspace_path(TEMP_WS_PATH)
    assert service.add_source("source",source_path,TEMP_WS_PATH,"GB")
    return service.get_all_sources_conversations()

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


# def test_pipeline_service_clear_conversations() -> None:
#     """
#     Tests:
#         1. Ensure that there are no conversations after they are cleared.
#     """
#     conversations = create_conversations(SMALL_CONV_DIR_PATH)
#     service = TranscriptionPipelineService()
#     service.add_conversations_to_transcribe(conversations)
#     service.clear_conversations()
#     assert service.get_number_all_conversations() == 0

# def test_pipeline_service_is_ready_to_transcribe() -> None:
#     """
#     Tests:
#         1. Check is not ready without any conversations.
#         2. Check is ready after conversations are added.
#     """
#     conversations = create_conversations(SMALL_CONV_DIR_PATH)
#     service = TranscriptionPipelineService()
#     assert not service.is_ready_to_transcribe()
#     service.add_conversations_to_transcribe(conversations)
#     assert service.is_ready_to_transcribe()

# def test_pipeline_service_get_transcription_summary() -> None:
#     """
#     Tests:
#         1. Obtain the summary and check its type
#     """
#     service = TranscriptionPipelineService()
#     assert type(service.get_transcription_summary()) == TranscriptionSummary

# def test_pipeline_service_get_names_successful_transcription() -> None:
#     """
#     Tests:
#         1. Ensure names of successfully transcribed conversations are returned.
#     """
#     conversations = create_conversations(MP3_FILE_PATH)
#     service = TranscriptionPipelineService()
#     assert len(service.get_names_successful_transcription()) == 0
#     service.add_conversations_to_transcribe(conversations)
#     service.start_transcription_process()
#     service.add_conversations_to_transcribe(
#         create_conversations(CONV_DIR_PATH))
#     assert len(service.get_names_successful_transcription()) == 1

# def test_pipeline_service_get_names_unsuccessful_transcription() -> None:
#     """
#     Tests:
#         1. Ensure names of unsuccessful conversations are returned.
#     """
#     service = TranscriptionPipelineService()
#     assert len(service.get_names_unsuccessful_transcription()) == 0

# def test_pipeline_service_get_names_ready_for_transcription() -> None:
#     """
#     Tests:
#         1. No names returned when no conversations added.
#         2. Names of conversations returned when they added.
#         3. No names returned after transcription.
#     """
#     conversations = create_conversations(MP3_FILE_PATH)
#     service = TranscriptionPipelineService()
#     assert len(service.get_names_ready_for_transcription()) == 0
#     service.add_conversations_to_transcribe(conversations)
#     assert len(service.get_names_ready_for_transcription()) == 1
#     service.start_transcription_process()
#     assert len(service.get_names_ready_for_transcription()) == 0

# def test_pipeline_service_get_number_successful_transcription() -> None:
#     """
#     Tests:
#         1. Ensure correct number is returned before and after transcription.
#     """
#     conversations = create_conversations(MP3_FILE_PATH)
#     service = TranscriptionPipelineService()
#     service.add_conversations_to_transcribe(conversations)
#     assert service.get_number_successful_transcription() == 0
#     service.start_transcription_process()
#     assert service.get_number_successful_transcription() == 1

# def test_pipeline_service_get_number_unsuccessful_transcription() -> None:
#     """
#     Tests:
#         1. Ensure number of unsuccessful conversations are returned.
#     """
#     service = TranscriptionPipelineService()
#     assert service.get_number_successful_transcription() == 0

# def test_pipeline_service_get_number_ready_for_transcription() -> None:
#     """
#     Tests:
#         1. Ensure correct number of ready conversations returned at all stages.
#     """
#     conversations = create_conversations(MP3_FILE_PATH)
#     service = TranscriptionPipelineService()
#     service.add_conversations_to_transcribe(conversations)
#     assert service.get_number_ready_for_transcription() == 1
#     service.start_transcription_process()
#     assert service.get_number_ready_for_transcription() == 0

# def test_pipeline_service_get_number_all_conversations() -> None:
#     """
#     Tests:
#         1. Ensure correct number is returned at all stages.
#     """
#     conversations = create_conversations(MP3_FILE_PATH)
#     service = TranscriptionPipelineService()
#     assert service.get_number_all_conversations() == 0
#     service.add_conversations_to_transcribe(conversations)
#     assert service.get_number_all_conversations() == 1
#     service.start_transcription_process()
#     service.add_conversations_to_transcribe(
#         create_conversations(WAV_FILE_PATH))
#     assert service.get_number_all_conversations() == 2

# def test_pipeline_service_get_successful_transcriptions() -> None:
#     """
#     Tests:
#         1. Get successful conversation list and check status.
#     """
#     conversations = create_conversations(MP3_FILE_PATH)
#     service = TranscriptionPipelineService()
#     service.add_conversations_to_transcribe(conversations)
#     assert len(service.get_successful_transcriptions()) == 0
#     service.start_transcription_process()
#     transcribed = service.get_successful_transcriptions()
#     for conversation in transcribed:
#         assert conversation.get_transcription_status() == \
#             TranscriptionStatus.successful


# def test_pipeline_service_get_unsuccessful_transcriptions() -> None:
#     """
#     Tests:
#         1. Get unsuccessful conversations and check status.
#     """
#     service = TranscriptionPipelineService()
#     assert len(service.get_unsuccessful_transcriptions()) == 0

# def test_pipeline_service_get_ready_transcriptions() -> None:
#     """
#     Tests:
#         1. Get ready conversations and check their status.
#     """
#     conversations = create_conversations(MP3_FILE_PATH)
#     service = TranscriptionPipelineService()
#     service.add_conversations_to_transcribe(conversations)
#     service.start_transcription_process()
#     service.add_conversations_to_transcribe(
#         create_conversations(WAV_FILE_PATH))
#     ready_conversations = service.get_ready_transcriptions()
#     for conversation in ready_conversations:
#         conversation.get_transcription_status() == TranscriptionStatus.ready

# def test_pipeline_service_get_all_conversations() -> None:
#     """
#     Tests:
#         1. Get all conversations regardless of the status.
#     """
#     conversations = create_conversations(MP3_FILE_PATH)
#     service = TranscriptionPipelineService()
#     assert len(service.get_all_conversations()) == 0
#     service.add_conversations_to_transcribe(conversations)
#     service.start_transcription_process()
#     assert len(service.get_all_conversations()) == 1
#     service.add_conversations_to_transcribe(
#         create_conversations(WAV_FILE_PATH))
#     assert len(service.get_all_conversations()) == 2

# def test_pipeline_service_add_conversations_to_transcribe() -> None:
#     """
#     Tests:
#         1. Ensure only valid conversations are added.
#     """
#     conversations = create_conversations(MP3_FILE_PATH)
#     service = TranscriptionPipelineService()
#     service.add_conversations_to_transcribe(conversations)
#     assert service.get_number_all_conversations() == 1

def test_pipeline_service_start_transcription_process() -> None:
    """
    Tests:
        1. Transcribe valid conversations
    """
    conversations = create_conversations(SMALL_CONV_DIR_PATH)
    service = TranscriptionPipelineService()
    service.add_conversations_to_transcribe(conversations)
    assert service.get_number_ready_for_transcription() == 1
    service.start_transcription_process()
    transcriptions = service.get_successful_transcriptions()
    for conversation in transcriptions:
        print("STATUS {} --> {}".format(
            conversation.get_conversation_name(),
            conversation.get_transcription_status()))
        utterance_map = conversation.get_utterances()
        for name, utterances in utterance_map.items():
            print("UTTERANCES FOR {}".format(name))
            print_utterances(utterances)


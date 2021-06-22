# Standard library imports
from typing import Dict, Any, List
# Local imports
from Src.Components.organizer import Conversation
from Src.Components.controller.services import OrganizerService, FileSystemService,\
                                                GBSettingAttrs
from Src.Components.controller.services.pipeline_service.transcription_stage \
    import TranscriptionStage
from Src.Components.engines import Engines,  Utterance, UtteranceAttributes
from Src.Components.io import IO
from Src.Components.network import Network

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

############################### SETUP #######################################

def initialize_stage() -> TranscriptionStage:
    engines = Engines(IO(), Network())
    return TranscriptionStage(engines = engines, io = IO(),num_threads= 4)

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
    conv =  organizer_service.get_configured_source_conversation(source_name)
    assert type(conv) == Conversation
    return conv

def cleanup_sources() -> None:
    io = IO()
    dir_paths = io.paths_of_subdirectories(WS_DIR_PATH + "/source_ws")[1]
    for path in dir_paths:
        io.delete(path)

def print_utterance_map(mapping : Dict[str,List[Utterance]]):
    for name, utterances in mapping.items():
        print("source name: {}".format(name),
            "number utterances {}".format(len(utterances)))
        print_utterances(utterances)

def print_utterances(utterances : List[Utterance]):
    for utterance in utterances:
        msg = "{}: {} {}_{}".format(
            utterance.get(UtteranceAttributes.speaker_label)[1],
            utterance.get(UtteranceAttributes.transcript)[1],
            utterance.get(UtteranceAttributes.start_time)[1],
            utterance.get(UtteranceAttributes.end_time)[1])
        print(msg)

########################## TEST DEFINITIONS ##################################

# TODO: Need to add tests that check for different formats of video files.

# def test_set_conversation_audio() -> None:
#     """
#     Tests:
#         1. Set a valid audio type conversation.
#     """
#     stage = initialize_stage()
#     conversation = initialize_conversation(MP3_FILE_PATH)
#     assert stage.set_conversation(conversation)
#     cleanup_sources()

# def test_set_conversation_video() -> None:
#     """
#     Tests:
#         1. Set a valid video type conversation.
#     """
#     stage = initialize_stage()
#     conversation = initialize_conversation(MOV_FILE_PATH)
#     assert stage.set_conversation(conversation)
#     cleanup_sources()

# def test_set_conversation_mixed() -> None:
#     """
#     Tests:
#         1. Set a valid source with mixed audio and video.
#     """
#     stage = initialize_stage()
#     conversation = initialize_conversation(MIXED_CONV_DIR_PATH)
#     assert stage.set_conversation(conversation)
#     cleanup_sources()

# def test_set_conversations() -> None:
#     """
#     Tests:
#         1. Set multiple different types of conversations.
#     """
#     stage = initialize_stage()
#     conversation_audio_1 = initialize_conversation(MP3_FILE_PATH)
#     conversation_video_1 = initialize_conversation(MOV_FILE_PATH)
#     conversation_mixed_1 = initialize_conversation(MIXED_CONV_DIR_PATH)
#     assert stage.set_conversations([
#         conversation_audio_1,conversation_video_1, conversation_mixed_1])
#     cleanup_sources()

# def test_transcribe_audio_valid() -> None:
#     """
#     Tests:
#         1. Transcribe a valid audio conversation object.
#     """
#     stage = initialize_stage()
#     conversation = initialize_conversation(WAV_FILE_PATH)
#     stage.set_conversation(conversation)
#     results = stage.transcribe()
#     assert results[conversation.get_conversation_name()]
#     print_utterance_map(conversation.get_utterances())

def test_transcribe_video_valid() -> None:
    """
    Tests:
        1. Transcribe a valid video conversation object.
    """
    stage = initialize_stage()
    conversation = initialize_conversation(MOV_FILE_PATH)
    stage.set_conversation(conversation)
    results = stage.transcribe()
    assert results[conversation.get_conversation_name()]
    print_utterance_map(conversation.get_utterances())


# def test_transcribe_mixed_valid() -> None:
#     """
#     Tests:
#         1. Transcribe a conversation object with both audio and video sources.
#     """
#     stage = initialize_stage()
#     conversation = initialize_conversation(MIXED_CONV_DIR_PATH)
#     stage.set_conversation(conversation)
#     results = stage.transcribe()
#     assert results[conversation.get_conversation_name()]
#     print_utterance_map(conversation.get_utterances())


# def test_transcribe_multiple_conversations() -> None:
#     """
#     Transcribe multiple conversation objects in parallel.
#     """
#     stage = initialize_stage()
#     conversation_audio_1 = initialize_conversation(MP3_FILE_PATH)
#     conversation_video_1 = initialize_conversation(MOV_FILE_PATH)
#     conversation_mixed_1 = initialize_conversation(MIXED_CONV_DIR_PATH)
#     assert stage.set_conversations([
#         conversation_audio_1,conversation_video_1, conversation_mixed_1])
#     results = stage.transcribe()
#     assert results[conversation_audio_1.get_conversation_name()]
#     assert results[conversation_video_1.get_conversation_name()]
#     assert results[conversation_mixed_1.get_conversation_name()]


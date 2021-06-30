# Standard library imports
from typing import Dict, Any
# Local imports
from Src.Components.controller.services import OrganizerService, FileSystemService,\
                                                GBSettingAttrs
from Src.Components.controller.services.pipeline_service.format_stage \
    import FormatStage
from Src.Components.controller.services.pipeline_service.transcription_stage\
    import TranscriptionStage,TranscriptionStageResult
from Src.Components.controller.services.pipeline_service.analysis_stage import \
    AnalysisStage,AnalysisStageResult
from Src.Components.controller.services.pipeline_service import PipelineServiceLoader
from Src.Components.organizer import Conversation
from Src.Components.io import IO
# Third party imports

############################### GLOBALS #####################################

WS_DIR_PATH = "TestData/workspace/fs_workspace"
RESULT_DIR_PATH = "TestData/workspace/dir_2"
WAV_FILE_PATH = "TestData/media/test.wav"
MP3_FILE_PATH = "TestData/media/sample1.mp3"
CONV_DIR_PATH = "TestData/media/conversation"
MIXED_CONV_DIR_PATH = "TestData/media/audio_video_conversation"
MOV_FILE_PATH = "TestData/media/sample_video_conversation.mov"
FORMAT_CONFIG_PATH = "TestData/plugins/normal_format_plugins/config.json"
ANALYSIS_CONFIG_PATH = "TestData/plugins/analysis_plugins/config.json"

############################### SETUP ########################################

def transcribe_and_analyze(analysis_config_path : str,
        conversations : Dict[str,Conversation]) -> AnalysisStageResult:
    transcription_stage = TranscriptionStage()
    analysis_stage = AnalysisStage()
    loader = PipelineServiceLoader()
    configs = loader.parse_analysis_plugin_configuration_file(
        analysis_config_path)
    for data in configs:
        analysis_stage.register_plugin_from_data(data)
    # Transcribing
    results = transcription_stage.generate_utterances(conversations)
    # Analyzing
    return analysis_stage.analyze(conversations,results)

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

def test_register_format() -> None:
    """
    Tests:
        1. Load from a valid config path.
    """
    stage = FormatStage()
    loader = PipelineServiceLoader()
    format_name, configs = loader.parse_format_configuration_file(
        FORMAT_CONFIG_PATH)
    assert len(stage.register_format(format_name, configs)) > 0

def test_format_conversations_audio_source() -> None:
    """
    Tests:
        1. Format using an audio source conversation.
    """
    # Format init
    stage = FormatStage()
    loader = PipelineServiceLoader()
    format_name, configs = loader.parse_format_configuration_file(
        FORMAT_CONFIG_PATH)
    stage.register_format(format_name, configs)
    # Conversations
    c1 = initialize_conversation(MP3_FILE_PATH)
    # Running the transcriptionStage
    conversations = {
        c1.get_conversation_name() : c1}
    # Transcribing
    # Others
    analysis_stage_results = transcribe_and_analyze(
        ANALYSIS_CONFIG_PATH, conversations)
    results = stage.format_conversations(
        format_name, conversations,analysis_stage_results)
    print(results)

def test_format_conversations_video_source() -> None:
    # Format init
    stage = FormatStage()
    loader = PipelineServiceLoader()
    format_name, configs = loader.parse_format_configuration_file(
        FORMAT_CONFIG_PATH)
    stage.register_format(format_name, configs)
    # Conversations
    c1 = initialize_conversation(MOV_FILE_PATH)
    # Running the transcriptionStage
    conversations = {
        c1.get_conversation_name() : c1}
    # Transcribing
    # Others
    analysis_stage_results = transcribe_and_analyze(
        ANALYSIS_CONFIG_PATH, conversations)
    results = stage.format_conversations(
        format_name, conversations,analysis_stage_results)
    print(results)

def test_format_conversations_mixed_source() -> None:
    # Format init
    stage = FormatStage()
    loader = PipelineServiceLoader()
    format_name, configs = loader.parse_format_configuration_file(
        FORMAT_CONFIG_PATH)
    stage.register_format(format_name, configs)
    # Conversations
    c1 = initialize_conversation(MIXED_CONV_DIR_PATH)
    # Running the transcriptionStage
    conversations = {
        c1.get_conversation_name() : c1}
    # Transcribing
    # Others
    analysis_stage_results = transcribe_and_analyze(
        ANALYSIS_CONFIG_PATH, conversations)
    results = stage.format_conversations(
        format_name, conversations,analysis_stage_results)
    print(results)

def test_is_format() -> None:
    stage = FormatStage()
    loader = PipelineServiceLoader()
    format_name, configs = loader.parse_format_configuration_file(
        FORMAT_CONFIG_PATH)
    stage.register_format(format_name, configs)
    assert stage.is_format(format_name)

def is_format_plugin() -> None:
    stage = FormatStage()
    loader = PipelineServiceLoader()
    format_name, configs = loader.parse_format_configuration_file(
        FORMAT_CONFIG_PATH)
    stage.register_format(format_name, configs)
    assert stage.is_format_plugin(format_name,"plugin_one")
    assert stage.is_format_plugin(format_name,"plugin_two")

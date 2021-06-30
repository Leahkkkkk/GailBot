# Standard library imports
from typing import Dict, Any
# Local imports
from Src.Components.controller.services import OrganizerService, FileSystemService,\
                                                GBSettingAttrs
from Src.Components.controller.services.pipeline_service import \
    PipelineService, PipelineServiceSummary
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

def test_register_analysis_plugins() -> None:
    """
    Tests:
        1. Register from valid file.
        2. Register from invalid file.
    """
    service = PipelineService()
    assert len(service.register_analysis_plugins(ANALYSIS_CONFIG_PATH)) > 0
    assert len(service.register_analysis_plugins("invalid")) == 0

def test_register_format() -> None:
    """
    Tests:
        1. Register from a valid file.
        2. Register from an invalid file.
    """
    service = PipelineService()
    assert service.register_format(FORMAT_CONFIG_PATH) == \
        ("normal" , ["plugin_one", "plugin_two"])
    assert service.register_format("invalid") == ("",[])

def test_start_service_valid() -> None:
    """
    Tests:
        1. Test service with valid plugins and format added.
    """
    service = PipelineService()
    service.register_analysis_plugins(ANALYSIS_CONFIG_PATH)
    service.register_format(FORMAT_CONFIG_PATH)
    # Conversations
    c1 = initialize_conversation(MP3_FILE_PATH)
    c2 = initialize_conversation(MOV_FILE_PATH)
    c3 = initialize_conversation(MIXED_CONV_DIR_PATH)
    service.add_conversations([c1,c2,c3])
    summary = service.start_service()
    print(summary)

def test_get_analysis_plugin_names() -> None:
    """
    Tests:
        1. Make sure names are correct.
    """
    service = PipelineService()
    service.register_analysis_plugins(ANALYSIS_CONFIG_PATH)
    assert service.get_analysis_plugin_names() == ["plugin_one", "plugin_two"]

def test_get_format_names() -> None:
    """
    Tests:
        1. Check the format names.
    """
    service = PipelineService()
    service.register_format(FORMAT_CONFIG_PATH)
    assert service.get_format_names() == ["normal"]

def test_get_format_plugin_names() -> None:
    """
    Tests:
        1. Check the plugin names.
    """
    service = PipelineService()
    service.register_format(FORMAT_CONFIG_PATH)
    assert service.get_format_plugin_names("normal") == ["plugin_one", "plugin_two"]

def test_add_conversations() -> None:
    """
    Tests:
        1. Add multiple conversations.
    """
    service = PipelineService()
    # Conversations
    c1 = initialize_conversation(MP3_FILE_PATH)
    c2 = initialize_conversation(MOV_FILE_PATH)
    c3 = initialize_conversation(MIXED_CONV_DIR_PATH)
    assert service.add_conversations([c1,c2,c3])

def test_is_conversation() -> None:
    """
    Tests:
        1. Check valid conversation.
        2. Check invalid conversation.
    """
    service = PipelineService()
    # Conversations
    c1 = initialize_conversation(MP3_FILE_PATH)
    service.add_conversations([c1])
    assert service.is_conversation(c1.get_conversation_name())
    assert not service.is_conversation("invalid")

# Standard library imports
from Src.Components.organizer.conversation import Conversation
from typing import Any, Dict
# Local imports
from Src.Components.controller.services \
    import OrganizerService, SourceDetails,SettingDetails, FileSystemService,\
        GBSettingAttrs
from Src.Components.controller.services.pipeline_service import \
    PipelineService, PipelineServiceSummary


############################### GLOBALS #####################################
# DIR PATHS
WS_DIR_PATH = "TestData/workspace/fs_workspace"
RESULT_DIR_PATH = "TestData/workspace/results"
# CONVERSATION PATHS
MIXED_CONV_PATH = "TestData/media/audio_video_conversation"
MOV_FILE_PATH = "TestData/media/sample-mov-file.mov"
MP3_FILE_PATH = "TestData/media/sample1.mp3"
# PLUGINS
ANALYSIS_PLUGIN_CONFIG_PATH = "TestData/workspace/plugins/pipeline_service_test/analysis_config.json"
FORMAT_PLUGIN_CONFIG_PATH = "TestData/workspace/plugins/pipeline_service_test/format_config.json"

############################### SETUP #####################################

def initialize_configured_service() -> OrganizerService:
    fs_service = FileSystemService()
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    service = OrganizerService(fs_service)
    assert service.is_configured()
    return service

def obtain_settings_profile_data() -> Dict[str,Any]:
    return {
        GBSettingAttrs.engine_type : "watson",
        GBSettingAttrs.watson_api_key : "MSgOPTS9CvbADe49nEg4wm8_gxeRuf4FGUmlHS9QqAw3",
        GBSettingAttrs.watson_language_customization_id : "41e54a38-2175-45f4-ac6a-1c11e42a2d54",
        GBSettingAttrs.watson_base_language_model : "en-US_BroadbandModel",
        GBSettingAttrs.watson_region : "dallas",
        GBSettingAttrs.analysis_plugins_to_apply : ["second_analysis"],
        GBSettingAttrs.output_format : "normal"}

def conversation_from_source(source_name : str, source_path : str) -> Conversation:
    organizer_service = initialize_configured_service()
    profile_name = "new"
    assert organizer_service.create_new_settings_profile(
        profile_name,obtain_settings_profile_data())
    assert organizer_service.add_source(source_name, source_path,RESULT_DIR_PATH)
    assert organizer_service.apply_settings_profile_to_source(
        source_name,profile_name)
    conversation =  organizer_service.get_configured_source_conversation(
        source_name)
    assert conversation != None
    return conversation

########################## TEST DEFINITIONS ##################################

def test() -> None:
    service = PipelineService(4)
    c1 = conversation_from_source("mp3",MP3_FILE_PATH)
    assert service.add_source(c1.get_conversation_name(),c1)
    assert service.is_source(c1.get_conversation_name())
    print(service.register_analysis_plugins(ANALYSIS_PLUGIN_CONFIG_PATH))
    print(service.register_format(FORMAT_PLUGIN_CONFIG_PATH))
    summary = service.start()
    print(summary)
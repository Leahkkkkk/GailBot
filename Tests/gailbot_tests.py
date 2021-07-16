# Standard library imports
from typing import Dict, Any

# Local imports
from Src.Components import GailBotController,SettingDetails, SourceDetails,GBSettingAttrs,\
                        PipelineServiceSummary, AnalysisPlugin, AnalysisPluginInput,\
                        FormatPlugin, FormatPluginInput, ConversationSummary
############################### GLOBALS #####################################

WS_DIR_PATH = "TestData/workspace/gb_tests_ws"
RESULT_DIR_PATH = "TestData/workspace/gb_tests_results"
# AUDIO FILES
WAV_FILE_PATH = "TestData/media/test2a.wav"
MP3_FILE_PATH = "TestData/media/sample1.mp3"
# VIDEO FILES
MP4_FILE_PATH = "TestData/media/sample-mp4-file.mp4"
MOV_FILE_PATH = "TestData/media/sample_video_conversation.mov"
# SOURCE DIRS
CONV_DIR_PATH = "TestData/media/small_conversation"
MIXED_CONV_DIR_PATH = "TestData/media/audio_video_conversation"
# PLUGINS DIRS
ANALYSIS_PLUGINS_DIR = "TestData/plugins/gb_2019_plugins/analysis"
ANALYSIS_CONFIG_PATH = "TestData/plugins/gb_2019_plugins/analysis/config.json"
FORMAT_PLUGINS_DIR = "TestData/plugins/gb_2019_plugins/format"
FORMAT_CONFIG_PATH = "TestData/plugins/gb_2019_plugins/format/config.json"


############################### SETUP #######################################

def initialize_controller() -> GailBotController:
    return GailBotController(WS_DIR_PATH)

def get_settings_profile_data() -> Dict[GBSettingAttrs,Any]:
    return {
        GBSettingAttrs.engine_type : "watson",
        GBSettingAttrs.watson_api_key :
            "MSgOPTS9CvbADe49nEg4wm8_gxeRuf4FGUmlHS9QqAw3",
        GBSettingAttrs.watson_language_customization_id :
            "41e54a38-2175-45f4-ac6a-1c11e42a2d54",
        GBSettingAttrs.watson_base_language_model : "en-US_BroadbandModel",
        GBSettingAttrs.watson_region : "dallas"
    }

########################## TEST DEFINITIONS ##################################

def test() -> None:
    controller = GailBotController(WS_DIR_PATH)
    # Registering plugins
    controller.register_analysis_plugins(ANALYSIS_CONFIG_PATH)
    controller.register_format(FORMAT_CONFIG_PATH)
    # Adding sources
    controller.create_new_settings_profile("test",get_settings_profile_data())
    controller.add_source("mixed",MIXED_CONV_DIR_PATH,RESULT_DIR_PATH,RESULT_DIR_PATH)
    controller.apply_settings_profile_to_source("mixed","test")
    summary = controller.transcribe()
    for conv_name, conv_summary in summary.conversation_summary.items():
        print(conv_name, conv_summary)
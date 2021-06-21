# Standard library imports
from typing import List, Dict, Any

# Local imports
from Src.Components import GailBotController, SettingDetails, SourceDetails, \
                    GBSettingAttrs, TranscriptionSummary

############################### GLOBALS #####################################

WS_DIR_PATH = "TestData/workspace/fs_workspace"
WAV_FILE_PATH = "TestData/media/test2a.wav"
MP3_FILE_PATH = "TestData/media/sample1.mp3"
TXT_FILE_PATH = "TestData/configs/textfile.txt"
IMAGES_DIR_PATH = "TestData/images"
CONV_DIR_PATH = "TestData/media/small_conversation"
RESULT_DIR_PATH = "TestData/workspace/dir_2"
MP4_FILE_PATH = "TestData/media/sample-mp4-file.mp4"


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


def test_add_source_video() -> None:
    controller = GailBotController(WS_DIR_PATH)

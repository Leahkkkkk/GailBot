# Standard library imports
from typing import List
# Local imports
from Src.Components.controller import GailBotController, TranscriptionSummary,\
                                SourceDetails,SettingDetails
############################### GLOBALS #####################################

TEMP_WS_PATH = "TestData/workspace"
SETTINGS_DIR_PATH = "TestData/configs/settings"
CONFIG_FILE_PATH = "TestData/configs/config.json"
WAV_FILE_PATH = "TestData/media/test2a.wav"
MP3_FILE_PATH = "TestData/media/sample1.mp3"
CONV_DIR_PATH = "TestData/media/conversation"
SMALL_CONV_DIR_PATH = "TestData/media/small_conversation"

############################### SETUP #######################################


def initialize_controller() -> GailBotController:
    controller = GailBotController()
    assert controller.set_configuration_file_path(CONFIG_FILE_PATH)
    assert controller.is_configured()
    return controller

########################## TEST DEFINITIONS ##################################

def test_controller_add_source() -> None:
    controller = initialize_controller()
    assert controller.add_source("mp3",MP3_FILE_PATH,TEMP_WS_PATH)
    summary = controller.transcribe_all_sources()
    print(summary)



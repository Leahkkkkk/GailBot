# Standard library imports
from typing import List
# Local imports
from Src.Components.controller import GailBotController, TranscriptionSummary,\
                                SourceDetails,SettingDetails
############################### GLOBALS #####################################

WS_DIR_PATH = "TestData/workspace/fs_workspace"
WAV_FILE_PATH = "TestData/media/test2a.wav"
MP3_FILE_PATH = "TestData/media/sample1.mp3"
TXT_FILE_PATH = "TestData/configs/textfile.txt"
IMAGES_DIR_PATH = "TestData/images"
CONV_DIR_PATH = "TestData/media/conversation"
RESULT_DIR_PATH = "TestData/workspace/dir_2"


############################### SETUP #######################################

def initialize_controller() -> GailBotController:
    return GailBotController(WS_DIR_PATH)

########################## TEST DEFINITIONS ##################################

def test_controller_add_source() -> None:
    """
    Tests:
        1. Add a valid file source.
        2. Add a valid directory source.
        3. Add an invalid source.
        4. Add an existing source.
    """
    controller = initialize_controller()
    assert controller.add_source("file",MP3_FILE_PATH, RESULT_DIR_PATH)
    assert controller.add_source("directory",CONV_DIR_PATH,RESULT_DIR_PATH)
    assert not controller.add_source("file",MP3_FILE_PATH, RESULT_DIR_PATH)
    # TODO: Run test after method fixed.
    #assert not controller.add_source("invalid","invalid", RESULT_DIR_PATH)
    assert controller.remove_sources(["file","directory"])

def test_controller_remove_source() -> None:
    pass

def test_controller_remove_sources() -> None:
    pass
# Standard library imports

############################### GLOBALS #####################################
from Src.Components.controller.services.config_service import ConfigService,\
    SystemBlackBoard
from Src.Components.controller.services.fs_service import FileSystemService


############################### SETUP #####################################

WS_DIR_PATH = "TestData/workspace/temp_ws"
CONFIG_FILE_PATH = "TestData/configs/config.json"
WAV_FILE_PATH = "TestData/media/overlayed.wav"


########################## TEST DEFINITIONS ##################################

def test_is_system_blackboard_loaded() -> None:
    fs_service = FileSystemService()
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    service = ConfigService(fs_service)
    assert service.is_system_blackboard_loaded()

def test_get_system_blackboard() -> None:
    fs_service = FileSystemService()
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    service = ConfigService(fs_service)
    assert type(service.get_system_blackboard()) == SystemBlackBoard

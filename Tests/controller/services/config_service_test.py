# Standard library imports
# Local imports
from Src.Components.controller.services import ConfigService, FileSystemService
from Src.Components.config import SystemBB

############################### GLOBALS #####################################

WS_DIR_PATH = "TestData/workspace/fs_workspace"
WAV_FILE_PATH = "TestData/media/test2a.wav"
CONFIG_FILE_PATH = "TestData/workspace/fs_workspace/config.json"



########################## TEST DEFINITIONS ##################################

def test_config_service_configure_from_path_valid() -> None:
    """
    Tests:
        1. Configure from a valid path before fs_service configured.
        2. Configure from a valid path after fs_service configured.
    """
    fs_service = FileSystemService()
    service = ConfigService(fs_service)
    assert not service.configure_from_path()
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    assert service.configure_from_path()

def test_config_service_configure_from_path_invalid() -> None:
    """
    Tests:
        1. Configure from an invalid path.
    """
    fs_service = FileSystemService()
    service = ConfigService(fs_service)
    fs_service.configure_from_workspace_path(WAV_FILE_PATH)
    assert not service.configure_from_path()

def test_config_service_is_configured() -> None:
    """
    Tests:
        1. Check that fully configured after loading from valid file.
        2. Check that is not configured before loading from file.
    """
    fs_service = FileSystemService()
    service = ConfigService(fs_service)
    assert not service.is_configured()
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    service.configure_from_path()
    assert service.is_configured()

def test_config_service_get_configuration_file_path() -> None:
    """
    Tests:
        1. Get path before configuring.
        2. Get path after configuring.
    """
    fs_service = FileSystemService()
    service = ConfigService(fs_service)
    assert service.get_configuration_file_path() == None
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    service.configure_from_path()
    assert service.get_configuration_file_path() == CONFIG_FILE_PATH

def test_config_service_get_supported_blackboard_types() -> None:
    """
    Tests:
        1. Get system blackboard and check values against file values.
    """

    fs_service = FileSystemService()
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    service = ConfigService(fs_service)
    service.configure_from_path()
    assert service.get_supported_blackboard_types() == ["system_blackboard"]

def test_config_service_get_system_blackboard() -> None:
    """
    Tests:
        1. Reset and check that blackboard cannot be retrieved.
    """
    fs_service = FileSystemService()
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    service = ConfigService(fs_service)
    service.configure_from_path()
    system_bb = service.get_system_blackboard()
    assert type(system_bb) == SystemBB

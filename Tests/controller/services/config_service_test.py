# Standard library imports
# Local imports
from os import sysconf
from Src.Components.controller.services import ConfigService
from Src.Components.config import SystemBB

############################### GLOBALS #####################################

CONFIG_PATH = "TestData/configs/config.json"
INVALID_CONFIG_PATH = "TestData/configs/invalid_config.json"
########################## TEST DEFINITIONS ##################################

def test_config_service_set_configuration_file_path_valid() -> None:
    """
    Tests:
        1. Set a valid file path for configuration.
    """
    service = ConfigService()
    assert service.set_configuration_file_path(CONFIG_PATH)

def test_config_service_set_configuration_file_path_invalid() -> None:
    """
    Tests:
        1. Set an invalid file path for configuration.
    """
    service = ConfigService()
    assert not service.set_configuration_file_path("not a path")

def test_config_service_configure_from_path_valid() -> None:
    """
    Tests:
        1. Configure from a valid path / config file.
    """
    service = ConfigService()
    assert service.set_configuration_file_path(CONFIG_PATH)
    assert service.configure_from_path()


def test_config_service_configure_from_path_invalid() -> None:
    """
    Tests:
        1. Configure from an invalid path / config file.
    """
    service = ConfigService()
    assert service.set_configuration_file_path(INVALID_CONFIG_PATH)
    assert not service.configure_from_path()

def test_config_service_is_fully_configured() -> None:
    """
    Tests:
        1. Check that fully configured after loading from valid file.
        2. Check that is not configured before loading from file.
    """
    service = ConfigService()
    assert service.set_configuration_file_path(CONFIG_PATH)
    assert not service.is_fully_configured()
    assert service.configure_from_path()
    assert service.is_fully_configured()

def test_config_service_get_configuration_file_path() -> None:
    """
    Tests:
        1. Ensure that the configuration path is the correct one.
    """
    service = ConfigService()
    assert service.get_configuration_file_path() == ""
    service.set_configuration_file_path(CONFIG_PATH)
    assert service.get_configuration_file_path() == CONFIG_PATH

def test_config_service_get_supported_blackboard_types() -> None:
    """
    Tests:
        1. Ensure that the blackboard types are as expected.
    """
    service = ConfigService()
    assert service.get_supported_blackboard_types() == ["system_blackboard"]

def test_config_service_get_system_blackboard() -> None:
    """
    Tests:
        1. Get system blackboard and check values against file values.
    """
    service = ConfigService()
    service.set_configuration_file_path(CONFIG_PATH)
    service.configure_from_path()
    system_bb = service.get_system_blackboard()
    assert type(system_bb) == SystemBB

def test_config_service_reset() -> None:
    """
    Tests:
        1. Reset and check that blackboard cannot be retrieved.
        2. Reset and make sure blackboards can be loaded again.
    """
    service = ConfigService()
    service.set_configuration_file_path(CONFIG_PATH)
    service.configure_from_path()
    service.reset()
    assert service.get_system_blackboard() == None
    service.set_configuration_file_path(CONFIG_PATH)
    service.configure_from_path()
    assert type(service.get_system_blackboard()) == SystemBB




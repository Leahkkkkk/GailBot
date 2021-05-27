# Standard library imports
from enum import Enum
from typing import Any, Dict, Callable
# Local imports
from Src.Components.controller.services import FileSystemService
from Src.Components.organizer import Organizer,Settings
from Src.Components.io import IO

############################### GLOBALS #####################################

WS_DIR_PATH = "TestData/workspace/fs_workspace"
WAV_FILE_PATH = "TestData/media/test2a.wav"
CONFIG_FILE_PATH = "TestData/workspace/fs_workspace/config.json"


############################### SETUP #####################################
class CustomAttrs(Enum):
    test = "test"

class CustomSettings(Settings):

    def __init__(self, data : Dict[str,Any]) -> None:
        self.attrs = [e.value for e in CustomAttrs]
        super().__init__(attrs=self.attrs)
        self._parse_data(data)

    def save_to_file(self, save_method : Callable[[Dict],bool]) -> bool:
        data = dict()
        for attr in self.attrs:
            data[attr] = self.get(attr)[1]
        return save_method(data)

    def _parse_data(self, data : Dict[str,Any]) -> None:
        for attr, value in data.items():
            self._set_value(attr,value)

def initialize_service() -> FileSystemService:
    fs_service = FileSystemService()
    assert fs_service.configure_from_workspace_path(WS_DIR_PATH)
    return fs_service

def create_settings() -> CustomSettings:
    organizer = Organizer(IO())
    organizer.register_settings_type(
        "custom",lambda data : CustomSettings(data))
    return organizer.create_settings("custom",{"test" : 1})[1]

########################## TEST DEFINITIONS ##################################

def test_fs_service_configure_from_workspace_path_valid() -> None:
    """
    Tests:
        1. Configure fs service from valid directory.
    """
    fs_service = FileSystemService()
    assert fs_service.configure_from_workspace_path(WS_DIR_PATH)


def test_fs_service_configure_from_workspace_path_invalid() -> None:
    """
    Tests:
        1. Configure fs service from invalid file.
        2. Configure from random string.
    """
    fs_service = FileSystemService()
    assert not fs_service.configure_from_workspace_path(WAV_FILE_PATH)
    assert not fs_service.configure_from_workspace_path("invalid")

def test_fs_service_shutdown() -> None:
    """
    Tests:
        1. Shutdown when not configured.
        2. Shutdown after configuring.
    """
    fs_service = FileSystemService()
    assert not fs_service.shutdown()
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    assert fs_service.shutdown()

def test_fs_service_save_settings_profile_to_disk() -> None:
    """
    Tests:
        1. Save a settings profile to disk without configuring.
        2. Save a settings profile to disk after configuring.
    """
    fs_service = FileSystemService()
    settings = create_settings()
    assert not fs_service.save_settings_profile_to_disk("s1",settings)
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    assert fs_service.save_settings_profile_to_disk("s1",settings)
    assert fs_service.remove_settings_profile_from_disk("s1")

def test_fs_service_load_saved_settings_profile_data_from_disk() -> None:
    """
    Tests:
        1. Load a setting before configuring.
        2. Load a saved setting.
        3. Load a setting that is not saved.
    """
    fs_service = FileSystemService()
    profile_name = "s2"
    settings = create_settings()
    assert not fs_service.load_saved_settings_profile_data_from_disk(
        profile_name)
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    fs_service.save_settings_profile_to_disk(profile_name,settings)
    assert type(fs_service.load_saved_settings_profile_data_from_disk(
                profile_name)) == dict
    assert fs_service.load_saved_settings_profile_data_from_disk("invalid") \
            == None
    assert fs_service.remove_settings_profile_from_disk(profile_name)

def test_fs_service_load_all_settings_profiles_data_from_disk() -> None:
    """
    Tests:
        1. Load all profiles and check before configuring.
        2. Load all profiles and check after configuring.
        3. Load all profiles and check after creating new profile.
    """
    fs_service = FileSystemService()
    assert fs_service.load_all_settings_profiles_data_from_disk() == None
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    assert len(fs_service.load_all_settings_profiles_data_from_disk().values()) == 0
    fs_service.save_settings_profile_to_disk("s1",create_settings())
    assert len(fs_service.load_all_settings_profiles_data_from_disk().values()) == 1
    fs_service.remove_settings_profile_from_disk("s1")

def test_fs_service_remove_settings_profile_from_disk() -> None:
    """
    Tests:
        1. Remove before configuring.
        2. Remove profile that does not exist after configuring.
        3. Remove profile that does exist after configuring.
    """
    fs_service = FileSystemService()
    assert not fs_service.remove_settings_profile_from_disk("invalid")
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    assert not fs_service.remove_settings_profile_from_disk("invalid")
    fs_service.save_settings_profile_to_disk("s1",create_settings())
    assert fs_service.remove_settings_profile_from_disk("s1")

def test_fs_service_create_source_workspace_on_disk() -> None:
    """
    Tests:
        1. Create source workspace before configuring.
        2. Create source workspace after configuring.
        3. Attempt to create workspace that already exists.
    """
    fs_service = FileSystemService()
    assert not fs_service.create_source_workspace_on_disk("s1")
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    assert fs_service.create_source_workspace_on_disk("s1")
    assert not fs_service.create_source_workspace_on_disk("s1")
    fs_service.cleanup_source_workspace_from_disk("s1")


def test_fs_service_cleanup_source_workspace_from_disk() -> None:
    """
    Tests:
        1. Cleanup before configuring.
        2. Cleanup source that does not exist.
        3. Cleanup source that does exit.
    """
    fs_service = FileSystemService()
    assert not fs_service.cleanup_source_workspace_from_disk("s1")
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    fs_service.create_source_workspace_on_disk("s1")
    assert fs_service.cleanup_source_workspace_from_disk("s1")
    assert not fs_service.cleanup_source_workspace_from_disk("s1")

def test_fs_service_is_configured() -> None:
    """
    Tests:
        1. Determine if configured after initialization only.
        2. Determine if configured after invalid file.
        3. Determine if configured after valid directory.
    """
    fs_service = FileSystemService()
    assert not fs_service.is_configured()
    fs_service.configure_from_workspace_path(WAV_FILE_PATH)
    assert not fs_service.is_configured()
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    assert fs_service.is_configured()
    fs_service.configure_from_workspace_path(WAV_FILE_PATH)
    assert fs_service.is_configured()

def test_fs_service_get_workspace_dir_path() -> None:
    """
    Tests:
        1. Get path before configuring.
        2. Get path after configuring.
    """
    fs_service = FileSystemService()
    assert fs_service.get_workspace_dir_path() == None
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    assert fs_service.get_workspace_dir_path() == WS_DIR_PATH

def test_fs_service_get_config_service_data_from_disk() -> None:
    """
    Tests:
        1. Get data before configuring.
        2. Get data after configuring.
    """
    fs_service = FileSystemService()
    assert fs_service.get_config_service_data_from_disk() == None
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    assert type(fs_service.get_config_service_data_from_disk()) == dict

def test_fs_service_get_config_service_configuration_source() -> None:
    """
    Tests:
        1. Get the source before configuring.
        2. Get the source after configuring.
    """
    fs_service = FileSystemService()
    assert fs_service.get_config_service_configuration_source() == None
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    assert fs_service.get_config_service_configuration_source() == CONFIG_FILE_PATH


def test_fs_service_is_saved_settings_profile() -> None:
    """
    Tests:
        1. Check before configuring.
        2. Check after configuring.
    """
    fs_service = FileSystemService()
    assert not fs_service.is_saved_settings_profile("invalid")
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    fs_service.save_settings_profile_to_disk("s1",create_settings())
    assert fs_service.is_saved_settings_profile("s1")
    fs_service.remove_settings_profile_from_disk("s1")

def test_fs_service_is_saved_settings_profile() -> None:
    """
    Tests:
        1. Check before configuring.
        2. Check after configuring.
        3. Check invalid.
    """
    fs_service = FileSystemService()
    assert not fs_service.is_saved_settings_profile("s1")
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    fs_service.save_settings_profile_to_disk("s1",create_settings())
    assert fs_service.is_saved_settings_profile("s1")
    fs_service.remove_settings_profile_from_disk("s1")
    assert not fs_service.is_saved_settings_profile("s1")

def test_fs_service_get_saved_settings_profile_location_on_disk() -> None:
    """
    Tests:
        1. Get the save location on disk before confguring.
        2. Get the location after configuring.
        3. Get the location of a profile that does not exist.
    """
    io = IO()
    fs_service = FileSystemService()
    assert fs_service.get_saved_settings_profile_location_on_disk("s1") == None
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    fs_service.save_settings_profile_to_disk("s1",create_settings())
    assert io.is_file(fs_service.get_saved_settings_profile_location_on_disk("s1"))
    fs_service.remove_settings_profile_from_disk("s1")
    assert not io.is_file(fs_service.get_saved_settings_profile_location_on_disk("s1"))

def test_fs_service_get_saved_settings_profile_names() -> None:
    """
    Tests:
        1. Get names of all saved profiles before configuring.
        2. Get names of all saved profiles after configuring.
    """
    fs_service = FileSystemService()
    assert len(fs_service.get_saved_settings_profile_names()) == 0
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    assert len(fs_service.get_saved_settings_profile_names()) == 0
    fs_service.save_settings_profile_to_disk("s1",create_settings())
    assert len(fs_service.get_saved_settings_profile_names()) == 1
    fs_service.remove_settings_profile_from_disk("s1")

# TODO: Test after fixing.
def test_fs_service_get_source_workspace_names() -> None:
    """
    Tests:
        1. Get before configuring.
        2. Get after configuring.
    """
    pass
    # fs_service = FileSystemService()
    # assert len(fs_service.get_source_workspace_names()) == 0
    # fs_service.configure_from_workspace_path(WS_DIR_PATH)
    # fs_service.create_source_workspace_on_disk("s1")
    # assert len(fs_service.get_source_workspace_names()) == 1
    # fs_service.cleanup_source_workspace_from_disk("s1")


def test_fs_service_get_source_workspace_location_on_disk() -> None:
    """
    Tests:
        1. Check location before configuring.
        2. Check after configuring.
    """
    io = IO()
    fs_service = FileSystemService()
    fs_service.get_source_workspace_location_on_disk("s1") == None
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    fs_service.create_source_workspace_on_disk("s1")
    assert io.is_directory(
        fs_service.get_source_workspace_location_on_disk("s1"))
    fs_service.cleanup_source_workspace_from_disk("s1")

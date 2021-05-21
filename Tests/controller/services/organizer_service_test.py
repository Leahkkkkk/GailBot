# Standard library imports
# Local imports
from Src.Components.controller.services \
    import OrganizerService, SourceDetails,SettingDetails
from Src.Components.organizer import Settings, Conversation

############################### GLOBALS #####################################

SETTINGS_DIR_PATH = "TestData/configs/settings"
TEMP_WS_PATH = "TestData/workspace"
WAV_FILE_PATH = "TestData/media/test2a.wav"
TXT_FILE_PATH = "TestData/configs/textfile.txt"
IMAGES_DIR_PATH = "TestData/images"
CONV_DIR_PATH = "TestData/media/conversation"

########################## TEST DEFINITIONS ##################################

def test_organizer_service_add_source_valid() -> None:
    """
    Tests:
        1. Add a valid source and ensure conversation created from file.
        2. Add a valid source and ensure conversation created from directory.
    """
    service = OrganizerService()
    service.set_workspace_path(SETTINGS_DIR_PATH)
    service.set_conversation_workspace_path(TEMP_WS_PATH)
    assert service.add_source("file",WAV_FILE_PATH,TEMP_WS_PATH,"GB")
    assert service.add_source("dir",CONV_DIR_PATH,TEMP_WS_PATH,"GB")

# TODO: Add test when bugs have been fixed.
# def test_organizer_service_add_source_invalid() -> None:
#     """
#     Tests:
#         1. Add an invalid file.
#         2. Add a directory with invalid files.
#         3. Add an empty directory.
#     """
#     service = OrganizerService()
#     service.set_workspace_path(SETTINGS_DIR_PATH)
#     service.set_conversation_workspace_path(TEMP_WS_PATH)
#     assert not service.add_source("file",TXT_FILE_PATH,TEMP_WS_PATH,"GB")
#     assert not service.add_source("dir",IMAGES_DIR_PATH,TEMP_WS_PATH,"GB")
#     assert not service.add_source("dir",TEMP_WS_PATH,TEMP_WS_PATH,"GB")

def test_organizer_service_remove_source() -> None:
    """
    Tests:
        1. Remove an existing source
        2. Remove a source that does not exist.
    """
    service = OrganizerService()
    service.set_workspace_path(SETTINGS_DIR_PATH)
    service.set_conversation_workspace_path(TEMP_WS_PATH)
    assert service.add_source("file",WAV_FILE_PATH,TEMP_WS_PATH,"GB")
    assert service.remove_source("file")
    assert not service.remove_source("file")

def test_organizer_service_clear_sources() -> None:
    """
    Tests:
        1. Clear sources and check previously added cannot be retrieved.
    """
    service = OrganizerService()
    service.set_workspace_path(SETTINGS_DIR_PATH)
    service.set_conversation_workspace_path(TEMP_WS_PATH)
    service.add_source("file",WAV_FILE_PATH,TEMP_WS_PATH,"GB")
    assert service.clear_sources()
    assert service.add_source("file",WAV_FILE_PATH,TEMP_WS_PATH,"GB")

def test_organizer_service_save_settings() -> None:
    """
    Tests:
        1. Save a settings object without changing data.
        2. Attempt to save a settings object with an existing name.
    """
    service = OrganizerService()
    service.set_workspace_path(SETTINGS_DIR_PATH)
    service.set_conversation_workspace_path(TEMP_WS_PATH)
    service.add_source("file",WAV_FILE_PATH,TEMP_WS_PATH,"GB")
    assert service.save_source_settings("file","profile1")
    assert service.delete_setting("profile1")
    assert not service.save_source_settings("file","default")

def test_organizer_service_delete_setting() -> None:
    """
    Tests:
        1. Delete a valid setting.
        2. Attempt to delete a setting that does not exist.
    """
    service = OrganizerService()
    service.set_workspace_path(SETTINGS_DIR_PATH)
    service.set_conversation_workspace_path(TEMP_WS_PATH)
    service.add_source("file",WAV_FILE_PATH,TEMP_WS_PATH,"GB")
    assert service.save_source_settings("file","profile1")
    assert service.delete_setting("profile1")
    assert not service.delete_setting("invalid")

def test_organizer_service_is_setting() -> None:
    """
    Tests:
        1. Check a valid setting exists.
        2. Check invalid settings does not exist.
    """
    service = OrganizerService()
    service.set_workspace_path(SETTINGS_DIR_PATH)
    service.set_conversation_workspace_path(TEMP_WS_PATH)
    assert service.is_setting("default")
    assert not service.is_setting("invalid")

def test_organizer_service_is_source() -> None:
    """
    Tests:
        1. Check an added source exists.
        2. Check unknown source does not exist.
    """
    service = OrganizerService()
    service.set_workspace_path(SETTINGS_DIR_PATH)
    service.set_conversation_workspace_path(TEMP_WS_PATH)
    service.add_source("file",WAV_FILE_PATH,TEMP_WS_PATH,"GB")
    assert service.is_source("file")
    assert not service.is_source("dir")

def test_organizer_service_get_source_names() -> None:
    """
    Tests:
        1. Obtain and verify names of sources.
    """
    service = OrganizerService()
    service.set_workspace_path(SETTINGS_DIR_PATH)
    service.set_conversation_workspace_path(TEMP_WS_PATH)
    assert len(service.get_source_names()) == 0
    service.add_source("file",WAV_FILE_PATH,TEMP_WS_PATH,"GB")
    assert service.get_source_names() == ["file"]

def test_organizer_service_get_source_paths() -> None:
    """
    Tests:
        1. Ensure no paths are present if no sources added.
        2. Ensure the source paths are valid.
    """
    service = OrganizerService()
    service.set_workspace_path(SETTINGS_DIR_PATH)
    service.set_conversation_workspace_path(TEMP_WS_PATH)
    assert len(service.get_source_paths()) == 0
    service.add_source("file",WAV_FILE_PATH,TEMP_WS_PATH,"GB")
    assert service.get_source_paths() == [WAV_FILE_PATH]

def test_organizer_service_get_source_settings() -> None:
    """
    Tests:
        1. Check object of type settings is returned.
    """
    service = OrganizerService()
    service.set_workspace_path(SETTINGS_DIR_PATH)
    service.set_conversation_workspace_path(TEMP_WS_PATH)
    service.add_source("file",WAV_FILE_PATH,TEMP_WS_PATH,"GB")
    assert isinstance(service.get_source_settings("file"),Settings)

def test_organizer_service_get_available_setting_details() -> None:
    """
    Tests:
    """
    pass

def test_organizer_service_get_available_setting_names() -> None:
    """
    Tests:
        1. Check default setting names available.
        2. Check if new setting names are available after saving.
    """
    service = OrganizerService()
    service.set_workspace_path(SETTINGS_DIR_PATH)
    service.set_conversation_workspace_path(TEMP_WS_PATH)
    assert service.get_available_setting_names() == ["default"]
    service.add_source("file",WAV_FILE_PATH,TEMP_WS_PATH,"GB")
    service.save_source_settings("file","test")
    assert service.get_available_setting_names() == ["default","test"]
    service.delete_setting("test")

def test_organizer_service_get_source_details() -> None:
    """
    Tests:
    """
    pass

def test_organizer_service_get_all_sources_conversations() -> None:
    """
    Tests:
        1. Ensure number of conversations is the same as thw sources.
    """
    service = OrganizerService()
    service.set_workspace_path(SETTINGS_DIR_PATH)
    service.set_conversation_workspace_path(TEMP_WS_PATH)
    assert len(service.get_all_sources_conversations()) == 0
    service.add_source("file",WAV_FILE_PATH,TEMP_WS_PATH,"GB")
    assert len(service.get_all_sources_conversations()) == 1

def organizer_service_get_source_conversation() -> None:
    """
    Tets:
        1. Ensure a conversation type object is retrieved for a valid source.
        2. Ensure None is returned for an invalid source.
    """
    service = OrganizerService()
    service.set_workspace_path(SETTINGS_DIR_PATH)
    service.set_conversation_workspace_path(TEMP_WS_PATH)
    service.add_source("file",WAV_FILE_PATH,TEMP_WS_PATH,"GB")
    assert type(service.get_source_conversation("file")) == Conversation
    assert service.get_source_conversation("invalid") == None

def test_organizer_service_set_workspace_path() -> None:
    """
    Tests:
        1. Set a workspace path with a default settings, which should work.
        2. Set a workspace with no default settings.
    """
    service = OrganizerService()
    assert service.set_workspace_path(SETTINGS_DIR_PATH)
    assert not service.set_workspace_path(TEMP_WS_PATH)

def test_organizer_service_set_conversation_workspace_path() -> None:
    """
    Tests:
        1. Set a valid directory as path.
        2. Set an invalid file as path.
    """
    service = OrganizerService()
    assert service.set_conversation_workspace_path(TEMP_WS_PATH)
    assert not service.set_conversation_workspace_path(WAV_FILE_PATH)

def test_organizer_service_load_setting_from_path() -> None:
    """
    Tests:
    """
    pass
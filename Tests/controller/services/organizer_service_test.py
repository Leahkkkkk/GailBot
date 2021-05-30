# Standard library imports
from Src.Components.controller.services.organizer_service.settings import GailBotSettings
from typing import Any, Dict
# Local imports
from Src.Components.controller.services \
    import OrganizerService, SourceDetails,SettingDetails, FileSystemService,\
        GBSettingAttrs
from Src.Components.organizer import Settings, Conversation

############################### GLOBALS #####################################

WS_DIR_PATH = "TestData/workspace/fs_workspace"
WAV_FILE_PATH = "TestData/media/test2a.wav"
TXT_FILE_PATH = "TestData/configs/textfile.txt"
IMAGES_DIR_PATH = "TestData/images"
CONV_DIR_PATH = "TestData/media/conversation"
RESULT_DIR_PATH = "TestData/workspace/dir_2"


############################### GLOBALS #####################################
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
        GBSettingAttrs.watson_region : "dallas"
    }

########################## TEST DEFINITIONS ##################################

def test_organizer_service_add_source_valid() -> None:
    """
    Tests:
        1. Add a valid source and ensure conversation created from file.
        2. Add a valid source and ensure conversation created from directory.
    """
    service = initialize_configured_service()
    assert service.add_source("file",WAV_FILE_PATH,RESULT_DIR_PATH)
    assert service.add_source("dir",CONV_DIR_PATH,RESULT_DIR_PATH)
    assert service.clear_sources()

def test_organizer_service_add_source_invalid() -> None:
    pass


def test_organizer_service_remove_source() -> None:
    """
    Tests:
        1. Remove an existing source
        2. Remove a source that does not exist.
    """
    service = initialize_configured_service()
    assert service.add_source("file",WAV_FILE_PATH,RESULT_DIR_PATH)
    assert service.remove_source("file")
    assert not service.remove_source("file")

def test_organizer_service_remove_sources() -> None:
    """
    Tests:
        1. Remove one existing and one invalid source.
        2. Remove all valid sources.
    """
    service = initialize_configured_service()
    service.add_source("file",WAV_FILE_PATH,RESULT_DIR_PATH)
    assert not service.remove_sources(["file","invalid"])
    service.add_source("file",WAV_FILE_PATH,RESULT_DIR_PATH)
    service.add_source("dir",CONV_DIR_PATH,RESULT_DIR_PATH)
    assert service.remove_sources(["file","dir"])


def test_organizer_service_clear_sources() -> None:
    """
    Tests:
        1. Clear sources and check previously added cannot be retrieved.
    """
    service = initialize_configured_service()
    assert service.add_source("file",WAV_FILE_PATH,RESULT_DIR_PATH)
    assert service.clear_sources()
    assert service.add_source("file",WAV_FILE_PATH,RESULT_DIR_PATH)
    assert service.clear_sources()


def test_organizer_service_create_new_settings_profile() -> None:
    """
    Tests:
        1. Create a profile with incomplete data.
        2. Create a profile with complete data.
        3. Create a profile with a repeated name.
    """
    service = initialize_configured_service()
    assert not service.create_new_settings_profile("s1",{})
    assert service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    assert not service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    service.clear_sources()

def test_organizer_service_save_settings_profile() -> None:
    """
    Tests:
        1. Save invalid profile.
        2. Save profile that exists.
    """
    service = initialize_configured_service()
    service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    assert not service.save_settings_profile("invalid")
    assert service.save_settings_profile("s1")
    service.remove_settings_profile("s1")
    assert service.clear_sources()


def test_organizer_service_remove_settings_profile() -> None:
    """
    Tests:
        1. Remove invalid profile.
        2. Remove valid profile and associated source.
    """
    service = initialize_configured_service()
    service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    service.add_source("file",WAV_FILE_PATH,RESULT_DIR_PATH)
    service.apply_settings_profile_to_source("file","s1")
    assert not service.remove_settings_profile("invalid")
    assert service.remove_settings_profile("s1")
    assert not service.is_source("file")


def test_organizer_service_remove_all_settings_profiles() -> None:
    """
    Tests:
        2. Remove all profiles and associated source.
    """
    service = initialize_configured_service()
    service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    service.create_new_settings_profile(
        "s2",obtain_settings_profile_data())
    service.add_source("file",WAV_FILE_PATH,RESULT_DIR_PATH)
    service.add_source("file2",WAV_FILE_PATH,RESULT_DIR_PATH)
    service.apply_settings_profile_to_source("file","s1")
    service.apply_settings_profile_to_source("file2","s2")
    assert service.remove_all_settings_profiles()
    assert not service.is_source("file")
    assert not service.is_source("file2")

def test_organizer_service_change_settings_profile_name() -> None:
    """
    Tests:
        1. Change the name of settings that does not exist.
        2. Change the name of existing settings and check that source settings
            name also changed.
    """
    service = initialize_configured_service()
    service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    assert service.add_source("file",WAV_FILE_PATH,RESULT_DIR_PATH)
    assert service.is_source("file")
    service.apply_settings_profile_to_source("file","s1")
    assert not service.change_settings_profile_name("s2","s3")
    assert service.change_settings_profile_name("s1","s2")
    assert service.get_source_settings_profile_name("file") == "s2"
    service.clear_sources()
    service.remove_settings_profile("s2")

def test_organizer_service_apply_settings_profile_to_source() -> None:
    """
    Tests:
        1. Apply a settings that does not exist.
        2. Apply to a source that does not exist.
        3. Apply profile to un-configured source.
        4. Apply profile to configured source.
    """
    service = initialize_configured_service()
    service.add_source("file",WAV_FILE_PATH,RESULT_DIR_PATH)
    assert not service.apply_settings_profile_to_source("file","invalid")
    service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    assert not service.apply_settings_profile_to_source("invalid","s1")
    assert service.apply_settings_profile_to_source("file","s1")
    service.create_new_settings_profile(
        "s2",obtain_settings_profile_data())
    assert service.apply_settings_profile_to_source("file","s2")
    service.remove_settings_profile("s1")
    service.remove_settings_profile("s2")
    assert service.clear_sources()

def test_organizer_service_save_source_settings_profile() -> None:
    """
    Tests:
        1. Save source profile as existing name.
        2. Save profile with new name.
        3. Check that source has updated profile.
    """
    service = initialize_configured_service()
    service.add_source("file",WAV_FILE_PATH,RESULT_DIR_PATH)
    service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    service.apply_settings_profile_to_source("file","s1")
    assert not service.save_source_settings_profile("invalid","new")
    assert service.save_source_settings_profile("file","s2")
    assert service.get_source_settings_profile_name("file") == "s2"
    service.remove_settings_profile("s1")
    service.remove_settings_profile("s2")
    service.clear_sources()

def test_organizer_service_is_source() -> None:
    """
    Tests:
        1. Check an added source exists.
        2. Check unknown source does not exist.
    """
    service = initialize_configured_service()
    service.add_source("file",WAV_FILE_PATH,RESULT_DIR_PATH)
    assert service.is_source("file")
    assert not service.is_source("dir")
    service.clear_sources()

def test_organizer_service_is_source_configured() -> None:
    """
    Tests:
        1. Check an invalid source.
        2. Check a configured source.
        3. Check an un-configured source
    """
    service = initialize_configured_service()
    service.add_source("file",WAV_FILE_PATH,RESULT_DIR_PATH)
    service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    assert not service.is_source_configured("file")
    service.apply_settings_profile_to_source("file","s1")
    assert service.is_source_configured("file")
    assert not service.is_source_configured("invalid")
    service.clear_sources()
    service.remove_settings_profile("s1")

def test_organizer_service_get_source_names() -> None:
    """
    Tests:
        1. Check before adding any sources.
        2. Check after adding sources.
    """
    service = initialize_configured_service()
    assert len(service.get_source_names()) == 0
    service.add_source("file",WAV_FILE_PATH,RESULT_DIR_PATH)
    assert service.get_source_names() == ["file"]
    service.clear_sources()

def test_organizer_service_get_configured_source_names() -> None:
    service = initialize_configured_service()
    assert len(service.get_configured_source_names()) == 0
    service.add_source("file",WAV_FILE_PATH,RESULT_DIR_PATH)
    assert len(service.get_configured_source_names()) == 0
    service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    service.apply_settings_profile_to_source("file","s1")
    assert service.get_configured_source_names() == ["file"]
    service.clear_sources()
    service.remove_settings_profile("s1")

def test_organizer_service_get_source_details() -> None:
    """
    Tests:
        1. Get the details for an object that does not exist.
        2. Get details for an object that exists.
        3. Get details of source that exists and also has a settings profile.
    """
    service = initialize_configured_service()
    service.add_source("file",WAV_FILE_PATH,RESULT_DIR_PATH)
    service.add_source("file2",WAV_FILE_PATH,RESULT_DIR_PATH)
    service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    service.apply_settings_profile_to_source("file","s1")
    assert service.get_source_details("invalid") == None
    assert type(service.get_source_details("file")) == SourceDetails
    assert type(service.get_source_details("file2")) == SourceDetails
    service.clear_sources()
    service.remove_settings_profile("s1")

def test_organizer_service_get_sources_details() -> None:
    """
    Tests:
        1. Get source details of multiple sources some existing and some invalid.
    """
    service = initialize_configured_service()
    service.add_source("file",WAV_FILE_PATH,RESULT_DIR_PATH)
    service.add_source("file2",WAV_FILE_PATH,RESULT_DIR_PATH)
    assert list(service.get_sources_details(["file","file2"]).keys()) \
        == ["file","file2"]
    service.clear_sources()

def test_organizer_get_all_source_details() -> None:
    """
    Tests:
        1. Get all details.
    """
    service = initialize_configured_service()
    service.add_source("file",WAV_FILE_PATH,RESULT_DIR_PATH)
    service.add_source("file2",WAV_FILE_PATH,RESULT_DIR_PATH)
    assert list(service.get_all_source_details().keys()) == ["file","file2"]
    service.clear_sources()

def test_organizer_service_get_configured_source_conversation() -> None:
    """
    Tests:
        1. Get for an invalid source.
        2. Get for an un-configured source.
        3. Get for a configured source.
    """
    service = initialize_configured_service()
    service.add_source("file",WAV_FILE_PATH,RESULT_DIR_PATH)
    service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    assert service.get_configured_source_conversation("invalid") == None
    assert service.get_configured_source_conversation("file") == None
    service.apply_settings_profile_to_source("file","s1")
    assert type(service.get_configured_source_conversation("file")) \
        == Conversation
    service.clear_sources()
    service.remove_settings_profile("s1")

def test_organizer_service_get_configured_sources_conversations() -> None:
    """
    Tests:
        1. Get for some valid and some invalid sources.
    """
    service = initialize_configured_service()
    service.add_source("file",WAV_FILE_PATH,RESULT_DIR_PATH)
    service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    service.apply_settings_profile_to_source("file","s1")
    assert len(service.get_configured_sources_conversations(
        ["file","dir"]).values()) == 1
    service.clear_sources()

def test_organizer_service_get_all_configured_source_conversations() -> None:
    """
    Tests:
        1. Get for all sources.
    """
    service = initialize_configured_service()
    service.add_source("file",WAV_FILE_PATH,RESULT_DIR_PATH)
    service.add_source("file2",WAV_FILE_PATH,RESULT_DIR_PATH)
    service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    service.apply_settings_profile_to_source("file","s1")
    service.apply_settings_profile_to_source("file2","s1")
    assert list(service.get_all_configured_source_conversations().keys()) ==\
        ["file","file2"]


def test_organizer_service_is_settings_profile() -> None:
    """
    Tests:
        1. Check invalid profile.
        2. Check valid profile.
    """
    service = initialize_configured_service()
    service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    assert not service.is_settings_profile("invalid")
    assert service.is_settings_profile("s1")

def test_organizer_service_is_settings_profile_saved() -> None:
    """
    Tests:
        1. Check before saving new profile.
        2. Check after saving new profile.
    """
    service = initialize_configured_service()
    service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    assert not service.is_settings_profile_saved("s1")
    service.save_settings_profile("s1")
    assert service.is_settings_profile_saved("s1")
    service.remove_settings_profile("s1")

def test_organizer_service_get_settings_profile_details() -> None:
    """
    Tests:
        1. Get details for a profile that does not exist.
        2. Get details for a profile that does exist.
    """
    service = initialize_configured_service()
    service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    assert service.get_settings_profile_details("s2") == None
    assert type(service.get_settings_profile_details("s1")) == SettingDetails
    service.remove_settings_profile("s1")

def test_organizer_service_get_settings_profiles_details() -> None:
    """
    Tests:
        1. Get details for some settings that exist, and some that do not.
    """
    service = initialize_configured_service()
    service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    service.create_new_settings_profile(
        "s2",obtain_settings_profile_data())
    assert list(service.get_settings_profiles_details(["s1","s2"]).keys()) == \
        ["s1","s2"]
    service.remove_settings_profile("s1")
    service.remove_settings_profile("s2")

def test_organizer_service_get_all_settings_profiles_details() -> None:
    """
    Tests:
        1. Get settings details for all profiles.
    """
    service = initialize_configured_service()
    service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    service.create_new_settings_profile(
        "s2",obtain_settings_profile_data())
    assert list(service.get_all_settings_profiles_details().keys()) \
            == ["s1","s2"]
    service.remove_settings_profile("s1")
    service.remove_settings_profile("s2")


def test_organizer_service_get_source_settings_profile_name() -> None:
    """
    Tests:
        1. Check before applying profile to source.
        2. Check after applying profile to source.
    """
    service = initialize_configured_service()
    service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    service.add_source("file",WAV_FILE_PATH,RESULT_DIR_PATH)
    assert service.get_source_settings_profile_name("file") == None
    service.apply_settings_profile_to_source("file","s1")
    assert service.get_source_settings_profile_name("file") == "s1"
    service.clear_sources()
    service.remove_settings_profile("s1")

def test_organizer_service_get_source_names_using_settings_profile() -> None:
    """
    Tests:
        1. Get for invaid sources.
        2. Get for valid sources.
    """
    service = initialize_configured_service()
    assert service.add_source("file",WAV_FILE_PATH,RESULT_DIR_PATH)
    assert service.add_source("dir",CONV_DIR_PATH,RESULT_DIR_PATH)
    service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    service.create_new_settings_profile(
        "s2",obtain_settings_profile_data())
    service.apply_settings_profile_to_source("file","s1")
    service.apply_settings_profile_to_source("dir","s1")
    assert service.get_source_names_using_settings_profile("s1") == ["file","dir"]
    assert service.get_source_names_using_settings_profile("s2") == []
    service.remove_settings_profile("s1")
    service.remove_settings_profile("s2")
    service.clear_sources()

def test_organizer_service_get_sources_details_using_settings_profile() -> None:
    """
    Tests:
        1. Get for an invalid settings profile.
        2. Get for valid settings profile.
    """
    service = initialize_configured_service()
    assert service.add_source("file",WAV_FILE_PATH,RESULT_DIR_PATH)
    assert service.add_source("dir",CONV_DIR_PATH,RESULT_DIR_PATH)
    service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    service.apply_settings_profile_to_source("file","s1")
    assert list(service.get_sources_details_using_settings_profile("s1").keys()) \
        == ["file"]
    assert len(service.get_sources_details_using_settings_profile("invalid").keys()) \
        == 0
    service.clear_sources()

def test_organizer_service_get_source_settings_profile_details() -> None:
    """
    Tests:
        1. Get the settings details for an invalid source.
        2. Get the settings details for a valid source.
        3. Get details for an un-configured source.
    """
    service = initialize_configured_service()
    service.add_source("file",WAV_FILE_PATH,RESULT_DIR_PATH)
    service.add_source("file2",WAV_FILE_PATH,RESULT_DIR_PATH)
    service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    service.apply_settings_profile_to_source("file","s1")
    assert type(service.get_source_settings_profile_details("file")) == \
        SettingDetails
    assert  service.get_source_settings_profile_details("invalid") == None
    assert  service.get_source_settings_profile_details("file2") == None
    service.clear_sources()

def test_organizer_service_get_all_sources_settings_profile_details() -> None:
    """
    Tests:
        1. Get details for all configured sources.
    """
    service = initialize_configured_service()
    service.add_source("file",WAV_FILE_PATH,RESULT_DIR_PATH)
    service.add_source("file2",WAV_FILE_PATH,RESULT_DIR_PATH)
    service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    service.apply_settings_profile_to_source("file","s1")
    assert list(service.get_all_sources_settings_profile_details().keys()) == \
        ["file"]
    service.clear_sources()

def test_organizer_service_set_settings_profile_attribute() -> None:
    """
    Tests:
        1. Change for an invalid settings profile.
        2. Change for a valid profile and check that all sources using it
            are also changed.
    """
    service = initialize_configured_service()
    service.add_source("file",WAV_FILE_PATH,RESULT_DIR_PATH)
    service.add_source("file2",WAV_FILE_PATH,RESULT_DIR_PATH)
    assert not service.set_settings_profile_attribute(
        "s1",GBSettingAttrs.engine_type,"google")
    service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    service.create_new_settings_profile(
        "s2",obtain_settings_profile_data())
    service.apply_settings_profile_to_source("file","s1")
    service.apply_settings_profile_to_source("file2","s2")
    service.set_settings_profile_attribute(
        "s1",GBSettingAttrs.engine_type,"google")
    settings_details : SettingDetails = service.get_settings_profile_details("s1")
    assert settings_details.values["engine_type"] == "google"
    conversation = service.get_configured_source_conversation("file")
    settings : GailBotSettings = conversation.get_settings()
    assert settings.get_engine_type() == "google"
    conversation2 = service.get_configured_source_conversation("file2")
    settings2 : GailBotSettings = conversation2.get_settings()
    assert settings2.get_engine_type() != "google"
    service.clear_sources()

def test_organizer_service_set_source_settings_profile_attribute() -> None:
    """
    Tests:
        1. Set for an invalid source.
        2. Set for a valid source and ensure the entire settings profile
            not changed.
    """
    service = initialize_configured_service()
    assert not service.set_source_settings_profile_attribute(
        "invalid",GBSettingAttrs.engine_type,"google")
    service.add_source("file",WAV_FILE_PATH,RESULT_DIR_PATH)
    service.create_new_settings_profile(
        "s1",obtain_settings_profile_data())
    service.apply_settings_profile_to_source("file","s1")
    service.set_source_settings_profile_attribute(
        "file",GBSettingAttrs.engine_type,"google")
    settings : GailBotSettings = service.get_configured_source_conversation(
        "file").get_settings()
    assert settings.get_engine_type() == "google"
    settings_details = service.get_settings_profile_details("s1")
    assert settings_details.values["engine_type"] != "google"
    service.clear_sources()


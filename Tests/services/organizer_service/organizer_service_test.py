# Standard library imports
from typing import Dict, Any, List
import pytest
from copy import deepcopy
from enum import Enum
# Local imports
from Src.components.io import IO
from Src.components.services import OrganizerService, FileSystemService, \
    SourceDetails, SettingsDetails, Source
from Src.components.organizer import Settings
from Tests.services.vardefs import *


############################### SETUP #####################################

TRANSCRIBER_NAME = "test"


def obtain_settings_profile_data() -> Dict:
    return {
        GBSettingAttrs.engine_type: "watson",
        GBSettingAttrs.watson_api_key: "MSgOPTS9CvbADe49nEg4wm8_gxeRuf4FGUmlHS9QqAw3",
        GBSettingAttrs.watson_language_customization_id: "41e54a38-2175-45f4-ac6a-1c11e42a2d54",
        GBSettingAttrs.watson_base_language_model: "en-US_BroadbandModel",
        GBSettingAttrs.watson_region: "dallas",
        GBSettingAttrs.analysis_plugins_to_apply: ["second_analysis"],
        GBSettingAttrs.output_format: "normal"}


class GBSettingAttrs(Enum):
    engine_type = "engine_type"
    watson_api_key = "watson_api_key"
    watson_language_customization_id = "watson_language_customization_id"
    watson_base_language_model = "watson_base_language_model"
    watson_region = "watson_region"
    output_format = "output_format"
    analysis_plugins_to_apply = "analysis_plugins_to_apply"


class GailBotSettings(Settings):

    def __init__(self, data: Dict[GBSettingAttrs, Any]) -> None:
        self.io = IO()
        self.save_extension = "json"
        self.attrs = list([x for x in GBSettingAttrs])
        self.data = dict()
        self.configured = False
        if not all([attr in data for attr in self.attrs]):
            return
        for attr in self.attrs:
            self.data[attr] = None
        for attr, value in data.items():
            self.set_value(attr, value)
        self.configured = True

    ############################ MODIFIERS ####################################

    def save_to_file(self, save_path: str) -> bool:
        try:
            path_with_extension = "{}.{}".format(
                save_path, self.save_extension)
            data = dict()
            for k, v in self.data.items():
                data[k.value] = v
            return self.io.write(path_with_extension, data, True)
        except Exception as e:
            print(e)
            return False

    ############################ SETTERS ####################################

    def set_value(self, attr: GBSettingAttrs, value: Any) -> bool:
        if self.has_attribute(attr) and \
                self.is_configured():
            self.data[attr] = value
            return True
        return False

    ############################ GETTERS ####################################

    def is_configured(self) -> bool:
        return self.configured

    def has_attribute(self, attr: GBSettingAttrs) -> bool:
        return attr in self.attrs

    def get_value(self, attr: GBSettingAttrs) -> Any:
        if self.has_attribute(attr) and \
                self.is_configured():
            return self.data[attr]

    def get_all_values(self) -> Dict:
        return deepcopy(self.data)


@pytest.fixture(scope='session', autouse=True)
def reset_workspace() -> None:
    io = IO()
    io.delete(RESULT_DIR_PATH)
    io.create_directory(RESULT_DIR_PATH)


def initialize_configured_service() -> OrganizerService:
    fs_service = FileSystemService()
    assert fs_service.configure_from_workspace_path(WS_DIR_PATH)
    service = OrganizerService(fs_service)
    service.add_settings_profile_type(
        "gb", lambda x: GailBotSettings(x))
    return service


########################## TEST DEFINITIONS ##################################


def test_configure_from_disk() -> None:
    pass


def test_organizer_service_add_source_valid() -> None:
    """
    Tests:
        1. Add a valid source and ensure conversation created from file.
        2. Add a valid source and ensure conversation created from directory.
    """
    service = initialize_configured_service()
    assert service.add_source("file", WAV_FILE_PATH,
                              RESULT_DIR_PATH, TRANSCRIBER_NAME)
    assert service.add_source("dir", CONV_DIR_PATH, RESULT_DIR_PATH,
                              TRANSCRIBER_NAME)
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
    assert service.add_source("file", WAV_FILE_PATH, RESULT_DIR_PATH, TRANSCRIBER_NAME
                              )
    assert service.remove_source("file")
    assert not service.remove_source("file")


def test_organizer_service_remove_sources() -> None:
    """
    Tests:
        1. Remove one existing and one invalid source.
        2. Remove all valid sources.
    """
    service = initialize_configured_service()
    service.add_source("file", WAV_FILE_PATH,
                       RESULT_DIR_PATH, TRANSCRIBER_NAME)
    assert not service.remove_sources(["file", "invalid"])
    assert service.add_source("file", WAV_FILE_PATH, RESULT_DIR_PATH,
                              TRANSCRIBER_NAME)
    assert service.add_source("dir", CONV_DIR_PATH, RESULT_DIR_PATH,
                              TRANSCRIBER_NAME)
    assert service.is_source("file")
    assert service.is_source("dir")
    assert service.remove_sources(["file", "dir"])


def test_organizer_service_clear_sources() -> None:
    """
    Tests:
        1. Clear sources and check previously added cannot be retrieved.
    """
    service = initialize_configured_service()
    assert service.add_source("file", WAV_FILE_PATH, RESULT_DIR_PATH,
                              TRANSCRIBER_NAME)
    assert service.clear_sources()
    assert service.add_source("file", WAV_FILE_PATH, RESULT_DIR_PATH,
                              TRANSCRIBER_NAME)
    assert service.clear_sources()


def test_reset_source() -> None:
    """
    Tests:
        1. Reset a valid source.
        2. Reset an invalid source.
    """
    service = initialize_configured_service()
    assert service.add_source("file", WAV_FILE_PATH, RESULT_DIR_PATH,
                              TRANSCRIBER_NAME)
    assert service.reset_source("file")
    assert not service.reset_source("invalid")


def test_reset_sources() -> None:
    """
    Tests:
        1. Reset only some sources.
    """
    service = initialize_configured_service()
    service.add_source("file", WAV_FILE_PATH, RESULT_DIR_PATH,
                       TRANSCRIBER_NAME)
    service.add_source("dir", CONV_DIR_PATH, RESULT_DIR_PATH,
                       TRANSCRIBER_NAME)
    assert service.reset_sources(["file", "dir"])


def reset_all_sources() -> None:
    """
    Tests:
        1. Reset all sources.
    """
    service = initialize_configured_service()
    service.add_source("file", WAV_FILE_PATH, RESULT_DIR_PATH,
                       TRANSCRIBER_NAME)
    service.add_source("dir", CONV_DIR_PATH, RESULT_DIR_PATH,
                       TRANSCRIBER_NAME)
    assert service.reset_all_sources()


def test_organizer_service_create_new_settings_profile() -> None:
    """
    Tests:
        1. Create a profile with incomplete data.
        2. Create a profile with complete data.
        3. Create a profile with a repeated name.
    """
    service = initialize_configured_service()
    assert not service.create_new_settings_profile("gb", "s1", {})
    assert service.create_new_settings_profile(
        "gb", "s1", obtain_settings_profile_data())
    assert not service.create_new_settings_profile(
        "gb", "s1", obtain_settings_profile_data())
    service.clear_sources()


def test_organizer_service_save_settings_profile() -> None:
    """
    Tests:
        1. Save invalid profile.
        2. Save profile that exists.
    """
    service = initialize_configured_service()
    service.create_new_settings_profile("gb",
                                        "s1", obtain_settings_profile_data())
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
    service.create_new_settings_profile("gb",
                                        "s1", obtain_settings_profile_data())
    service.add_source("file", WAV_FILE_PATH,
                       RESULT_DIR_PATH, TRANSCRIBER_NAME)
    service.apply_settings_profile_to_source("file", "s1")
    assert not service.remove_settings_profile("invalid")
    assert service.remove_settings_profile("s1")
    assert not service.is_source("file")


def test_organizer_service_remove_all_settings_profiles() -> None:
    """
    Tests:
        2. Remove all profiles and associated source.
    """
    service = initialize_configured_service()
    service.create_new_settings_profile("gb",
                                        "s1", obtain_settings_profile_data())
    service.create_new_settings_profile("gb",
                                        "s2", obtain_settings_profile_data())
    service.add_source("file", WAV_FILE_PATH,
                       RESULT_DIR_PATH, TRANSCRIBER_NAME)
    service.add_source("file2", WAV_FILE_PATH,
                       RESULT_DIR_PATH, TRANSCRIBER_NAME)
    service.apply_settings_profile_to_source("file", "s1")
    service.apply_settings_profile_to_source("file2", "s2")
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
    service.create_new_settings_profile("gb",
                                        "s1", obtain_settings_profile_data())
    assert service.add_source("file", WAV_FILE_PATH,
                              RESULT_DIR_PATH, TRANSCRIBER_NAME)
    assert service.is_source("file")
    service.apply_settings_profile_to_source("file", "s1")
    assert not service.change_settings_profile_name("s2", "s3")
    assert service.change_settings_profile_name("s1", "s2")
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
    service.add_source("file", WAV_FILE_PATH,
                       RESULT_DIR_PATH, TRANSCRIBER_NAME)
    assert not service.apply_settings_profile_to_source("file", "invalid")
    service.create_new_settings_profile("gb",
                                        "s1", obtain_settings_profile_data())
    assert not service.apply_settings_profile_to_source("invalid", "s1")
    assert service.apply_settings_profile_to_source("file", "s1")
    service.create_new_settings_profile("gb",
                                        "s2", obtain_settings_profile_data())
    assert service.apply_settings_profile_to_source("file", "s2")
    service.remove_settings_profile("s1")
    service.remove_settings_profile("s2")
    assert service.clear_sources()


def test_apply_settings_profile_to_sources() -> None:
    """
    Tests:
        1. Apply a new settings profile to multiple sources.
    """
    service = initialize_configured_service()
    service.add_source("file", WAV_FILE_PATH,
                       RESULT_DIR_PATH, TRANSCRIBER_NAME)
    service.add_source("dir", CONV_DIR_PATH, RESULT_DIR_PATH, TRANSCRIBER_NAME)
    service.create_new_settings_profile("gb",
                                        "s1", obtain_settings_profile_data())
    assert service.apply_settings_profile_to_sources(["file", "dir"], "s1")


def test_organizer_service_save_source_settings_profile() -> None:
    """
    Tests:
        1. Save source profile as existing name.
        2. Save profile with new name.
        3. Check that source has updated profile.
    """
    service = initialize_configured_service()
    service.add_source("file", WAV_FILE_PATH,
                       RESULT_DIR_PATH, TRANSCRIBER_NAME)
    service.create_new_settings_profile("gb",
                                        "s1", obtain_settings_profile_data())
    service.apply_settings_profile_to_source("file", "s1")
    assert not service.save_source_settings_profile("invalid", "new")
    assert service.save_source_settings_profile("file", "s2")
    assert service.get_source_settings_profile_name("file") == "s2"
    service.remove_settings_profile("s1")
    service.remove_settings_profile("s2")
    service.clear_sources()


# def test_get_supported_audio_formats() -> None:
#     """
#     Tests:
#         1. Make sure more than one format is supported.
#     """
#     service = initialize_configured_service()
#     assert len(service.get_supported_audio_formats()) > 0


# def test_get_supported_video_formats() -> None:
#     """
#     Tests:
#         1. Make sure more than one format is supported.
#     """
#     service = initialize_configured_service()
#     assert len(service.get_supported_video_formats()) > 0


def test_organizer_service_is_source() -> None:
    """
    Tests:
        1. Check an added source exists.
        2. Check unknown source does not exist.
    """
    service = initialize_configured_service()
    service.add_source("file", WAV_FILE_PATH,
                       RESULT_DIR_PATH, TRANSCRIBER_NAME)
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
    service.add_source("file", WAV_FILE_PATH,
                       RESULT_DIR_PATH, TRANSCRIBER_NAME)
    service.create_new_settings_profile("gb",
                                        "s1", obtain_settings_profile_data())
    assert not service.is_source_configured("file")
    service.apply_settings_profile_to_source("file", "s1")
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
    service.add_source("file", WAV_FILE_PATH,
                       RESULT_DIR_PATH, TRANSCRIBER_NAME)
    assert service.get_source_names() == ["file"]
    service.clear_sources()


def test_organizer_service_get_configured_source_names() -> None:
    """
    Tests:
        1. Check before adding and configuring.
        2. Check after adding and configuring.
    """
    service = initialize_configured_service()
    assert len(service.get_configured_source_names()) == 0
    service.add_source("file", WAV_FILE_PATH,
                       RESULT_DIR_PATH, TRANSCRIBER_NAME)
    assert len(service.get_configured_source_names()) == 0
    service.create_new_settings_profile("gb",
                                        "s1", obtain_settings_profile_data())
    assert service.apply_settings_profile_to_source("file", "s1")
    assert service.get_configured_source_names() == ["file"]
    service.clear_sources()
    service.remove_settings_profile("s1")


# def test_organizer_service_get_source_details() -> None:
#     """
#     Tests:
#         1. Get the details for an object that does not exist.
#         2. Get details for an object that exists.
#         3. Get details of source that exists and also has a settings profile.
#     """
#     service = initialize_configured_service()
#     service.add_source("file", WAV_FILE_PATH,
#                        RESULT_DIR_PATH, TRANSCRIBER_NAME)
#     service.add_source("file2", WAV_FILE_PATH,
#                        RESULT_DIR_PATH, TRANSCRIBER_NAME)
#     service.create_new_settings_profile("gb",
#                                         "s1", obtain_settings_profile_data())
#     service.apply_settings_profile_to_source("file", "s1")
#     assert service.get_source_details("invalid") == None
#     assert type(service.get_source_details("file")) == SourceDetails
#     assert type(service.get_source_details("file2")) == SourceDetails
#     service.clear_sources()
#     service.remove_settings_profile("s1")


# def test_organizer_service_get_sources_details() -> None:
#     """
#     Tests:
#         1. Get source details of multiple sources some existing and some invalid.
#     """
#     service = initialize_configured_service()
#     service.add_source("file", WAV_FILE_PATH,
#                        RESULT_DIR_PATH, TRANSCRIBER_NAME)
#     service.add_source("file2", WAV_FILE_PATH,
#                        RESULT_DIR_PATH, TRANSCRIBER_NAME)
#     assert list(service.get_sources_details(["file", "file2"]).keys()) \
#         == ["file", "file2"]
#     service.clear_sources()


# def test_organizer_get_all_source_details() -> None:
#     """
#     Tests:
#         1. Get all details.
#     """
#     service = initialize_configured_service()
#     service.add_source("file", WAV_FILE_PATH,
#                        RESULT_DIR_PATH, TRANSCRIBER_NAME)
#     service.add_source("file2", WAV_FILE_PATH,
#                        RESULT_DIR_PATH, TRANSCRIBER_NAME)
#     assert list(service.get_all_source_details().keys()) == ["file", "file2"]
#     service.clear_sources()


def test_get_configured_sources() -> None:
    """
    Tests:
        1. Check that only configured sources are obtained.
    """
    service = initialize_configured_service()
    service.add_source("file", WAV_FILE_PATH,
                       RESULT_DIR_PATH, TRANSCRIBER_NAME)
    service.add_source("file2", WAV_FILE_PATH,
                       RESULT_DIR_PATH, TRANSCRIBER_NAME)
    service.create_new_settings_profile("gb",
                                        "s1", obtain_settings_profile_data())
    service.apply_settings_profile_to_source("file", "s1")
    assert list(service.get_configured_sources().keys()) == ["file"]


def test_organizer_service_is_settings_profile() -> None:
    """
    Tests:
        1. Check invalid profile.
        2. Check valid profile.
    """
    service = initialize_configured_service()
    service.create_new_settings_profile("gb",
                                        "s1", obtain_settings_profile_data())
    assert not service.is_settings_profile("invalid")
    assert service.is_settings_profile("s1")


def test_organizer_service_is_settings_profile_saved() -> None:
    """
    Tests:
        1. Check before saving new profile.
        2. Check after saving new profile.
    """
    service = initialize_configured_service()
    service.create_new_settings_profile("gb",
                                        "s1", obtain_settings_profile_data())
    assert not service.is_settings_profile_saved("s1")
    assert service.save_settings_profile("s1")
    assert service.is_settings_profile_saved("s1")
    assert service.remove_settings_profile("s1")


# def test_organizer_service_get_settings_profile_details() -> None:
#     """
#     Tests:
#         1. Get details for a profile that does not exist.
#         2. Get details for a profile that does exist.
#     """
#     service = initialize_configured_service()
#     service.create_new_settings_profile("gb",
#                                         "s1", obtain_settings_profile_data())
#     assert service.get_settings_profile_details("s2") == None
#     assert type(service.get_settings_profile_details("s1")) == SettingsDetails
#     service.remove_settings_profile("s1")


# def test_organizer_service_get_settings_profiles_details() -> None:
#     """
#     Tests:
#         1. Get details for some settings that exist, and some that do not.
#     """
#     service = initialize_configured_service()
#     service.create_new_settings_profile("gb",
#                                         "s1", obtain_settings_profile_data())
#     service.create_new_settings_profile("gb",
#                                         "s2", obtain_settings_profile_data())
#     assert list(service.get_settings_profiles_details(["s1", "s2"]).keys()) == \
#         ["s1", "s2"]
#     service.remove_settings_profile("s1")
#     service.remove_settings_profile("s2")


# def test_organizer_service_get_all_settings_profiles_details() -> None:
#     """
#     Tests:
#         1. Get settings details for all profiles.
#     """
#     service = initialize_configured_service()
#     service.create_new_settings_profile("gb",
#                                         "s1", obtain_settings_profile_data())
#     service.create_new_settings_profile("gb",
#                                         "s2", obtain_settings_profile_data())
#     assert list(service.get_all_settings_profiles_details().keys()) \
#         == ["s1", "s2"]
#     service.remove_settings_profile("s1")
#     service.remove_settings_profile("s2")


def test_organizer_service_get_source_settings_profile_name() -> None:
    """
    Tests:
        1. Check before applying profile to source.
        2. Check after applying profile to source.
    """
    service = initialize_configured_service()
    service.create_new_settings_profile("gb",
                                        "s1", obtain_settings_profile_data())
    service.add_source("file", WAV_FILE_PATH,
                       RESULT_DIR_PATH, TRANSCRIBER_NAME)
    assert service.get_source_settings_profile_name("file") == None
    service.apply_settings_profile_to_source("file", "s1")
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
    assert service.add_source("file", WAV_FILE_PATH,
                              RESULT_DIR_PATH, TRANSCRIBER_NAME)
    assert service.add_source("dir", CONV_DIR_PATH,
                              RESULT_DIR_PATH, TRANSCRIBER_NAME)
    service.create_new_settings_profile("gb",
                                        "s1", obtain_settings_profile_data())
    service.create_new_settings_profile("gb",
                                        "s2", obtain_settings_profile_data())
    service.apply_settings_profile_to_source("file", "s1")
    service.apply_settings_profile_to_source("dir", "s1")
    assert service.get_source_names_using_settings_profile("s1") == [
        "file", "dir"]
    assert service.get_source_names_using_settings_profile("s2") == []
    service.remove_settings_profile("s1")
    service.remove_settings_profile("s2")
    service.clear_sources()


# def test_organizer_service_get_sources_details_using_settings_profile() -> None:
#     """
#     Tests:
#         1. Get for an invalid settings profile.
#         2. Get for valid settings profile.
#     """
#     service = initialize_configured_service()
#     assert service.add_source("file", WAV_FILE_PATH,
#                               RESULT_DIR_PATH, TRANSCRIBER_NAME)
#     assert service.add_source("dir", CONV_DIR_PATH,
#                               RESULT_DIR_PATH, TRANSCRIBER_NAME)
#     service.create_new_settings_profile("gb",
#                                         "s1", obtain_settings_profile_data())
#     service.apply_settings_profile_to_source("file", "s1")
#     assert list(service.get_sources_details_using_settings_profile("s1").keys()) \
#         == ["file"]
#     assert len(service.get_sources_details_using_settings_profile("invalid").keys()) \
#         == 0
#     service.clear_sources()


# def test_organizer_service_get_source_settings_profile_details() -> None:
#     """
#     Tests:
#         1. Get the settings details for an invalid source.
#         2. Get the settings details for a valid source.
#         3. Get details for an un-configured source.
#     """
#     service = initialize_configured_service()
#     service.add_source("file", WAV_FILE_PATH,
#                        RESULT_DIR_PATH, TRANSCRIBER_NAME)
#     service.add_source("file2", WAV_FILE_PATH,
#                        RESULT_DIR_PATH, TRANSCRIBER_NAME)
#     service.create_new_settings_profile("gb",
#                                         "s1", obtain_settings_profile_data())
#     service.apply_settings_profile_to_source("file", "s1")
#     assert type(service.get_source_settings_profile_details("file")) == \
#         SettingsDetails
#     assert service.get_source_settings_profile_details("invalid") == None
#     assert service.get_source_settings_profile_details("file2") == None
#     service.clear_sources()


# def test_organizer_service_get_all_sources_settings_profile_details() -> None:
#     """
#     Tests:
#         1. Get details for all configured sources.
#     """
#     service = initialize_configured_service()
#     service.add_source("file", WAV_FILE_PATH,
#                        RESULT_DIR_PATH, TRANSCRIBER_NAME)
#     service.add_source("file2", WAV_FILE_PATH,
#                        RESULT_DIR_PATH, TRANSCRIBER_NAME)
#     service.create_new_settings_profile("gb",
#                                         "s1", obtain_settings_profile_data())
#     service.apply_settings_profile_to_source("file", "s1")
#     assert list(service.get_all_sources_settings_profile_details().keys()) == \
#         ["file"]
#     service.clear_sources()


# def test_organizer_service_set_settings_profile_attribute() -> None:
#     """
#     Tests:
#         1. Change for an invalid settings profile.
#         2. Change for a valid profile and check that all sources using it
#             are also changed.
#     """
#     service = initialize_configured_service()
#     service.add_source("file", WAV_FILE_PATH,
#                        RESULT_DIR_PATH, TRANSCRIBER_NAME)
#     service.add_source("file2", WAV_FILE_PATH,
#                        RESULT_DIR_PATH, TRANSCRIBER_NAME)
#     assert not service.set_settings_profile_attribute(
#         "s1", GBSettingAttrs.engine_type, "google")
#     service.create_new_settings_profile("gb",
#                                         "s1", obtain_settings_profile_data())
#     service.create_new_settings_profile("gb",
#                                         "s2", obtain_settings_profile_data())
#     service.apply_settings_profile_to_source("file", "s1")
#     service.apply_settings_profile_to_source("file2", "s2")
#     service.set_settings_profile_attribute(
#         "s1", GBSettingAttrs.engine_type, "google")
#     settings_details: SettingsDetails = service.get_settings_profile_details(
#         "s1")
#     assert settings_details.values["engine_type"] == "google"
#     sources = service.get_configured_sources()
#     source: Source = sources["file"]
#     conversation = source.conversation
#     settings: GailBotSettings = conversation.get_settings()
#     assert settings.get_engine_type() == "google"
#     source2 = sources["file2"]
#     conversation2 = source2.conversation
#     settings2: GailBotSettings = conversation2.get_settings()
#     assert settings2.get_engine_type() != "google"
#     service.clear_sources()


# def test_organizer_service_set_source_settings_profile_attribute() -> None:
#     """
#     Tests:
#         1. Set for an invalid source.
#         2. Set for a valid source and ensure the entire settings profile
#             not changed.
#     """
#     service = initialize_configured_service()
#     assert not service.set_source_settings_profile_attribute(
#         "invalid", GBSettingAttrs.engine_type, "google")
#     service.add_source("file", WAV_FILE_PATH,
#                        RESULT_DIR_PATH, TRANSCRIBER_NAME)
#     service.create_new_settings_profile("gb",
#                                         "s1", obtain_settings_profile_data())
#     service.apply_settings_profile_to_source("file", "s1")
#     service.set_source_settings_profile_attribute(
#         "file", GBSettingAttrs.engine_type, "google")
#     sources = service.get_configured_sources()
#     source: Source = sources["file"]
#     settings: GailBotSettings = source.conversation.get_settings()
#     assert settings.get_engine_type() == "google"
#     settings_details = service.get_settings_profile_details("s1")
#     assert settings_details.values["engine_type"] != "google"
#     service.clear_sources()


from typing import Dict
from Src.components.controller import GailBotController, GBSettingAttrs, \
    GailBotSettings
from Src.components.io import IO
from Tests.controller.vardefs import *
import pytest

############################### GLOBALS #####################################


############################### SETUP #####################################

def obtain_settings_profile_data() -> Dict:
    return {
        GBSettingAttrs.engine_type: "watson",
        GBSettingAttrs.watson_api_key: WATSON_API_KEY,
        GBSettingAttrs.watson_language_customization_id: WATSON_LANG_CUSTOM_ID,
        GBSettingAttrs.watson_base_language_model: WATSON_BASE_LANG_MODEL,
        GBSettingAttrs.watson_region: WATSON_REGION,
        GBSettingAttrs.analysis_plugins_to_apply: ['tcu_analysis', 'second_analysis'],
        GBSettingAttrs.output_format: "normal"}


@pytest.fixture(scope='session', autouse=True)
def reset_workspace() -> None:
    io = IO()
    io.delete(RESULT_DIR_PATH)
    io.create_directory(RESULT_DIR_PATH)

########################## TEST DEFINITIONS ##################################


def test_initialize() -> None:
    """
    Tests:
        1. Initialize from valid source.
        2. Initialize  using invalid path.
    """
    try:
        GailBotController(MP3_FILE_PATH)
        assert False
    except:
        pass
    try:
        GailBotController(WS_DIR_PATH)
    except:
        assert False


def test_shutdown() -> None:
    """
    Tests:
        1. Shutdown after initializing.
    """
    controller = GailBotController(WS_DIR_PATH)
    controller.shutdown()


def test_add_source() -> None:
    """
    Tests:
        1. Add a valid audio file.
        2. Add a valid video file.
        3. Add a valid directory.
        4. Add an invalid file type.
        5. Add an invalid source.
        6. Add a source with an existing identifier.
    """
    controller = GailBotController(WS_DIR_PATH)
    assert controller.add_source("audio", MP3_FILE_PATH, RESULT_DIR_PATH)
    assert controller.add_source("video", MOV_FILE_PATH, RESULT_DIR_PATH)
    assert controller.add_source("mixed", MIXED_DIR_PATH, RESULT_DIR_PATH)
    assert not controller.add_source(
        "invalid_type", ANALYSIS_PLUGINS_CONFIG, RESULT_DIR_PATH)
    assert not controller.add_source(
        "invalid_path", "invalid", RESULT_DIR_PATH)
    assert not controller.add_source("audio", MP3_FILE_PATH, RESULT_DIR_PATH)


def test_remove_source() -> None:
    """
    Tests:
        1. Remove valid added source.
        2. Remove invalid source.
    """
    controller = GailBotController(WS_DIR_PATH)
    assert controller.add_source("audio", MP3_FILE_PATH, RESULT_DIR_PATH)
    assert controller.remove_source("audio")
    assert not controller.remove_source("audio")


def test_remove_sources() -> None:
    """
    Tests:
        1. Remove some valid and some invalid sources.
        2. Remove all valid sources.
    """
    controller = GailBotController(WS_DIR_PATH)
    assert controller.add_source("audio", MP3_FILE_PATH, RESULT_DIR_PATH)
    assert controller.add_source("video", MOV_FILE_PATH, RESULT_DIR_PATH)
    assert not controller.remove_sources(["audio", "invalid"])
    assert controller.add_source("audio", MP3_FILE_PATH, RESULT_DIR_PATH)
    assert controller.remove_sources(["audio", "video"])


def test_clear_sources() -> None:
    """
    Tests:
        1. Run the method before adding sources.
        2. Run after adding sources.
    """
    controller = GailBotController(WS_DIR_PATH)
    controller.clear_sources()
    assert controller.add_source("audio", MP3_FILE_PATH, RESULT_DIR_PATH)
    assert controller.add_source("video", MOV_FILE_PATH, RESULT_DIR_PATH)
    controller.clear_sources()
    assert not controller.is_source("audio")
    assert not controller.is_source("video")


def test_reset_source() -> None:
    """
    Tests:
        1. Reset a source without adding it.
        2. Reset a source after applying a settings profile.
    """
    controller = GailBotController(WS_DIR_PATH)
    assert controller.add_source("audio", MP3_FILE_PATH, RESULT_DIR_PATH)
    assert controller.reset_source("audio")
    controller.create_new_settings_profile(
        "s1", obtain_settings_profile_data())
    assert controller.apply_settings_profile_to_source("audio", "s1")
    # assert controller.get_source_settings_profile_details("audio").profile_name == \
    #     "s1"
    assert controller.reset_source("audio")
    #assert controller.get_source_settings_profile_details("audio") == None


def test_create_new_settings_profile() -> None:
    """
    Tests:
        1. Create a new settings profile with valid data.
        2. Create a new settings profile with invalid data.
        3. Create a settings profile with existing identifier.
    """
    controller = GailBotController(WS_DIR_PATH)
    assert controller.create_new_settings_profile(
        "s1", obtain_settings_profile_data())
    assert not controller.create_new_settings_profile(
        "invalid", {})
    assert not controller.create_new_settings_profile(
        "s1", obtain_settings_profile_data())


def test_save_settings_profile() -> None:
    """
    Tests:
        1 Save a valid settings profile.
        2. Save an invalid settings profile.
    """
    controller = GailBotController(WS_DIR_PATH)
    assert controller.create_new_settings_profile(
        "s1", obtain_settings_profile_data())
    assert controller.save_settings_profile("s1")
    assert not controller.save_settings_profile("invalid")
    controller.remove_settings_profile("s1")


def test_remove_settings_profile() -> None:
    """
    Tests:
        1. Remove a settings profile that does not exist.
        2. Remove a settings profile that does exist.
    """
    controller = GailBotController(WS_DIR_PATH)
    assert controller.create_new_settings_profile(
        "s1", obtain_settings_profile_data())
    assert not controller.remove_settings_profile("invalid")
    assert controller.remove_settings_profile("s1")


def test_remove_all_settings_profiles() -> None:
    """
    Tests:
        1. Remove all settings profile.
    """
    controller = GailBotController(WS_DIR_PATH)
    assert controller.create_new_settings_profile(
        "s1", obtain_settings_profile_data())
    assert controller.create_new_settings_profile(
        "s2", obtain_settings_profile_data())
    assert controller.remove_all_settings_profile()
    assert not controller.is_settings_profile("s1")
    assert not controller.is_settings_profile("s2")


def test_change_settings_profile_name() -> None:
    """
    Tests:
        1. Change the name of an existing settings profile.
        2. Change the name of an invalid settings profile.
        3. Ensure sources using this settings profile also have changed name.
        4. Change valid profile name to an existing profile name
    """
    controller = GailBotController(WS_DIR_PATH)
    assert controller.add_source("audio", MP3_FILE_PATH, RESULT_DIR_PATH)
    assert controller.create_new_settings_profile(
        "s1", obtain_settings_profile_data())
    controller.apply_settings_profile_to_source("audio", "s1")
    assert controller.change_settings_profile_name("s1", "s2")
    # assert controller.get_source_settings_profile_details("audio").\
    #     profile_name == "s2"
    assert not controller.is_settings_profile("s1")
    assert not controller.change_settings_profile_name("invalid", "s2")
    assert controller.create_new_settings_profile(
        "s3", obtain_settings_profile_data())
    assert not controller.change_settings_profile_name("s2", "s3")


def test_apply_settings_profile_to_source() -> None:
    """
    Tests:
        1. Apply valid profile to valid source.
        2. Apply invalid profile to valid source.
        3. Apply valid profile to invalid source.
        4. Apply invalid profile to invalid source.
    """
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("audio", MP3_FILE_PATH, RESULT_DIR_PATH)
    controller.create_new_settings_profile(
        "s1", obtain_settings_profile_data())
    assert controller.apply_settings_profile_to_source("audio", "s1")
    assert not controller.apply_settings_profile_to_source(
        "audio", "invalid")
    assert not controller.apply_settings_profile_to_source(
        "invalid", "s1")
    assert not controller.apply_settings_profile_to_source(
        "invalid_source", "invalid_settings")


def test_apply_settings_profile_to_sources() -> None:
    """
    Tests:
        1. Apply valid profile to multiple valid sources.
        2. Apply invalid profile to multiple valid sources.
        3. Apply valid profile to some valid and some invalid sources.
    """
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("audio", MP3_FILE_PATH, RESULT_DIR_PATH)
    controller.add_source("video", MOV_FILE_PATH, RESULT_DIR_PATH)
    controller.create_new_settings_profile(
        "s1", obtain_settings_profile_data())
    assert controller.apply_settings_profile_to_sources(
        ["audio", "video"], "s1")
    assert not controller.apply_settings_profile_to_sources(
        ["audio", "video"], "invalid")
    assert not controller.apply_settings_profile_to_sources(
        ["audio", "invalid"], "s1")


def test_save_source_settings_profile() -> None:
    """
    Tests:
        1. Save valid source profile with unused profile name.
        2. Save invaid source profile.
        3. Save valid source profile with used profile name.
    """
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("audio", MP3_FILE_PATH, RESULT_DIR_PATH)
    controller.create_new_settings_profile(
        "s1", obtain_settings_profile_data())
    controller.apply_settings_profile_to_source("audio", "s1")
    assert controller.save_source_settings_profile("audio", "s2")
    assert not controller.save_source_settings_profile(
        "invalid", "doesnt_matter")
    assert not controller.save_source_settings_profile("audio", "s1")
    controller.remove_settings_profile("s2")


# def test_register_plugins() -> None:
#     """
#     Tests:
#         1. Register from a valid config path.
#         2. Register from invalid config path.
#         3. Register from invalid file contents.
#     """
#     controller = GailBotController(WS_DIR_PATH)
#     assert len(controller.register_analysis_plugins(
#         ANALYSIS_PLUGINS_CONFIG)) > 0
#     assert len(controller.register_analysis_plugins("invalid")) == 0
#     assert len(controller.register_analysis_plugins(EMPTY_JSON)) == 0


# def test_get_supported_source_formats() -> None:
#     """
#     Tests:
#         1. Check all the audio formats.
#     """
#     controller = GailBotController(WS_DIR_PATH)
#     assert len(controller.get_supported_audio_formats()) > 0


def test_is_source() -> None:
    """
    Tests:
        1. Check for valid source.
        2. Check for invalid source.
    """
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("audio", MP3_FILE_PATH, RESULT_DIR_PATH)
    assert controller.is_source("audio")
    assert not controller.is_source("invalid")


def test_is_source_ready_to_transcribe() -> None:
    """
    Tests:
        1. Check before setting source profile.
        2. Check after setting source profile.
        3. Check invalid source.
    """
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("audio", MP3_FILE_PATH, RESULT_DIR_PATH)
    assert not controller.is_source_ready_to_transcribe("audio")
    assert not controller.is_source_ready_to_transcribe("invalid")
    controller.create_new_settings_profile(
        "s1", obtain_settings_profile_data())
    controller.apply_settings_profile_to_source("audio", "s1")
    assert controller.is_source_ready_to_transcribe("audio")


def test_get_source_names() -> None:
    """
    Tests:
        1. Get the names of all added sources.
    """
    controller = GailBotController(WS_DIR_PATH)
    assert controller.get_source_names() == []
    controller.add_source("audio", MP3_FILE_PATH, RESULT_DIR_PATH)
    assert controller.get_source_names() == ["audio"]


def test_get_names_of_sources_ready_to_transcribe() -> None:
    """
    Tests:
        1. Check before and after applying settings profile.
    """
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("audio", MP3_FILE_PATH, RESULT_DIR_PATH)
    controller.create_new_settings_profile(
        "s1", obtain_settings_profile_data())
    assert controller.get_names_of_sources_ready_to_transcribe() == []
    controller.apply_settings_profile_to_source("audio", "s1")
    assert controller.get_names_of_sources_ready_to_transcribe() == ["audio"]


# def test_get_source_details() -> None:
#     """
#     Tests:
#         1. Get the details of a source that does not exist.
#         2. Get details of source that does exist.
#     """
#     controller = GailBotController(WS_DIR_PATH)
#     controller.add_source("audio", MP3_FILE_PATH, RESULT_DIR_PATH)
#     assert type(controller.get_source_details("audio")) == SourceDetails
#     assert controller.get_source_details("invalid") == None


# def test_get_sources_details() -> None:
#     """
#     Tests:
#         1. Get details of both valid and invalid sources.
#     """
#     controller = GailBotController(WS_DIR_PATH)
#     controller.add_source("audio", MP3_FILE_PATH, RESULT_DIR_PATH)
#     assert list(controller.get_sources_details(["audio", "invalid"]).keys()) == \
#         ["audio"]


# def test_get_all_source_details() -> None:
#     """
#     Tests:
#         1. Get the details of all sources.
#     """
#     controller = GailBotController(WS_DIR_PATH)
#     controller.add_source("audio", MP3_FILE_PATH, RESULT_DIR_PATH)
#     controller.add_source("video", MOV_FILE_PATH, RESULT_DIR_PATH)
#     assert list(controller.get_all_source_details().keys()) == \
#         ["audio", "video"]

def test_is_settings_profile() -> None:
    """
    Tests:
        1. Check valid profile.
        2. Check invalid profile.
    """
    controller = GailBotController(WS_DIR_PATH)
    controller.create_new_settings_profile(
        "s1", obtain_settings_profile_data())
    assert controller.is_settings_profile("s1")
    assert not controller.is_settings_profile("invalid")


def test_is_settings_profile_saved() -> None:
    """
    Tests:
        1. Check a saved profile.
        2. Check an invalid profile.
        3. Check a created but not saved profile.
    """
    controller = GailBotController(WS_DIR_PATH)
    controller.create_new_settings_profile(
        "s1", obtain_settings_profile_data())
    controller.create_new_settings_profile(
        "s2", obtain_settings_profile_data())
    assert controller.save_settings_profile("s1")
    assert controller.is_settings_profile_saved("s1")
    assert not controller.is_settings_profile_saved("s2")
    assert not controller.is_settings_profile_saved("invalid")
    controller.remove_settings_profile("s1")


# def test_get_settings_profile_details() -> None:
#     """
#     Tests:
#         1. Get for valid profile.
#         2. Get for invalid profile.
#     """
#     controller = GailBotController(WS_DIR_PATH)
#     controller.create_new_settings_profile(
#         "s1", obtain_settings_profile_data())
#     assert controller.get_settings_profile_details("invalid") == None
#     assert type(controller.get_settings_profile_details(
#         "s1")) == SettingsDetails


# def test_get_settings_profiles_details() -> None:
#     """
#     Tests:
#         1. Get some valid and some invalid profile details.
#     """
#     controller = GailBotController(WS_DIR_PATH)
#     controller.create_new_settings_profile(
#         "s1", obtain_settings_profile_data())
#     assert list(controller.get_settings_profiles_details(["s1", "invalid"]).keys()) == \
#         ["s1"]


# def test_get_all_settings_profiles_details() -> None:
#     """
#     Tests:
#         1. Get all profile details.
#     """
#     controller = GailBotController(WS_DIR_PATH)
#     controller.create_new_settings_profile(
#         "s1", obtain_settings_profile_data())
#     assert len(list(controller.get_all_settings_profiles_details().keys())) > 0


def test_get_source_settings_profile_name() -> None:
    """
    Tests:
        1. Get name for a source that does not have a profile.
        2. Get name for a source that does have a profile.
    """
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("audio", MP3_FILE_PATH, RESULT_DIR_PATH)
    controller.create_new_settings_profile(
        "s1", obtain_settings_profile_data())
    controller.apply_settings_profile_to_source("audio", "s1")
    assert controller.get_source_settings_profile_name("audio") == "s1"
    assert controller.get_source_settings_profile_name("invalid") == None


def test_get_source_names_using_settings_profile() -> None:
    """
    Tests:
        1. Get sources using the valid profile.
        2. Get sources using invalid profile.
    """
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("audio", MP3_FILE_PATH, RESULT_DIR_PATH)
    controller.add_source("video", MOV_FILE_PATH, RESULT_DIR_PATH)
    controller.create_new_settings_profile(
        "s1", obtain_settings_profile_data())
    controller.apply_settings_profile_to_source("audio", "s1")
    assert controller.get_source_names_using_settings_profile("s1") == [
        "audio"]
    assert controller.get_source_names_using_settings_profile("invalid") == []


def test_get_sources_details_using_settings_profile() -> None:
    """
    Tests:
        1. Get source details using valid profile.
    """
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("audio", MP3_FILE_PATH, RESULT_DIR_PATH)
    controller.add_source("video", MOV_FILE_PATH, RESULT_DIR_PATH)
    controller.create_new_settings_profile(
        "s1", obtain_settings_profile_data())
    controller.apply_settings_profile_to_source("audio", "s1")
    # assert list(controller.get_sources_details_using_settings_profile("s1").keys()) \
    #     == ["audio"]


# def test_get_source_settings_profile_details() -> None:
#     """
#     Tests:
#         1. Get the settings profile details of a valid source.
#         2. Get the  settings profile details of an invalid source.
#     """
#     controller = GailBotController(WS_DIR_PATH)
#     controller.add_source("audio", MP3_FILE_PATH, RESULT_DIR_PATH)
#     controller.create_new_settings_profile(
#         "s1", obtain_settings_profile_data())
#     controller.apply_settings_profile_to_source("audio", "s1")
#     assert type(controller.get_source_settings_profile_details("audio")) == \
#         SettingsDetails


# def test_get_sources_settings_profile_details() -> None:
#     """
#     Tests:
#         1. Get for some valid and invalid sources.
#     """
#     controller = GailBotController(WS_DIR_PATH)
#     controller.add_source("audio", MP3_FILE_PATH, RESULT_DIR_PATH)
#     controller.create_new_settings_profile(
#         "s1", obtain_settings_profile_data())
#     controller.apply_settings_profile_to_source("audio", "s1")
#     assert list(controller.get_sources_settings_profile_details(["audio", "invalid"]).keys()) == \
#         ["audio"]


# def test_get_all_sources_settings_profile_details() -> None:
#     """
#     Tests:
#         1. Get for all sources if they are configured.
#     """
#     controller = GailBotController(WS_DIR_PATH)
#     controller.add_source("audio", MP3_FILE_PATH, RESULT_DIR_PATH)
#     controller.add_source("video", MOV_FILE_PATH, RESULT_DIR_PATH)
#     controller.create_new_settings_profile(
#         "s1", obtain_settings_profile_data())
#     controller.apply_settings_profile_to_source("audio", "s1")
#     assert list(controller.get_all_sources_settings_profile_details().keys()) == \
#         ["audio"]


# def test_get_plugin_names() -> None:
#     """
#     Tests:
#         1. Get the names of all plugins.
#     """
#     controller = GailBotController(WS_DIR_PATH)
#     assert controller.get_analysis_plugin_names() == []
#     controller.register_analysis_plugins(ANALYSIS_PLUGINS_CONFIG)
#     assert len(controller.get_analysis_plugin_names()) > 0


def test_set_settings_profile_attribute() -> None:
    """
    Tests:
        1. Change the attribute of a valid profile and check if it is changed
        for all assciated sources.
        2. Change attribute for an invalid profile.
        3. Change an invalid attribute.
    """
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("audio", MP3_FILE_PATH, RESULT_DIR_PATH)
    controller.create_new_settings_profile(
        "s1", obtain_settings_profile_data())
    controller.apply_settings_profile_to_source("audio", "s1")
    assert controller.set_settings_profile_attribute(
        "s1", GBSettingAttrs.analysis_plugins_to_apply, ["test"])
    # assert controller.get_settings_profile_details("s1").\
    #     values[GBSettingAttrs.analysis_plugins_to_apply.value] == ["test"]
    # assert controller.get_source_settings_profile_details("audio").\
    #     values[GBSettingAttrs.analysis_plugins_to_apply.value] == ["test"]
    assert not controller.set_settings_profile_attribute(
        "invalid", GBSettingAttrs.analysis_plugins_to_apply, ["test"])
    assert not controller.set_settings_profile_attribute(
        "s2", "invalid", ["test"])


def test_set_source_settings_profile_attribute() -> None:
    """
    Tests:
        1. Set source settings profile attribute and check it is different from
        the original settings profile attribute.
        2. Set for a source that does not have a settings profile.
    """
    controller = GailBotController(WS_DIR_PATH)
    controller.add_source("audio", MP3_FILE_PATH, RESULT_DIR_PATH)
    controller.add_source("video", MOV_FILE_PATH, RESULT_DIR_PATH)
    controller.create_new_settings_profile(
        "s1", obtain_settings_profile_data())
    assert controller.apply_settings_profile_to_source("audio", "s1")
    assert controller.set_source_settings_profile_attribute(
        "audio", GBSettingAttrs.analysis_plugins_to_apply, ["test"])
    # assert controller.get_settings_profile_details("s1").\
    #     values[GBSettingAttrs.analysis_plugins_to_apply.value] != ["test"]
    assert not controller.set_source_settings_profile_attribute(
        "video", GBSettingAttrs.analysis_plugins_to_apply, ["test"])

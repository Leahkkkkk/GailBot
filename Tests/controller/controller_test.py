# Standard library imports
from Tests.controller.services.pipeline_service.pipeline_service_test import MIXED_CONV_DIR_PATH, MOV_FILE_PATH
from typing import List, Dict, Any
from Src.Components import controller
# Local imports
from Src.Components.controller import GailBotController, PipelineServiceSummary,\
                                SourceDetails,SettingDetails, GBSettingAttrs
############################### GLOBALS #####################################

WS_DIR_PATH = "TestData/workspace/fs_workspace"
WAV_FILE_PATH = "TestData/media/test2a.wav"
MP3_FILE_PATH = "TestData/media/sample1.mp3"
TXT_FILE_PATH = "TestData/configs/textfile.txt"
IMAGES_DIR_PATH = "TestData/images"
CONV_DIR_PATH = "TestData/media/small_conversation"
RESULT_DIR_PATH = "TestData/workspace/dir_2"
FORMAT_CONFIG_PATH = "TestData/plugins/normal_format_plugins/config.json"
ANALYSIS_CONFIG_PATH = "TestData/plugins/analysis_plugins/config.json"

############################### SETUP #######################################

def initialize_controller() -> GailBotController:
    return GailBotController(WS_DIR_PATH)

def get_settings_profile_data() -> Dict[GBSettingAttrs,Any]:
    return {
        GBSettingAttrs.engine_type : "watson",
        GBSettingAttrs.watson_api_key :
            "MSgOPTS9CvbADe49nEg4wm8_gxeRuf4FGUmlHS9QqAw3",
        GBSettingAttrs.watson_language_customization_id :
            "41e54a38-2175-45f4-ac6a-1c11e42a2d54",
        GBSettingAttrs.watson_base_language_model : "en-US_BroadbandModel",
        GBSettingAttrs.watson_region : "dallas"
    }

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
    """
    Tests:
        1. Remove an added source.
        2. Remove a source that has not been added.
    """
    controller = initialize_controller()
    assert not controller.remove_source("invalid")
    controller.add_source("file",MP3_FILE_PATH, RESULT_DIR_PATH)
    assert controller.remove_source("file")

def test_controller_remove_sources() -> None:
    """
    Tests:
        1. Remove some valid and come invalid sources.
    """
    controller = initialize_controller()
    controller.add_source("file",MP3_FILE_PATH, RESULT_DIR_PATH)
    controller.add_source("directory",CONV_DIR_PATH,RESULT_DIR_PATH)
    assert not controller.remove_sources(["file","invalid","directory"])
    controller.add_source("file",MP3_FILE_PATH, RESULT_DIR_PATH)
    controller.add_source("directory",CONV_DIR_PATH,RESULT_DIR_PATH)
    assert controller.remove_sources(["file","directory"])

def test_controller_clear_sources() -> None:
    """
    Tests:
        1. Remove all sources.
    """
    controller = initialize_controller()
    controller.add_source("file",MP3_FILE_PATH, RESULT_DIR_PATH)
    controller.add_source("directory",CONV_DIR_PATH,RESULT_DIR_PATH)
    assert controller.clear_sources()
    assert not controller.is_source("file")
    assert not controller.is_source("directory")

def test_controller_create_new_settings_profile() -> None:
    """
    Tests:
        1. Create a new profile with invalid data.
        2. Create a profile with correct data.
    """
    controller = initialize_controller()
    assert not controller.create_new_settings_profile(
        "custom", {"invalid" : 1})
    assert controller.create_new_settings_profile(
        "custom" , get_settings_profile_data())

def test_controller_save_settings_profile() -> None:
    """
    Tests:
        1. Save an invalid settings profile.
        2. Save a valid settings profile on disk and check if it can be deleted.
    """
    controller = initialize_controller()
    assert controller.create_new_settings_profile(
        "custom" , get_settings_profile_data())
    assert not controller.save_settings_profile("invalid")
    assert controller.save_settings_profile("custom")
    assert controller.remove_settings_profile("custom")

def test_controller_remove_settings_profile() -> None:
    """
    Tests:
        1. Remove invalid settings profile.
        2. Remove an existing settings profile that is saved on disk.
        3. Remove a settings profile that is not saved on disk.
    """
    controller = initialize_controller()
    controller.create_new_settings_profile(
        "disk" , get_settings_profile_data())
    controller.create_new_settings_profile(
        "non_disk" , get_settings_profile_data())
    controller.save_settings_profile("disk")
    assert not controller.remove_settings_profile("invalid")
    assert controller.remove_settings_profile("disk")
    assert controller.remove_settings_profile("non_disk")

def test_controller_remove_all_settings_profiles() -> None:
    """
    Tests:
        1. Remove all settings profile.
    """
    controller = initialize_controller()
    controller.create_new_settings_profile(
        "disk" , get_settings_profile_data())
    controller.create_new_settings_profile(
        "non_disk" , get_settings_profile_data())
    assert controller.remove_all_settings_profiles()
    assert not controller.is_settings_profile("disk")
    assert not controller.is_settings_profile("non_disk")

def test_controller_change_settings_profile_name() -> None:
    """
    Tests:
        1. Change name of an invalid profile.
        2. Change name of a profile that is not on disk.
        3. Change the name  of a profile that is saved on disk.
        4. Change the name of a profile saved on disk, and is applied to sources.
    """
    controller = initialize_controller()
    controller.create_new_settings_profile(
        "disk" , get_settings_profile_data())
    controller.save_settings_profile("disk")
    controller.create_new_settings_profile(
        "non_disk" , get_settings_profile_data())
    assert not controller.change_settings_profile_name("invalid","invalid")
    assert controller.change_settings_profile_name("disk","disk_changed")
    assert controller.is_settings_profile("disk_changed")
    assert controller.is_settings_profile_saved("disk_changed")
    assert not controller.is_settings_profile("disk")
    assert controller.change_settings_profile_name("non_disk","non_disk_changed")
    controller.add_source("file",MP3_FILE_PATH, RESULT_DIR_PATH)
    controller.add_source("directory",CONV_DIR_PATH,RESULT_DIR_PATH)
    controller.apply_settings_profile_to_source("file","disk_changed")
    controller.apply_settings_profile_to_source("directory","disk_changed")
    assert controller.change_settings_profile_name("disk_changed","disk")
    assert controller.get_source_settings_profile_name("file") == "disk"
    assert controller.get_source_settings_profile_name("directory") == "disk"
    controller.remove_all_settings_profiles()
    controller.clear_sources()

def test_controller_apply_settings_profile_to_source() -> None:
    """
    Tests:
        1. Apply a profile to an invalid source.
        2. Apply an invalid profile.
        3. Apply a profile to a source and check if it is there.
    """
    controller = initialize_controller()
    controller.add_source("file",MP3_FILE_PATH, RESULT_DIR_PATH)
    controller.create_new_settings_profile(
        "disk" , get_settings_profile_data())
    assert not controller.apply_settings_profile_to_source("invalid","disk")
    assert not controller.apply_settings_profile_to_source("file","invalid")
    assert controller.apply_settings_profile_to_source("file","disk")
    assert controller.get_source_settings_profile_name("file") == "disk"
    controller.remove_all_settings_profiles()
    controller.clear_sources()

def test_controller_save_source_settings_profile() -> None:
    """
    Tests:
        1. Save an invalid settings profile to disk.
        2. Save a valid profile to disk.
    """
    controller = initialize_controller()
    controller.create_new_settings_profile(
        "disk" , get_settings_profile_data())
    assert not controller.save_settings_profile("invalid")
    assert controller.save_settings_profile("disk")
    assert controller.is_settings_profile_saved("disk")
    controller.remove_all_settings_profiles()
    controller.clear_sources()

def test_register_analysis_plugins() -> None:
    """
    Tests:
        1. Register from valid path.
        2. Register from invalid path.
    """
    controller = initialize_controller()
    assert len(controller.register_analysis_plugins(ANALYSIS_CONFIG_PATH)) > 0
    assert len(controller.register_analysis_plugins("invalid")) == 0

def test_register_format() -> None:
    """
    Tests:
        1. Register from valid path.
        2. Register from invalid path.
    """
    controller = initialize_controller()
    name, plugin_names = controller.register_format(FORMAT_CONFIG_PATH)
    assert name == "normal"
    assert len(plugin_names) > 0

def test_transcribe_audio_source() -> None:
    """
    Tests:
        1. Test with a valid audio source.
    """
    controller = initialize_controller()
    controller.register_analysis_plugins(ANALYSIS_CONFIG_PATH)
    controller.register_format(FORMAT_CONFIG_PATH)
    controller.create_new_settings_profile(
        "disk" , get_settings_profile_data())
    controller.add_source("file",MP3_FILE_PATH,RESULT_DIR_PATH)
    controller.apply_settings_profile_to_source("file","disk")
    summary = controller.transcribe()
    print(summary)

def test_transcribe_video_source() -> None:
    """
    Tests:
        1. Test with a valid video source.
    """
    controller = initialize_controller()
    controller.register_analysis_plugins(ANALYSIS_CONFIG_PATH)
    controller.register_format(FORMAT_CONFIG_PATH)
    controller.create_new_settings_profile(
        "disk" , get_settings_profile_data())
    controller.add_source("file",MOV_FILE_PATH,RESULT_DIR_PATH)
    controller.apply_settings_profile_to_source("file","disk")
    summary = controller.transcribe()
    print(summary)

def test_transcribe_mixed_source() -> None:
    """
    Tests:
        1. Test with a valid mixed source.
    """
    controller = initialize_controller()
    controller.register_analysis_plugins(ANALYSIS_CONFIG_PATH)
    controller.register_format(FORMAT_CONFIG_PATH)
    controller.create_new_settings_profile(
        "disk" , get_settings_profile_data())
    controller.add_source("file",MIXED_CONV_DIR_PATH,RESULT_DIR_PATH)
    controller.apply_settings_profile_to_source("file","disk")
    summary = controller.transcribe()
    print(summary)

def test_transcribe_multiple_sources() -> None:
    """
    Tests:
        1. Transcribe from multiple sources.
    """
    controller = initialize_controller()
    controller.register_analysis_plugins(ANALYSIS_CONFIG_PATH)
    controller.register_format(FORMAT_CONFIG_PATH)
    controller.create_new_settings_profile(
        "disk" , get_settings_profile_data())
    controller.add_source("audio",MP3_FILE_PATH,RESULT_DIR_PATH)
    controller.add_source("video",MOV_FILE_PATH,RESULT_DIR_PATH)
    controller.add_source("mixed",MIXED_CONV_DIR_PATH,RESULT_DIR_PATH)
    controller.apply_settings_profile_to_source("audio","disk")
    controller.apply_settings_profile_to_source("video","disk")
    controller.apply_settings_profile_to_source("mixed","disk")
    summary = controller.transcribe()
    print(summary)

def test_controller_is_source() -> None:
    """
    Tests:
        1. Check an invalid source.
        2. Check a valid source.
    """
    controller = initialize_controller()
    controller.add_source("file",MP3_FILE_PATH, RESULT_DIR_PATH)
    assert not controller.is_source("invalid")
    assert controller.is_source("file")

def test_controller_is_source_ready_to_transcribe() -> None:
    """
    Tests:
        1. Check an invalid source.
        2. Check a source with no settings.
        3. Check a source with settings.
    """
    controller = initialize_controller()
    controller.add_source("file",MP3_FILE_PATH, RESULT_DIR_PATH)
    controller.create_new_settings_profile(
        "disk" , get_settings_profile_data())
    assert not controller.is_source_ready_to_transcribe("invalid")
    assert not controller.is_source_ready_to_transcribe("file")
    controller.apply_settings_profile_to_source("file","disk")
    assert controller.is_source_ready_to_transcribe("file")
    controller.remove_all_settings_profiles()
    controller.clear_sources()

def test_controller_get_source_names() -> None:
    """
    Tests:
        1. Obtain the names of all sources.
    """
    controller = initialize_controller()
    assert controller.get_source_names() == []
    controller.add_source("file",MP3_FILE_PATH, RESULT_DIR_PATH)
    controller.add_source("directory",CONV_DIR_PATH,RESULT_DIR_PATH)
    assert controller.get_source_names() == ["file","directory"]
    controller.remove_all_settings_profiles()
    controller.clear_sources()

def test_controller_get_names_of_sources_ready_to_transcribe() -> None:
    """
    Tests:
        1. Obtain the names of sources that are ready to transcribe.
    """
    controller = initialize_controller()
    controller.add_source("file",MP3_FILE_PATH, RESULT_DIR_PATH)
    controller.add_source("directory",CONV_DIR_PATH,RESULT_DIR_PATH)
    controller.create_new_settings_profile(
        "disk" , get_settings_profile_data())
    controller.apply_settings_profile_to_source("file","disk")
    assert controller.get_names_of_sources_ready_to_transcribe() == ["file"]
    controller.remove_all_settings_profiles()
    controller.clear_sources()

def test_controller_get_source_details() -> None:
    """
    Tests:
        1. Obtain the names of all source details.
    """
    controller = initialize_controller()
    controller.add_source("file",MP3_FILE_PATH, RESULT_DIR_PATH)
    assert type(controller.get_source_details("file")) == SourceDetails
    controller.remove_all_settings_profiles()
    controller.clear_sources()

def test_controller_get_all_source_details() -> None:
    """
    Tests:
        1. Get the details of all sources.
    """
    controller = initialize_controller()
    controller.add_source("file",MP3_FILE_PATH, RESULT_DIR_PATH)
    controller.add_source("directory",CONV_DIR_PATH,RESULT_DIR_PATH)
    assert list(controller.get_all_source_details().keys()) == ["file","directory"]
    controller.remove_all_settings_profiles()
    controller.clear_sources()

def test_controller_is_settings_profile() -> None:
    """
    Tests:
        1. Check an invalid profile.
        2. Check a valid profile.
    """
    controller = initialize_controller()
    assert not controller.is_settings_profile("invalid")
    controller.create_new_settings_profile(
        "disk" , get_settings_profile_data())
    assert controller.is_settings_profile("disk")
    controller.remove_all_settings_profiles()
    controller.clear_sources()

def test_controller_is_settings_profile_saved() -> None:
    """
    Tests:
        1. Check an invalid profile.
        2. Check an unsaved profile.
        3. Check a saved profile.
    """
    controller = initialize_controller()
    controller.create_new_settings_profile(
        "disk" , get_settings_profile_data())
    assert not controller.is_settings_profile_saved("invalid")
    assert not controller.is_settings_profile_saved("disk")
    controller.save_settings_profile("disk")
    assert controller.is_settings_profile_saved("disk")
    controller.remove_all_settings_profiles()
    controller.clear_sources()

def test_controller_get_settings_profile_details() -> None:
    """
    Tests:
        1. Get details of invalid profile.
        2. Get the details of a valid profile.
    """
    controller = initialize_controller()
    controller.create_new_settings_profile(
        "disk" , get_settings_profile_data())
    assert controller.get_settings_profile_details("invalid") == None
    assert type(controller.get_settings_profile_details("disk")) \
        == SettingDetails
    controller.remove_all_settings_profiles()
    controller.clear_sources()

def test_controller_get_all_settings_profile_details() -> None:
    """
    Tests:
        1. Obtain the details of all settings.
    """
    controller = initialize_controller()
    controller.create_new_settings_profile(
        "disk" , get_settings_profile_data())
    controller.create_new_settings_profile(
        "disk2" , get_settings_profile_data())
    assert list(controller.get_all_settings_profile_details().keys()) == \
        ["disk","disk2"]
    controller.remove_all_settings_profiles()
    controller.clear_sources()

def test_controller_get_source_settings_profile_name() -> None:
    """
    Tests:
        1. Obtain the name for an invalid source
        2. Obtain the name for a valid source with no profile.
        3. Obtain the name for a valid source with profile.
    """
    controller = initialize_controller()
    assert controller.get_source_settings_profile_name("invalid") == ""
    controller.add_source("file",MP3_FILE_PATH, RESULT_DIR_PATH)
    controller.create_new_settings_profile(
        "disk" , get_settings_profile_data())
    assert controller.get_source_settings_profile_name("file") == ""
    controller.apply_settings_profile_to_source("file","disk")
    assert controller.get_source_settings_profile_name("file") == "disk"
    controller.remove_all_settings_profiles()
    controller.clear_sources()

def test_controller_get_source_names_using_settings_profile() -> None:
    """
    Tests:
        1. Use an invalid profile name.
        2. get the name of all sources using profile.
    """
    controller = initialize_controller()
    controller.create_new_settings_profile(
        "disk" , get_settings_profile_data())
    controller.add_source("file",MP3_FILE_PATH, RESULT_DIR_PATH)
    controller.add_source("directory",CONV_DIR_PATH,RESULT_DIR_PATH)
    controller.apply_settings_profile_to_source("file","disk")
    controller.get_source_names_using_settings_profile("invalid") == []
    controller.get_source_names_using_settings_profile("disk") == ["file"]
    controller.remove_all_settings_profiles()
    controller.clear_sources()

def test_controller_get_sources_details_using_settings_profile() -> None:
    """
    Tests:
        1. Use an invalid profile name.
        2. Get source details of valid profile
    """
    controller = initialize_controller()
    controller.create_new_settings_profile(
        "disk" , get_settings_profile_data())
    controller.add_source("file",MP3_FILE_PATH, RESULT_DIR_PATH)
    controller.add_source("directory",CONV_DIR_PATH,RESULT_DIR_PATH)
    controller.apply_settings_profile_to_source("file","disk")
    assert list(controller.get_sources_details_using_settings_profile(
        "invalid").keys())== []
    assert list(controller.get_sources_details_using_settings_profile(
        "disk").keys()) == ["file"]
    controller.remove_all_settings_profiles()
    controller.clear_sources()

def test_controller_get_source_settings_profile_name() -> None:
    """
    Tests:
        1. Use an invalid source name.
        2. Get the settings details of settings appled to a source.
        3. Check for a source that does not have a settings profile.
    """
    controller = initialize_controller()
    controller.create_new_settings_profile(
        "disk" , get_settings_profile_data())
    controller.add_source("file",MP3_FILE_PATH, RESULT_DIR_PATH)
    controller.add_source("directory",CONV_DIR_PATH,RESULT_DIR_PATH)
    controller.apply_settings_profile_to_source("file","disk")
    assert controller.get_source_settings_profile_name("invalid") == None
    assert controller.get_source_settings_profile_name("file") == "disk"
    assert controller.get_source_settings_profile_name("directory") == None
    controller.remove_all_settings_profiles()
    controller.clear_sources()

# TODO: Run these tests
def test_controller_get_source_settings_profile_details() -> None:
    """
    Tests:
        1. Use an invalid source name.
        2. Get the settings details of settings appled to a source.
        3. Check for a source that does not have a settings profile.
    """
    controller = initialize_controller()
    controller.create_new_settings_profile(
        "disk" , get_settings_profile_data())
    controller.add_source("file",MP3_FILE_PATH, RESULT_DIR_PATH)
    controller.add_source("directory",CONV_DIR_PATH,RESULT_DIR_PATH)
    controller.apply_settings_profile_to_source("file","disk")
    assert controller.get_source_settings_profile_details("invalid") == None
    assert type(controller.get_source_settings_profile_details("file")) == \
        SettingDetails
    assert controller.get_source_settings_profile_details("directory") == None
    controller.remove_all_settings_profiles()
    controller.clear_sources()

def test_controller_get_sources_settings_profile_details() -> None:
    """
    Tests:
        1. Obtain the details of some sources.
    """
    controller = initialize_controller()
    controller.create_new_settings_profile(
        "disk" , get_settings_profile_data())
    controller.add_source("file",MP3_FILE_PATH, RESULT_DIR_PATH)
    controller.add_source("directory",CONV_DIR_PATH,RESULT_DIR_PATH)
    controller.apply_settings_profile_to_source("file","disk")
    assert list(controller.get_sources_settings_profile_details(
        ["file","directory"]).keys()) == ["file"]
    controller.remove_all_settings_profiles()
    controller.clear_sources()

def test_controller_get_all_sources_settings_profile_details() -> None:
    """
    Tests:
        1. Get all sources settings profiles details.
    """
    controller = initialize_controller()
    controller.create_new_settings_profile(
        "disk" , get_settings_profile_data())
    controller.add_source("file",MP3_FILE_PATH, RESULT_DIR_PATH)
    controller.add_source("directory",CONV_DIR_PATH,RESULT_DIR_PATH)
    controller.apply_settings_profile_to_source("file","disk")
    assert list(controller.get_all_sources_settings_profile_details().keys()) \
        == ["file"]
    controller.remove_all_settings_profiles()
    controller.clear_sources()

# TODO: Test after implementation.
def test_controller_get_supported_audio_formats() -> None:
    """
    Tests:
        1. Check there is more than one format.
    """
    controller = initialize_controller()
    assert len(controller.get_supported_audio_formats()) > 0

# TODO: Test after implementation.
def test_controller_get_supported_video_formats() -> None:
    """
    Tests:
        1. Check there is more than one format.
    """
    controller = initialize_controller()
    assert len(controller.get_supported_video_formats()) > 0

def test_get_analysis_plugin_names() -> None:
    """
    Tests:
        1. Check plugin names.
    """
    controller = initialize_controller()
    assert len(controller.get_analysis_plugin_names()) == 0
    controller.register_analysis_plugins(ANALYSIS_CONFIG_PATH)
    assert len(controller.get_analysis_plugin_names()) > 0

def test_get_format_names() -> None:
    """
    Tests:
        1. Check the return list length.
    """
    controller = initialize_controller()
    assert len(controller.get_format_names()) == 0
    controller.register_format(FORMAT_CONFIG_PATH)
    assert len(controller.get_format_names()) > 0

def test_get_format_plugin_names() -> None:
    """
    Tests:
        1. Use invalid plugin name .
        2. Check the plugin list length.
    """
    controller = initialize_controller()
    assert len(controller.get_format_plugin_names("invalid")) == 0
    format_name, plugin_names = controller.register_format(FORMAT_CONFIG_PATH)
    assert controller.get_format_plugin_names(format_name) == plugin_names

# TODO: Do this test.
def test_set_settings_profile_attribute() -> None:
    pass

# TODO: Do this test.
def test_set_source_settings_profile_attribute() -> None:
    pass






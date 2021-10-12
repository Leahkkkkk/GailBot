# Standard library imports
from enum import Enum
from typing import Any, Dict, Callable
# Local imports
from Src.Components.io import IO
from Src.Components.controller.services.organizer_service import GailBotSettings, GBSettingAttrs
from Src.Components.controller.services.fs_service.fs_service import \
    FileSystemService, SettingsHook, SourceHook
from Tests.controller.vardefs import *

############################### GLOBALS #####################################

# WS_DIR_PATH = "TestData/workspace/temp_ws"
# EMPTY_DIR_PATH = "TestData/workspace/empty_dir_1"
# WAV_FILE_PATH = "TestData/media/overlayed.wav"
# SETTINGS_PROFILE_EXTENSION = "json"

############################### SETUP #####################################


def get_settings_data() -> Dict:
    return {
        GBSettingAttrs.engine_type: "watson",
        GBSettingAttrs.watson_api_key: "MSgOPTS9CvbADe49nEg4wm8_gxeRuf4FGUmlHS9QqAw3",
        GBSettingAttrs.watson_language_customization_id: "41e54a38-2175-45f4-ac6a-1c11e42a2d54",
        GBSettingAttrs.watson_base_language_model: "en-US_BroadbandModel",
        GBSettingAttrs.watson_region: "dallas",
        GBSettingAttrs.analysis_plugins_to_apply: ["second_analysis"],
        GBSettingAttrs.output_format: "normal"}

########################## TEST DEFINITIONS ##################################


def test_configure_from_workspace_path() -> None:
    """
    Tests:
        1. Configure from a valid path.
        2. Configure from an invalid path.
    """
    service = FileSystemService()
    assert service.configure_from_workspace_path(WS_DIR_PATH)
    assert not service.configure_from_workspace_path("invalid")


def test_generate_settings_hook() -> None:
    """
    Tests:
        1. Generate a new hook after configuring.
        2. Generate a hook with the same name.
    """
    service = FileSystemService()
    service.configure_from_workspace_path(WS_DIR_PATH)
    assert type(service.generate_settings_hook("test")) == SettingsHook
    assert service.generate_settings_hook("test") == None


def test_generate_source_hook() -> None:
    """
    Tests:
        1. Generate a new hook after configuring.
        2. Generate a hook with the same name.
    """
    service = FileSystemService()
    service.configure_from_workspace_path(WS_DIR_PATH)
    assert type(service.generate_source_hook(
        "test", EMPTY_DIR_PATH)) == SourceHook
    assert service.generate_source_hook("test", EMPTY_DIR_PATH) == None


def test_remove_source_hook() -> None:
    """
    Tests:
        1. Remove a valid source hook.
        2. Remove an invalid source hook.
    """
    service = FileSystemService()
    service.configure_from_workspace_path(WS_DIR_PATH)
    service.generate_source_hook("test", EMPTY_DIR_PATH)
    assert service.remove_source_hook("test")
    assert not service.remove_source_hook("invalid")


def test_remove_settings_hook() -> None:
    """
    Tests:
        1. Remove a valid source hook.
        2. Remove an invalid source hook.
    """
    service = FileSystemService()
    service.configure_from_workspace_path(WS_DIR_PATH)
    service.generate_settings_hook("test")
    assert service.remove_settings_hook("test")
    assert not service.remove_settings_hook("invalid")


def test_is_workspace_configured() -> None:
    """
    Tests:
        1. Check before configuring.
        2. Check after configuring.
    """
    service = FileSystemService()
    assert not service.is_workspace_configured()
    service.configure_from_workspace_path(WS_DIR_PATH)
    assert service.is_workspace_configured()


def test_is_settings_hook() -> None:
    """
    Tests:
        1. Check valid hook.
        2. Check invalid hook.
    """
    service = FileSystemService()
    service.configure_from_workspace_path(WS_DIR_PATH)
    service.generate_settings_hook("test")
    assert service.is_settings_hook("test")
    assert not service.is_settings_hook("invalid")


def test_is_source_hook() -> None:
    """
    Tests:
        1. Check valid hook.
        2. Check invalid hook.
    """
    service = FileSystemService()
    service.configure_from_workspace_path(WS_DIR_PATH)
    service.generate_source_hook("test", EMPTY_DIR_PATH)
    assert service.is_source_hook("test")
    assert not service.is_source_hook("invalid")


def test_get_settings_hook() -> None:
    """
    Tests:
        1. Get valid hook.
        2. Get invalid hook.
    """
    service = FileSystemService()
    service.configure_from_workspace_path(WS_DIR_PATH)
    service.generate_settings_hook("test")
    assert type(service.get_settings_hook("test")) == SettingsHook
    assert service.get_settings_hook("invalid") == None


def test_get_source_hook() -> None:
    """
    Tests:
        1. Get valid hook.
        2. Get invalid hook.
    """
    service = FileSystemService()
    service.configure_from_workspace_path(WS_DIR_PATH)
    service.generate_source_hook("test", EMPTY_DIR_PATH)
    assert type(service.get_source_hook("test")) == SourceHook
    assert service.get_source_hook("invalid") == None


def test_get_all_settings_hooks() -> None:
    """
    Tests:
        1. Get all hooks.
    """
    service = FileSystemService()
    service.configure_from_workspace_path(WS_DIR_PATH)
    service.generate_settings_hook("test")
    service.generate_settings_hook("test2")
    assert list(service.get_all_settings_hooks().keys()) == \
        ["test", "test2"]


def test_get_all_source_hooks() -> None:
    """
    Tests:
        1. Get all hooks.
    """
    service = FileSystemService()
    service.configure_from_workspace_path(WS_DIR_PATH)
    service.generate_source_hook("test", EMPTY_DIR_PATH)
    service.generate_source_hook("test2", EMPTY_DIR_PATH)
    assert list(service.get_all_source_hooks().keys()) == \
        ["test", "test2"]


def test_get_source_hook_names() -> None:
    """
    Tests:
        1. Get the names of all hooks.
    """
    service = FileSystemService()
    service.configure_from_workspace_path(WS_DIR_PATH)
    service.generate_settings_hook("test")
    service.generate_settings_hook("test2")
    service.get_source_hook_names() == ["test", "test2"]


def test_get_settings_hook_names() -> None:
    """
    Tests:
        1. Get the names of all hooks.
    """
    service = FileSystemService()
    service.configure_from_workspace_path(WS_DIR_PATH)
    service.generate_settings_hook("test")
    service.generate_settings_hook("test2")
    service.get_settings_hook_names() == ["test", "test2"]

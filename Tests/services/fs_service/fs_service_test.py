from Src.components.services.fs_service import fs_service
from Tests.services.vardefs import *
# Standard library imports
from enum import Enum
from typing import Any, Dict, Callable
# Local imports
from Src.components.io import IO
from Src.components.services import FileSystemService, SourceHook, SettingsHook


############################### SETUP #####################################


########################## TEST DEFINITIONS ##################################


def test_shutdown() -> None:
    """
    Tests:
        1. Shutdown valid configured service.
    """
    fs_service = FileSystemService()
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    fs_service.shutdown()


def test_configure_from_workspace_path() -> None:
    """
    Tests:
        1. Configure in valid directory.
    """
    fs_service = FileSystemService()
    assert fs_service.configure_from_workspace_path(WS_DIR_PATH)
    fs_service.shutdown()


def test_generate_settings_hook() -> None:
    """
    Generate a settings hook in valid service
    """
    fs_service = FileSystemService()
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    assert fs_service.generate_settings_hook("test") != None
    fs_service.shutdown()


def test_generate_source_hook() -> None:
    """
    Tests:
        1. Generate a valid hook in valid service
    """
    fs_service = FileSystemService()
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    assert fs_service.generate_source_hook("test", EMPTY_DIR_PATH) != None
    fs_service.shutdown()


def test_is_workspace_configured() -> None:
    fs_service = FileSystemService()
    fs_service.configure_from_workspace_path(WS_DIR_PATH)
    assert fs_service.is_workspace_configured()
    fs_service.shutdown()

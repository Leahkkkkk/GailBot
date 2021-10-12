# Standard library imports
from typing import Dict
# Local imports
from Src.Components.io import IO
from Src.Components.controller.services.fs_service.source_hook import SourceHook
from Src.utils.observer import Subscriber
from Tests.controller.vardefs import *

############################### GLOBALS #####################################

SOURCE_NAME = "source"
# SOURCE_DIR_PATH = "TestData/workspace/temp_ws"
# EMPTY_DIR_PATH = "TestData/workspace/empty_dir_1"
# WAV_FILE_PATH = "TestData/media/test.txt"
# DIR_CONV_PATH = "TestData/media/conversation"

############################### SETUP #####################################


def listener(arg: str) -> None:
    print("Listening")


class TestSubscriber(Subscriber):
    def handle(self, event_type: str, data: Dict):
        print(data)


def add_to_hook(hook: SourceHook,
                identifier: str, path: str, item_type: str) -> None:
    io = IO()
    if io.is_file(path):
        new_path = "{}/{}.{}".format(EMPTY_DIR_PATH, io.get_name(path),
                                     io.get_file_extension(path)[1])
    elif io.is_directory(path):
        new_path = "{}/{}".format(EMPTY_DIR_PATH, io.get_name(path))
    else:
        new_path = path
    io.copy(path, new_path)
    s = hook.add_to_source(identifier, new_path, item_type)
    io.delete(new_path)
    return s

########################## TEST DEFINITIONS ##################################


def test_add_to_source() -> None:
    """
    Tests:
        1. Add a permanent file.
        2. Add a permanent directory.
        3. Re-add same item.
        4. Add a temp. item.
        5. Add an invalid path.
    """
    hook = SourceHook(SOURCE_DIR_PATH, SOURCE_NAME, EMPTY_DIR_PATH)
    assert add_to_hook(hook, "wav", WAV_FILE_PATH, "permanent")
    assert hook.is_contained("wav")
    assert not add_to_hook(hook, "wav", WAV_FILE_PATH, "permanent")
    assert hook.remove_from_source("wav")
    assert add_to_hook(hook, "dir", DIR_CONV_PATH, "permanent")
    assert hook.is_contained("dir")
    assert hook.remove_from_source("dir")
    assert add_to_hook(hook, "wav", WAV_FILE_PATH, "temporary")
    assert hook.is_contained("wav")
    assert hook.remove_from_source("wav")
    assert not add_to_hook(hook, "invalid", "invalid", "permanent")
    del hook


def test_write_to_file() -> None:
    """
    Tests:
        1. Write a new identifier.
        2. Append to new identifier.
    """
    io = IO()
    hook = SourceHook(SOURCE_DIR_PATH, SOURCE_NAME, EMPTY_DIR_PATH)
    assert hook.write_to_file(
        "test", "permanent", "apple", "txt", "Test dadasd")
    assert hook.write_to_file(
        "test", "permanent", "apple", "txt", "This is a new line")
    assert hook.write_to_file(
        "test", "permanent", "apple", "txt", "Test dadasd", True)


def test_change_item_type() -> None:
    """
    Tests:
        1. Change type for a valid item and get.
    """
    hook = SourceHook(SOURCE_DIR_PATH, SOURCE_NAME, EMPTY_DIR_PATH)
    assert add_to_hook(hook, "wav", WAV_FILE_PATH, "workspace")
    assert hook.change_item_type("wav", "permanent")
    assert hook.get_item_type("wav") == "permanent"
    hook.save_to_directory()
    del hook


def test_remove_from_source() -> None:
    """
    Tests:
        1. Remove a permanent file identifier.
        2. Remove a temporary dictionary.
        2. Remove an invalid identifier.
    """
    hook = SourceHook(SOURCE_DIR_PATH, SOURCE_NAME, EMPTY_DIR_PATH)
    assert add_to_hook(hook, "wav", WAV_FILE_PATH, "permanent")
    assert hook.remove_from_source("wav")
    assert add_to_hook(hook, "dir", DIR_CONV_PATH, "permanent")
    assert hook.remove_from_source("dir")
    assert not hook.remove_from_source("invalid")
    del hook


def test_cleanup() -> None:
    """
    Tests:
        1.Ensure all files deleted.
    """
    hook = SourceHook(SOURCE_DIR_PATH, SOURCE_NAME, EMPTY_DIR_PATH)
    assert add_to_hook(hook, "wav", WAV_FILE_PATH, "permanent")
    assert add_to_hook(hook, "dir", DIR_CONV_PATH, "permanent")
    hook.cleanup()
    del hook


def test_save_to_directory() -> None:
    io = IO()
    hook = SourceHook(SOURCE_DIR_PATH, SOURCE_NAME, EMPTY_DIR_PATH)
    assert add_to_hook(hook, "wav", WAV_FILE_PATH, "permanent")
    assert hook.save_to_directory()
    assert io.number_of_files_in_directory(
        hook.get_result_directory_path(), ["*"], False)[1] == 1
    del hook


def test_register_listener() -> None:
    """
    Tests:
        1. Add a listener of all three types and check if it works.
    """
    hook = SourceHook(SOURCE_DIR_PATH, SOURCE_NAME, EMPTY_DIR_PATH)
    subscriber = TestSubscriber()
    hook.register_listener("add_to_source", subscriber)
    hook.register_listener("remove_from_source", subscriber)
    hook.register_listener("cleanup", subscriber)
    assert add_to_hook(hook, "wav", WAV_FILE_PATH, "permanent")
    hook.remove_from_source("wav")
    hook.cleanup()
    del hook


def test_is_contained() -> None:
    """
    Tests:
        1. Use a valid identifier.
        2. Use an invalid identifier.
    """
    hook = SourceHook(SOURCE_DIR_PATH, SOURCE_NAME, EMPTY_DIR_PATH)
    add_to_hook(hook, "wav", WAV_FILE_PATH, "permanent")
    assert hook.is_contained("wav")
    assert not hook.is_contained("invalid")
    hook.cleanup()
    del hook


def test_get_hooked_paths() -> None:
    """
    Tests:
        1. Check that all items are returned.
    """
    hook = SourceHook(SOURCE_DIR_PATH, SOURCE_NAME, EMPTY_DIR_PATH)
    assert add_to_hook(hook, "wav", WAV_FILE_PATH, "permanent")
    assert add_to_hook(hook, "dir", DIR_CONV_PATH, "permanent")
    assert list(hook.get_hooked_paths("permanent").keys()) == ["wav", "dir"]
    hook.cleanup()
    del hook

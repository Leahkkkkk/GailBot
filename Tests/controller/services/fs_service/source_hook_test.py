# Standard library imports
# Local imports
from Src.Components.io import IO
from Src.Components.controller.services.fs_service.source_hook import SourceHook


############################### GLOBALS #####################################

SOURCE_DIR_PATH = "TestData/workspace/temp_ws"
EMPTY_DIR_PATH = "TestData/workspace/empty_dir_1"
WAV_FILE_PATH = "TestData/media/overlayed.wav"

############################### SETUP #####################################

def listener(arg : str) -> None:
    print("Listening")

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
    io = IO()
    hook = SourceHook(SOURCE_DIR_PATH)
    assert hook.add_to_source("wav",WAV_FILE_PATH,True)
    assert io.is_file(hook.get_item_path("wav"))
    assert not hook.add_to_source("wav2",WAV_FILE_PATH,False)
    assert hook.remove_from_source("wav")
    assert hook.add_to_source("dir",EMPTY_DIR_PATH,True)
    assert io.is_directory(hook.get_item_path("dir"))
    assert hook.remove_from_source("dir")
    assert hook.add_to_source("wav",WAV_FILE_PATH,False)
    assert io.is_file(hook.get_item_path("wav"))
    assert hook.remove_from_source("wav")
    assert not hook.add_to_source("invalid","invalid",False)

def test_remove_from_source() -> None:
    """
    Tests:
        1. Remove a permanent file identifier.
        2. Remove a temporary dictionary.
        2. Remove an invalid identifier.
    """
    hook = SourceHook(SOURCE_DIR_PATH)
    assert hook.add_to_source("wav",WAV_FILE_PATH,True)
    assert hook.remove_from_source("wav")
    assert hook.add_to_source("dir",EMPTY_DIR_PATH,False)
    assert hook.remove_from_source("dir")
    assert not hook.remove_from_source("invalid")

def test_cleanup() -> None:
    """
    Tests:
        1.Ensure all files deleted.
    """
    io = IO()
    hook = SourceHook(SOURCE_DIR_PATH)
    assert hook.add_to_source("wav",WAV_FILE_PATH,True)
    assert hook.add_to_source("dir",EMPTY_DIR_PATH,False)
    hook.cleanup()
    assert io.number_of_files_in_directory(SOURCE_DIR_PATH,["*"],False)[1] == 0

def test_register_listener() -> None:
    """
    Tests:
        1. Add a listener of all three types and check if it works.
    """
    hook = SourceHook(SOURCE_DIR_PATH)
    assert hook.register_listener("add_to_source",listener)
    assert hook.register_listener("remove_from_source",listener)
    assert hook.register_listener("cleanup",listener)
    hook.add_to_source("wav",WAV_FILE_PATH,True)
    hook.remove_from_source("wav")
    hook.cleanup()

def test_is_item() -> None:
    """
    Tests:
        1. Use a valid identifier.
        2. Use an invalid identifier.
    """
    hook = SourceHook(SOURCE_DIR_PATH)
    hook.add_to_source("wav",WAV_FILE_PATH,True)
    assert hook.is_item("wav")
    assert not hook.is_item("invalid")
    hook.cleanup()

def test_get_path() -> None:
    """
    Tests:
        1. Validate the path.
    """
    hook = SourceHook(SOURCE_DIR_PATH)
    assert hook.get_path() == SOURCE_DIR_PATH

def test_get_item_path() -> None:
    """
    Tests:
        1. Check a valid identifier path.
        2. Check an invalid identifier path.
    """
    io = IO()
    hook = SourceHook(SOURCE_DIR_PATH)
    hook.add_to_source("wav",WAV_FILE_PATH,True)
    assert io.is_file(hook.get_item_path("wav"))
    assert hook.get_item_path("invalid") == None
    hook.cleanup()

def test_get_hooked_items() -> None:
    """
    Tests:
        1. Check that all items are returned.
    """
    hook = SourceHook(SOURCE_DIR_PATH)
    assert hook.add_to_source("wav",WAV_FILE_PATH,True)
    assert hook.add_to_source("dir",EMPTY_DIR_PATH,False)
    assert list(hook.get_hooked_items().keys()) == ["wav","dir"]
    hook.cleanup()

def test_get_permanent_hooked_items() -> None:
    hook = SourceHook(SOURCE_DIR_PATH)
    assert hook.add_to_source("wav",WAV_FILE_PATH,True)
    assert hook.add_to_source("dir",EMPTY_DIR_PATH,False)
    assert list(hook.get_permanent_hooked_items().keys()) == ["wav"]
    hook.cleanup()

def test_get_temporary_hooked_items() -> None:
    hook = SourceHook(SOURCE_DIR_PATH)
    assert hook.add_to_source("wav",WAV_FILE_PATH,True)
    assert hook.add_to_source("dir",EMPTY_DIR_PATH,False)
    assert list(hook.get_temporary_hooked_items().keys()) == ["dir"]
    hook.cleanup()






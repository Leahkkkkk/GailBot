# Standard library imports
from typing import List
# Local imports
from Src.Components.analyzer import PluginLoader, PluginConfig, PluginData,\
                                    PluginDetails
# Third party imports

############################### GLOBALS #####################################

PLUGINS_DIR = "Tests/analyzer/plugins"
PLUGIN_ONE_DIR = "Tests/analyzer/plugins/plugin_one"
PLUGIN_ONE_FILE_PATH = "Tests/analyzer/plugins/plugin_one/plugin.py"
PLUGIN_TWO_DIR = "Tests/analyzer/plugins/plugin_two"
PLUGIN_TWO_FILE_PATH = "Tests/analyzer/plugins/plugin_two/plugin.py"
WAV_FILE_PATH = "TestData/media/test.wav"

############################### SETUP #######################################


def get_plugin_config(plugin_name : str, dependencies : List[str] = []) \
        -> PluginConfig:
    return PluginConfig(
        plugin_name, dependencies)

########################## TEST DEFINITIONS ##################################

def test_load_plugin_from_directory() -> None:
    """
    Tests:
        1. Load from a valid directory.
        2. Load from an invalid directory path.
        3. Load from invalid structure directory.
    """
    loader = PluginLoader()
    assert loader.load_plugin_from_directory(PLUGIN_ONE_DIR)
    assert not loader.load_plugin_from_directory(PLUGINS_DIR)
    assert not loader.load_plugin_from_directory("invalid")

def test_load_plugin_from_file() -> None:
    """
    Tests:
        1. Load from a valid file path.
        2. Load from an invalid file path.
        3. Load from an invalid file.
    """
    loader = PluginLoader()
    assert loader.load_plugin_from_file(
        get_plugin_config("one"), PLUGIN_ONE_FILE_PATH)
    assert not loader.load_plugin_from_file(
        get_plugin_config("invalid_file"), "invalid")
    assert not loader.load_plugin_from_file(
        get_plugin_config("wav"), WAV_FILE_PATH)

def test_load_plugin_subdirectories() -> None:
    """
    Tests:
        1. Load multiple plugins from subdirectories.
        2. Load from invalid directory.
        3. Load from invalid path.
    """
    loader = PluginLoader()
    assert loader.load_plugin_subdirectories(PLUGINS_DIR)
    assert not loader.load_plugin_subdirectories(PLUGIN_ONE_DIR)
    assert not loader.load_plugin_subdirectories("invalid")

def test_is_plugin_loaded() -> None:
    """
    Tests:
        1. Check a loaded plugin.
        2. Check a plugin that has not been loaded.
    """
    loader = PluginLoader()
    loader.load_plugin_from_file(
        get_plugin_config("one"), PLUGIN_ONE_FILE_PATH)
    assert loader.is_plugin_loaded("one")
    assert not loader.is_plugin_loaded("invalid")

def test_get_loaded_plugin_names() -> None:
    """
    Tests:
        1. Determine if the names of all plugins are returned.
    """
    loader = PluginLoader()
    assert len(loader.get_loaded_plugin_names()) == 0
    loader.load_plugin_from_file(
        get_plugin_config("one"), PLUGIN_ONE_FILE_PATH)
    loader.load_plugin_from_file(
        get_plugin_config("two"), PLUGIN_TWO_FILE_PATH)
    assert loader.get_loaded_plugin_names() == ["one","two"]

def test_get_plugin() -> None:
    """
    Tests:
        1. Get data for plugin that exists.
        2. Get data for plugin that does not exist.
    """
    loader = PluginLoader()
    loader.load_plugin_from_file(
        get_plugin_config("one"), PLUGIN_ONE_FILE_PATH)
    assert type(loader.get_plugin("one")) == PluginData
    assert loader.get_plugin("invalid") == None

def test_get_all_plugins() -> None:
    """
    Tests:
        1. Get data for all plugins.
    """
    loader = PluginLoader()
    loader.load_plugin_from_file(
        get_plugin_config("one"), PLUGIN_ONE_FILE_PATH)
    loader.load_plugin_from_file(
        get_plugin_config("two"), PLUGIN_TWO_FILE_PATH)
    assert list(loader.get_all_plugins().keys()) == ["one","two"]


def test_get_plugin_details() -> None:
    """
    Tests:
        1. Get the details of a loaded plugin.
        2. Get details of a plugin that has not been loaded.
    """
    loader = PluginLoader()
    loader.load_plugin_from_file(
        get_plugin_config("one"), PLUGIN_ONE_FILE_PATH)
    assert type(loader.get_plugin_details("one")) == PluginDetails
    assert loader.get_plugin_details("invalid") == None

def test_get_all_plugin_details() -> None:
    """
    Tests:
        1. Get all plugin details.
    """
    loader = PluginLoader()
    loader = PluginLoader()
    loader.load_plugin_from_file(
        get_plugin_config("one"), PLUGIN_ONE_FILE_PATH)
    loader.load_plugin_from_file(
        get_plugin_config("two"), PLUGIN_TWO_FILE_PATH)
    assert list(loader.get_all_plugin_details().keys()) == ["one","two"]

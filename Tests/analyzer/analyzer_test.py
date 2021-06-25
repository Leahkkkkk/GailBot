# Standard library imports
from typing import List, Dict
# Local imports
from Src.Components.analyzer import Analyzer, ApplyConfig, PluginConfig
# Third party imports

############################### GLOBALS #####################################

INVALID_DIR_PATH = "TestData/workspace/empty_dir_1"
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

def test_register_plugin() -> None:
    """
    Tests:
        1. Register from a valid directory.
        2. Register from an invalid directory.
        3. Register from an invalid directory structure.
    """
    analyzer = Analyzer()
    assert analyzer.register_plugin_from_directory(PLUGIN_ONE_DIR)
    assert not analyzer.register_plugin_from_directory("invalid")
    assert not analyzer.register_plugin_from_directory(INVALID_DIR_PATH)\

def test_register_plugin_from_file() -> None:
    """
    Tests:
        1. Load from a valid file.
        2. Load from an invalid file.
        3. Load from an invalid path.
    """
    analyzer = Analyzer()
    assert analyzer.register_plugin_from_file(
        get_plugin_config("one",[]),PLUGIN_ONE_FILE_PATH)
    assert not analyzer.register_plugin_from_file(
        get_plugin_config("one",[]),WAV_FILE_PATH)
    assert not analyzer.register_plugin_from_file(
        get_plugin_config("one",[]),"invalid")

def test_register_plugins_in_subdirectories() -> None:
    """
    Tests:
        1. Load from a valid directory.
        2. Load from an invalid directory structure.
        3. Load from an invalid directory path.
    """
    analyzer = Analyzer()
    assert analyzer.register_plugins_in_subdirectories(PLUGINS_DIR)
    assert not analyzer.register_plugins_in_subdirectories(PLUGIN_ONE_DIR)
    assert not analyzer.register_plugin_from_directory(WAV_FILE_PATH)

def test_apply_plugins_valid() -> None:
    """
    Tests:
        1. Apply valid plugins.
    """
    analyzer = Analyzer()
    # Loading plugins
    analyzer.register_plugin_from_file(
        get_plugin_config("one",[]),PLUGIN_ONE_FILE_PATH)
    analyzer.register_plugin_from_file(
        get_plugin_config("two",[]),PLUGIN_TWO_FILE_PATH)
    apply_configs = {
        "two" : ApplyConfig("two",["None"],"None"),
        "one" : ApplyConfig("one",["None"],"None")
        }
    assert analyzer.apply_plugins(apply_configs)


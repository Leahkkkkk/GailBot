# Standard library imports
from Src.Components.analyzer.plugin_details import PluginDetails
from typing import List, Dict
# Local imports
from Src.Components.analyzer import Analyzer, ApplyConfig
# Third party imports

############################### GLOBALS #####################################

INVALID_DIR_PATH = "TestData/workspace/empty_dir_1"
PLUGINS_DIR = "Tests/analyzer/plugins"
PLUGIN_ONE_DIR = "Tests/analyzer/plugins/plugin_one"
PLUGIN_ONE_CONFIG_PATH = "Tests/analyzer/plugins/plugin_one/config.json"
PLUGIN_TWO_DIR = "Tests/analyzer/plugins/plugin_two"
PLUGIN_TWO_CONFIG_PATH = "Tests/analyzer/plugins/plugin_two/config.json"
WAV_FILE_PATH = "TestData/media/test.wav"
WORKSPACE_DIR_PATH = "TestData/workspace"
RESULT_DIR_PATH = "TestData/workspace"

############################### SETUP #######################################

########################## TEST DEFINITIONS ##################################

def test_register_plugin_from_directory() -> None:
    """
    Tests:
        1. Register from a valid directory.
        2. Register from an invalid directory.
    """
    analyzer = Analyzer()
    assert analyzer.register_plugins_from_directory(PLUGINS_DIR) > 0
    assert analyzer.register_plugins_from_directory(PLUGIN_ONE_DIR) == 1
    assert analyzer.register_plugins_from_directory(INVALID_DIR_PATH) == 0

def test_register_plugin_using_config_file() -> None:
    """
    Tests:
        1. Use a valid config file.
        2. use an invalid config file path.
        3. Use an invalid config file structure.
    """
    analyzer = Analyzer()
    assert analyzer.register_plugin_using_config_file(PLUGIN_ONE_CONFIG_PATH)
    assert not analyzer.register_plugin_using_config_file(WAV_FILE_PATH)
    assert not analyzer.register_plugin_using_config_file("invalid")

def test_apply_plugins_valid() -> None:
    """
    Tests:
        1. Apply all plugins.
        2. Apply some plugins
    """
    analyzer = Analyzer()
    analyzer.register_plugins_from_directory(PLUGINS_DIR)
    summary = analyzer.apply_plugins({
        "plugin_one" : ApplyConfig("plugin_one",[],WORKSPACE_DIR_PATH,RESULT_DIR_PATH),
        "plugin_two" : ApplyConfig("plugin_two",[],WORKSPACE_DIR_PATH,RESULT_DIR_PATH),
    })
    print(summary)
    assert len(summary.successful_plugins) == 2

def test_is_plugin() -> None:
    """
    Tests:
        1. Check valid plugin.
        2. Check invalid plugin
    """
    analyzer = Analyzer()
    analyzer.register_plugins_from_directory(PLUGINS_DIR)
    assert analyzer.is_plugin("plugin_one")
    assert not analyzer.is_plugin("invalid")

def test_get_plugin_names() -> None:
    """
    Tests:
        1. Get the names of all the plugins that are loaded.
    """
    analyzer = Analyzer()
    analyzer.register_plugins_from_directory(PLUGINS_DIR)
    assert analyzer.get_plugin_names() == ["plugin_one","plugin_two"]

def test_get_plugin_details() -> None:
    """
    Tests:
        1. Get details of valid plugin.
        2. Get details of invalid plugins
    """
    analyzer = Analyzer()
    analyzer.register_plugins_from_directory(PLUGINS_DIR)
    assert type(analyzer.get_plugin_details("plugin_one")) == PluginDetails
    assert analyzer.get_plugin_details("invalid") == None

def test_get_all_plugin_details() -> None:
    """
    Tests:
        1. Get all plugin details.
    """
    analyzer = Analyzer()
    analyzer.register_plugins_from_directory(PLUGINS_DIR)
    assert list(analyzer.get_all_plugin_details().keys()) \
         == ["plugin_one","plugin_two"]



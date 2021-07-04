# Standard library imports
# Local imports
from Src.Components.plugin_manager import PluginManager, PluginDetails, ApplyConfig
# Third party imports

############################### GLOBALS #####################################

INVALID_DIR_PATH = "TestData/workspace/empty_dir_1"
PLUGINS_DIR = "TestData/plugins/random_plugins"
PLUGIN_ONE_DIR = "TestData/plugins/random_plugins/plugin_one"
PLUGIN_ONE_CONFIG_PATH = "TestData/plugins/random_plugins/plugin_one/config.json"
PLUGIN_TWO_DIR = "TestData/plugins/random_plugins/plugin_two"
PLUGIN_TWO_CONFIG_PATH = "TestData/plugins/random_plugins/plugin_two/config.json"
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
    plugin_manager = PluginManager()
    assert plugin_manager.register_plugins_from_directory(PLUGINS_DIR) > 0
    assert plugin_manager.register_plugins_from_directory(PLUGIN_ONE_DIR) == 1
    assert plugin_manager.register_plugins_from_directory(INVALID_DIR_PATH) == 0

def test_register_plugin_using_config_file() -> None:
    """
    Tests:
        1. Use a valid config file.
        2. use an invalid config file path.
        3. Use an invalid config file structure.
    """
    plugin_manager = PluginManager()
    assert plugin_manager.register_plugin_using_config_file(PLUGIN_ONE_CONFIG_PATH)
    assert not plugin_manager.register_plugin_using_config_file(WAV_FILE_PATH)
    assert not plugin_manager.register_plugin_using_config_file("invalid")

def test_apply_plugins_valid() -> None:
    """
    Tests:
        1. Apply all plugins.
        2. Apply some plugins.
        3. Apply a plugin that is dependant on another only. (should fail).
    """
    plugin_manager = PluginManager()
    plugin_manager.register_plugins_from_directory(PLUGINS_DIR)
    summary = plugin_manager.apply_plugins({
        "plugin_one" : ApplyConfig("plugin_one",[["path_1"]],{}),
        "plugin_two" : ApplyConfig("plugin_two",[["path_1"]],{}),
    })
    assert len(summary.successful_plugins) == 2
    summary = plugin_manager.apply_plugins({
        "plugin_one" : ApplyConfig("plugin_one",[["path_1"]],{})})
    assert len(summary.successful_plugins) == 1
    summary = plugin_manager.apply_plugins({
        "plugin_two" : ApplyConfig("plugin_two",[["path_1"]],{})})
    assert len(summary.successful_plugins) == 0

def test_is_plugin() -> None:
    """
    Tests:
        1. Check valid plugin.
        2. Check invalid plugin
    """
    plugin_manager = PluginManager()
    plugin_manager.register_plugins_from_directory(PLUGINS_DIR)
    assert plugin_manager.is_plugin("plugin_one")
    assert not plugin_manager.is_plugin("invalid")

def test_get_plugin_names() -> None:
    """
    Tests:
        1. Get the names of all the plugins that are loaded.
    """
    plugin_manager = PluginManager()
    plugin_manager.register_plugins_from_directory(PLUGINS_DIR)
    assert plugin_manager.get_plugin_names() == ["plugin_one","plugin_two"]

def test_get_plugin_details() -> None:
    """
    Tests:
        1. Get details of valid plugin.
        2. Get details of invalid plugins
    """
    plugin_manager = PluginManager()
    plugin_manager.register_plugins_from_directory(PLUGINS_DIR)
    assert type(plugin_manager.get_plugin_details("plugin_one")) == PluginDetails
    assert plugin_manager.get_plugin_details("invalid") == None

def test_get_all_plugin_details() -> None:
    """
    Tests:
        1. Get all plugin details.
    """
    plugin_manager = PluginManager()
    plugin_manager.register_plugins_from_directory(PLUGINS_DIR)
    assert list(plugin_manager.get_all_plugin_details().keys()) \
         == ["plugin_one","plugin_two"]



from typing import List
# Local imports
from Src.components.plugin_manager import PluginLoader, PluginSource, PluginConfig
# Third party imports
from Tests.plugin_manager.vardefs import *


############################### GLOBALS #####################################


############################### SETUP #######################################

########################## TEST DEFINITIONS ##################################


def test_load_plugin_using_config() -> None:
    """
    Tests:
        1. Load using a config with valid file path.
        2. Load using config with invalid file path.
        3. Load using config with invalid structure.
    """
    loader = PluginLoader()
    assert loader.load_plugin_using_config(
        PluginConfig("plugin_one", [], PLUGIN_FILE_PATH, "Umair", "None", "None", "plugin_one", "One"))
    assert not loader.load_plugin_using_config(
        PluginConfig("plugin_one", [], "invalid", "Umair", "None", "None", "plugin_one", "One"))
    assert not loader.load_plugin_using_config(
        PluginConfig("plugin_one", [], WAV_FILE_PATH, "Umair", "None", "None", "plugin_one", "One"))

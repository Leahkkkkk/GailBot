# Standard library imports
from typing import List
# Local imports
from Src.Components.analyzer import PluginLoader, PluginSource, PluginConfig
# Third party imports

############################### GLOBALS #####################################

PLUGIN_FILE_PATH = "Tests/analyzer/plugins/plugin_one/plugin.py"
WAV_FILE_PATH = "TestData/media/test2a_copy.wav"

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
        PluginConfig("plugin_one",[],PLUGIN_FILE_PATH,"Umair"))
    assert not loader.load_plugin_using_config(
        PluginConfig("plugin_one",[],"invalid","Umair"))
    assert not loader.load_plugin_using_config(
        PluginConfig("plugin_one",[],WAV_FILE_PATH,"Umair"))


# Standard library imports

# Local imports
from Src.Components.analyzer import Analyzer

# Third party imports

############################### GLOBALS #####################################

PLUGIN_CONFIG_DIR = "Src/Components/analyzer/plugins"
PLUGIN_ONE_DIR = "Tests/analyzer/plugins/plugin_one"
PLUGIN_TWO_DIR = "Tests/analyzer/plugins/plugin_two"

############################### SETUP #######################################

def initialize_analyzer() -> Analyzer:
    return Analyzer()

########################## TEST DEFINITIONS ##################################

def test_register_plugin() -> None:
    analyzer = initialize_analyzer()
    assert analyzer.register_plugin(PLUGIN_ONE_DIR)
    assert analyzer.register_plugin(PLUGIN_TWO_DIR)
    analyzer.apply_plugins("","",["plugin_one","plugin_two"])

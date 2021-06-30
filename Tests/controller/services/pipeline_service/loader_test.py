# Standard library imports
from typing import Dict, Any, List
# Local imports
from Src.Components.controller.services.pipeline_service import PipelineServiceLoader

# Third party imports

############################### GLOBALS #####################################

ANALYSIS_CONFIG_PATH = "TestData/plugins/analysis_plugins/config.json"
NORMAL_FORMAT_CONFIG_PATH = "TestData/plugins/normal_format_plugins/config.json"

############################### SETUP ########################################


########################## TEST DEFINITIONS ##################################

def test_parse_analysis_plugin_configuration_file() -> None:
    loader = PipelineServiceLoader()
    configs = loader.parse_analysis_plugin_configuration_file(
        ANALYSIS_CONFIG_PATH)
    assert len(configs) > 0

def test_parse_format_configuration_file() -> None:
    loader = PipelineServiceLoader()
    name, configs = loader.parse_format_configuration_file(
        NORMAL_FORMAT_CONFIG_PATH)
    assert len(configs) > 0

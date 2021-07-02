# Standard library imports
from dataclasses import dataclass
from typing import List, Any
# Local imports

@dataclass
class PluginConfig:
    """
    Used to configure / register a plugin.

    Args:
        plugin_name (str): Name of the plugin.
        plugin_dependencies (List[str]) Names of all plugins this is dependant on.
        plugin_file_path (str) Path to the definition file.
        plugin_author (str) Author name
        plugin_input_type (str) Type of the input as a string.
        plugin_output_type (str) Type of the output as a string.
        plugin_source_name (str) Name of the module plugin is loaded from.
        plugin_class_name (str) Name of the class plugin is loaded from.
    """
    plugin_name : str # Name of the plugin.
    plugin_dependencies : List[str] # Names of all plugins this is dependant on.
    plugin_file_path : str # Path to the definition file.
    plugin_author : str # Author name
    plugin_input_type : str # Type of the input as a string.
    plugin_output_type : str # Type of the output as a string.
    plugin_source_name : str # Name of the module plugin is loaded from.
    plugin_class_name : str # Name of the class plugin is loaded from.
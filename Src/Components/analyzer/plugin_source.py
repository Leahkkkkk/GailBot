# Standard library imports
from typing import List, Any
from dataclasses import dataclass
from .plugin import Plugin

@dataclass
class PluginSource:
    plugin_name : str
    plugin_object : Plugin
    plugin_dependencies : List[str]
    number_of_dependencies : int
    plugin_file_path : str
    plugin_author : str
    plugin_input_type : str
    plugin_output_type : str


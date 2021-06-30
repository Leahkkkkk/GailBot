# Standard library imports
from dataclasses import dataclass
from typing import List, Any
# Local imports

@dataclass
class PluginConfig:
    plugin_name : str
    plugin_dependencies : List[str]
    plugin_file_path : str
    plugin_author : str
    plugin_input_type : str
    plugin_output_type : str
    plugin_source_name : str
    plugin_class_name : str
# Standard library imports
from dataclasses import dataclass
from typing import List
# Local imports
from ...utils.loader import Config

@dataclass
class PluginConfig(Config):
    plugin_name : str
    plugin_dependencies : List[str]
    plugin_file_path : str
    plugin_author : str
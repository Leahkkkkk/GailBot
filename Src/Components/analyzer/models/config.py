# Standard library imports
from dataclasses import dataclass
from typing import List

@dataclass
class PluginConfig:
    plugin_name : str
    plugin_dependencies : List[str]
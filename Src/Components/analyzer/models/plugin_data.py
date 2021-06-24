# Standard library imports
from dataclasses import dataclass
from typing import List
# Local imports
from ..plugin import Plugin

@dataclass
class PluginData:
    plugin_object : Plugin
    plugin_name : str
    plugin_dependencies : List[str]
    number_of_dependencies : int
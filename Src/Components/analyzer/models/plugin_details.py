# Standard library imports
from dataclasses import dataclass
from typing import List
# Local imports


@dataclass
class PluginDetails:
    plugin_name : str
    plugin_dependencies : List[str]
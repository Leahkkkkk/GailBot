# Standard library imports
from dataclasses import dataclass
from typing import List
# Local imports

@dataclass
class PluginDetails:
    plugin_name : str
    plugin_dependencies : List[str]
    number_of_dependencies : int
    plugin_file_path : str
    plugin_author : str

# Standard library imports
from dataclasses import dataclass
from typing import List
# Local imports

@dataclass
class ApplyConfig:
    plugin_name : str
    source_paths : List[str]
    workspace_path : str
    result_dir_path : str
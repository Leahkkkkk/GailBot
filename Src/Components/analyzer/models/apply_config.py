# Standard library imports
from dataclasses import dataclass
from typing import List
# Local imports


@dataclass
class ApplyConfig:
    plugin_to_apply : str
    source_paths : List[str]
    result_dir_path : str
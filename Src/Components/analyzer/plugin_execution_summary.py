# Standard library imports
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PluginExecutionSummary:
    plugin_name : str
    source_paths : str
    source_to_output_paths : Dict[str,str]
    runtime_seconds : int
    was_successful : bool



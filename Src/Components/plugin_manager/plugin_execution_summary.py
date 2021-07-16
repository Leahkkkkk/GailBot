# Standard library imports
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class PluginExecutionSummary:
    """
    Summary for executing one individual plugin.
    """
    plugin_name : str
    args : List[Any]
    kwargs : Dict[str,Any]
    output : Any
    runtime_seconds : int
    was_successful : bool



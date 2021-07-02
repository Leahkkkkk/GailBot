# Standard library imports
from typing import List, Dict
from dataclasses import dataclass
from .plugin_execution_summary import PluginExecutionSummary

@dataclass
class PluginManagerSummary:
    """
    Summary for executing all plugins.

    Args:
        total_runtime_seconds (int)
        successful_plugins (List[str])
        failed_plugins (List[str])
        plugin_summaries (Dict[str, PluginExecutionSummary])

    """
    total_runtime_seconds : int
    successful_plugins : List[str]
    failed_plugins : List[str]
    plugin_summaries : Dict[str, PluginExecutionSummary]

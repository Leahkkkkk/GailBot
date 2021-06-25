# Standard library imports
from typing import List, Dict
from dataclasses import dataclass
from .plugin_execution_summary import PluginExecutionSummary

@dataclass
class AnalysisSummary:
    total_runtime_seconds : int
    successful_plugins : List[str]
    failed_plugins : List[str]
    plugin_summaries : Dict[str, PluginExecutionSummary]

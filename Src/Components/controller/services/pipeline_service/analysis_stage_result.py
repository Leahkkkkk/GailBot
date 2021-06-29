from dataclasses import dataclass
from typing import Dict
from ....plugin_manager import PluginManagerSummary

@dataclass
class AnalysisStageResult:
    analysis_summaries : Dict[str, PluginManagerSummary]
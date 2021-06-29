from dataclasses import dataclass
from typing import Dict
from ....analyzer import AnalysisSummary

@dataclass
class AnalysisStageResult:
    analysis_summaries : Dict[str,AnalysisSummary]
# Standard imports
from typing import List, Dict
from dataclasses import dataclass, field
from .payload_summary import PayloadSummary

@dataclass
class PipelineServiceSummary:
    source_names : List[str] = field(default_factory=list)
    sources_transcribed : List[str] = field(default_factory=list)
    sources_analyzed : List[str] = field(default_factory=list)
    sources_formatted : List[str] = field(default_factory=list)
    payload_summaries : Dict[str,PayloadSummary] = field(default_factory=dict)

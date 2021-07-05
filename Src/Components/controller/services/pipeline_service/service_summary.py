# Standard imports
from typing import List, Dict
from dataclasses import dataclass, field

@dataclass
class PipelineServiceSummary:
    source_names : List[str] = field(default_factory=list)
    sources_transcribed : List[str] = field(default_factory=list)
    sources_analyzed : List[str] = field(default_factory=list)
    sources_formatted : List[str] = field(default_factory=list)
    sources_analysis_plugin_summaries : Dict[str,Dict] = field(default_factory=dict)
    sources_format_plugin_summaries : Dict[str,Dict] = field(default_factory=dict)

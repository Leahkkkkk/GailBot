# Standard library imports
from dataclasses import dataclass
from typing import List

@dataclass
class PipelineServiceSummary:
    successful_conversations : List[str]
    failed_conversations : List[str]
    ready_conversations : List[str]
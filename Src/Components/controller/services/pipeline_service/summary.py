# Standard imports
from typing import List, Dict
from dataclasses import dataclass
# Local imports
from .conversation_summary import ConversationSummary

@dataclass
class PipelineServiceSummary:
    conversation_summary : Dict[str, ConversationSummary]
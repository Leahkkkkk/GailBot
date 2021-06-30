# Standard imports
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class ConversationSummary:
    conversation_name : str
    analysis_plugins_applied : List[str]
    format_plugins_appled : List[str]
    applied_format_name : str
    transcription_status : bool
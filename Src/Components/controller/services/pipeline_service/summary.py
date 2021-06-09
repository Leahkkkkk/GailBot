# Standard library imports
from dataclasses import dataclass
from typing import List

@dataclass
class TranscriptionSummary:
    successfully_transcribed_conversation_names : List[str]
    unsuccessfully_transcribed_conversation_names : List[str]
    ready_to_transcribe_conversation_names : List[str]
    number_successfully_transcribed_conversations : int
    number_unsuccessfully_transcribed_conversations : int
    number_ready_to_transcribe_conversations : int
    total_runtime_seconds : int
# Standard library imports
from dataclasses import dataclass
from typing import List

@dataclass
class TranscriptionSummary:
    successfully_transcribed_conversation_names : List[str]
    failed_transcription_conversation_names : List[str]
    ready_to_transcribe_conversation_names : List[str]
    successfully_transcribed_conversation_number : int
    failed_transcription_conversation_number : int
    ready_to_transcribe_conversation_number : int
    transcription_runtime : str


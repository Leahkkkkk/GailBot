# Standard imports
from enum import Enum

class TranscriptionStatus(Enum):
    """
    Transcription Statuses.
    """
    ready = "ready"
    successful = "successful"
    unsuccessful = "unsuccessful"
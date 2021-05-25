# Standard imports
from enum import Enum

class TranscriptionStatus(Enum):
    ready = "ready"
    successful = "successful"
    unsuccessful = "unsuccessful"
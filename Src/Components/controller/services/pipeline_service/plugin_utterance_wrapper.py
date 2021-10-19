# Standard imports
from dataclasses import dataclass


@dataclass
class Utt:
    speaker_label: str = None
    start_time_seconds: float = None
    end_time_seconds: float = None
    transcript: str = None

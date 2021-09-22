# Standard imports
from dataclasses import dataclass

@dataclass
class Utt:
    speaker_label : str
    start_time_seconds : float
    end_time_seconds : float
    transcript : str

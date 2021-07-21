# Standard imports
from typing import List, Dict
from dataclasses import dataclass
# Local imports


@dataclass
class Turn:
    speaker_label : str
    start_time_seconds : float
    end_time_seconds : float
    transcript : str
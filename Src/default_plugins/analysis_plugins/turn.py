# Standard imports
from dataclasses import dataclass
# Local imports

@dataclass
class Turn:
    speaker : str
    start_time_seconds : float
    end_time_seconds : float
    transcript : str
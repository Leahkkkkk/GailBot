# Standard imports
from dataclasses import dataclass
from typing import List

@dataclass
class PayloadSummary:
    payload_name : str
    settings_profile_used : str
    transcription_successful : bool
    analysis_successful : bool
    analysis_plugins_applied : List[str]
    format_successful : bool
    format_plugins_applied : List[str]




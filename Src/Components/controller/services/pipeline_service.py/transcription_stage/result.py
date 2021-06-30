# Standard imports
from dataclasses import dataclass
from typing import Dict

@dataclass
class TranscriptionStageResult:
    conversations_audio_sources : Dict[str, Dict[str,str]]
    conversations_status_maps : Dict[str, Dict[str,bool]]
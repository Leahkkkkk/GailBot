# Standard imports
from dataclasses import dataclass
from typing import Dict

@dataclass
class TranscriptionStageResult:
    """
    Result of the TranscriptionStage.

    Args:
        converstions_audio_sources(Dict[str,Dict[str,str]]):
            Mapping from conversation names to a dictionary mapping source
            file names to actual audio path.
        conversations_status_map (Dict[str, Dict[str,bool]]):
            Mapping from conversation name to a dictionary containing
            source file name to transcription status.
    """
    conversations_audio_sources : Dict[str, Dict[str,str]]
    conversations_status_maps : Dict[str, Dict[str,bool]]
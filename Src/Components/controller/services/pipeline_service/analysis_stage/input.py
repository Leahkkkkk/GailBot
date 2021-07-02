# Standard imports
from dataclasses import dataclass
from typing import Dict, List
# Local imports
from .....engines import Utterance

@dataclass
class AnalysisPluginInput:
    """
    Defines the input to an analysis plugin on a per Conversation basis.

    Args:
        utterances_map (Dict[str,List[Utterance]]):
            Map from a conversation source file name to its generated utterances
        source_to_audio_map (Dict[str,str]):
            Map from a source file name to the transcribed audio file path.
        source_to_source_path_map (Dict[str,str]):
            Map from a source file name to its path.
    """
    utterances_map : Dict[str, List[Utterance]]
    source_to_audio_map : Dict[str,str]
    source_to_source_path_map : Dict[str,str]


# Standard imports
from dataclasses import dataclass
from typing import Dict, List
# Local imports
from .....engines import Utterance

@dataclass
class AnalysisPluginInput:
    utterances_map = Dict[str,List[Utterance]]
    source_to_audio_map = Dict[str,str]
    source_name_to_path_map = Dict[str,str]


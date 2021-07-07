# Standard imports
from dataclasses import dataclass
from typing import Dict, List
# Local imports
from .....engines import Utterance

@dataclass
class AnalysisPluginInput:
    conversation_name : str
    utterances_map = Dict[str,List[Utterance]]
    source_to_audio_map = Dict[str,str]
    source_name_to_path_map = Dict[str,str]
    workspace_directory_path : str
    result_directory_path : str


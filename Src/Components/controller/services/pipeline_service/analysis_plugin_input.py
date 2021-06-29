from dataclasses import dataclass
from typing import Dict, List
from ....engines import Utterance

@dataclass
class AnalysisPluginInput:
    utterances_map : Dict[str, List[Utterance]]
    source_to_audio_map : Dict[str,str]
    source_to_source_path_map : Dict[str,str]


# Standard imports
from typing import Dict,  Any, List
from dataclasses import dataclass
# Local imports
from .....engines import Utterance

@dataclass
class FormatPluginInput:
    conversation_name : str
    utterances_map : Dict[str,List[Utterance]]
    analysis_plugin_outputs : Dict[str,Any]
    workspace_directory_path : str
    result_directory_path : str

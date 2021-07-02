# Standard imports
from typing import Dict,  Any, List
from dataclasses import dataclass
# Local imports
from .....engines import Utterance

@dataclass
class FormatPluginInput:
    """
    Input to a format plugin.

    Args:
        utterances_map (Dict[str,List]):
            Map from source file name to its generated utterances.
            analysis_plugin_outputs (Dict[str,Any]):
                Mapping from analysis plugin names to their outputs.
    """
    utterances_map : Dict[str,List[Utterance]]
    analysis_plugin_outputs : Dict[str,Any]
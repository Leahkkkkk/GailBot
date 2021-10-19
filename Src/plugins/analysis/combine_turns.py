# Standard imports
from typing import Dict, Any, List, Tuple
import re
# Local imports
from Src.default_plugins.turn import Turn
from Src.Components.controller.services import AnalysisPluginInput, \
    AnalysisPlugin, Utt


class CombineTurns(AnalysisPlugin):

    def __init__(self) -> None:
        pass

    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_input: AnalysisPluginInput) -> List[Turn]:
        # Combine all the utterances in the utterance map into a single
        # conversation.
        combined = list()
        turns_map: Dict[str, List[Utt]] = dependency_outputs["turn_construct"]
        for turns in turns_map.values():
            combined.extend(turns)
        combined.sort(key=lambda utt: utt.start_time_seconds)
        return combined

        ################################# GETTERS ###############################

    def was_successful(self) -> bool:
        return True

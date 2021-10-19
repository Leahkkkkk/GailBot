# Standard imports
from typing import Dict, Any, List, Tuple
import re
# Local imports
from Src.default_plugins.turn import Turn
from Src.Components.controller.services import AnalysisPluginInput, \
    AnalysisPlugin, Utt


class Fto(AnalysisPlugin):

    def __init__(self) -> None:
        pass

    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_input: AnalysisPluginInput) -> List[Turn]:
        # Get the input from the dependency
        try:
            utterances: List[Utt] = dependency_outputs["pauses"]
            new_utterances = list()
            for i in range(len(utterances)-1):
                curr_utt = utterances[i]
                nxt_utt = utterances[i+1]
                fto = nxt_utt.start_time_seconds - curr_utt.end_time_seconds
                curr_utt.transcript += ' [FTO: {}] '.format(str(round(fto, 1)))
                new_utterances.append(curr_utt)
            new_utterances.append(utterances[-1])
            return new_utterances
        except Exception as e:
            print(e)

    ################################# GETTERS ###############################

    def was_successful(self) -> bool:
        return True

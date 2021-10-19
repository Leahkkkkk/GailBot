# Standard imports
from typing import Dict, Any, List, Tuple
import re
# Local imports
from Src.default_plugins.turn import Turn
from Src.Components.controller.services import AnalysisPluginInput, \
    AnalysisPlugin, Utt


class Gaps(AnalysisPlugin):

    def __init__(self) -> None:
        self.lb_gap = 0.3

    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_input: AnalysisPluginInput) -> List[Turn]:
        utterances: List[Utt] = dependency_outputs["fto"]
        new_utterances = list()
        for i in range(len(utterances)-1):
            curr_utt = utterances[i]
            nxt_utt = utterances[i+1]
            fto = round(nxt_utt.start_time_seconds -
                        curr_utt.end_time_seconds, 2)
            if fto >= self.lb_gap and \
                    curr_utt.speaker_label != nxt_utt.speaker_label:
                new_utterances.extend([
                    curr_utt,
                    Utt("*GAP", curr_utt.end_time_seconds,
                        nxt_utt.start_time_seconds,
                        ' (' + str(round(fto, 1)) + ')')])
            else:
                new_utterances.append(curr_utt)
        new_utterances.append(utterances[-1])
        return new_utterances

    ################################# GETTERS ###############################

    def was_successful(self) -> bool:
        return True

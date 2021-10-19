# Standard imports
from typing import Dict, Any, List, Tuple
import re
from dataclasses import dataclass
# Local imports
from Src.default_plugins.turn import Turn
from Src.Components.controller.services import AnalysisPluginInput, \
    AnalysisPlugin, Utt


class Pauses(AnalysisPlugin):

    def __init__(self) -> None:
        @dataclass
        class Thresholds:
            lb_latch = 0.01
            ub_latch = 0.09
            lb_pause = 0.2
            ub_pause = 1.0
            lb_micropause = 0.1
            ub_micropause = 0.2
            lb_large_pause = 1.0

        @dataclass
        class Delimiters:
            latch_marker = u'\u2248'

        self.thresholds = Thresholds
        self.delimiters = Delimiters

    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_input: AnalysisPluginInput) -> List[Turn]:
        # Get the utterances from the dependencies
        try:
            utterances: List[Utt] = dependency_outputs["overlaps"]
            new_utterances = list()
            for i in range(len(utterances) - 1):
                curr_utt = utterances[i]
                nxt_utt = utterances[i+1]
                # Pauses only added for the same speaker.
                if curr_utt.speaker_label == nxt_utt.speaker_label:
                    continue
                fto = round(nxt_utt.start_time_seconds -
                            curr_utt.end_time_seconds, 2)
                if self.thresholds.lb_latch <= fto <= self.thresholds.ub_latch:
                    curr_utt.transcript += " {} ".format(
                        self.delimiters.latch_marker)
                elif self.thresholds.lb_pause <= fto <= self.thresholds.ub_pause:
                    curr_utt.transcript += " ({}) ".format(str(round(fto, 1)))
                elif self.thresholds.lb_micropause <= fto \
                        <= self.thresholds.ub_micropause:
                    curr_utt.transcript += " ({}) ".format(str(round(fto, 1)))
                elif fto >= self.thresholds.lb_large_pause:
                    new_utterances.extend([
                        curr_utt,
                        Utt("*PAU", curr_utt.end_time_seconds,
                            nxt_utt.start_time_seconds,
                            " ({}) ".format(str(round(fto, 1))))])
                    continue
                new_utterances.append(curr_utt)
            new_utterances.append(utterances[-1])
            return new_utterances
        except Exception as e:
            print(e)

    ################################# GETTERS ###############################

    def was_successful(self) -> bool:
        return True

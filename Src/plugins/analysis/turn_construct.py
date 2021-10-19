# Standard imports
from typing import Dict, Any, List, Tuple
import re
from copy import deepcopy
# Local imports
from Src.default_plugins.turn import Turn
from Src.Components.controller.services import AnalysisPluginInput, \
    AnalysisPlugin, Utt


class TurnConstruct(AnalysisPlugin):

    def __init__(self) -> None:
        self.turn_end_threshold_secs = 0.1
        self.successful = False

    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_input: AnalysisPluginInput) -> List[Turn]:
        # Obtain the utterance map
        utterances_map = plugin_input.get_utterances()
        new_map = dict()
        # Check threshold and combine each utterance to the next, assuming
        # that the speaker is the same.
        for file_name, utterances in utterances_map.items():
            combined_utterances = [deepcopy(utt) for utt in utterances]
            i = 0
            while i < len(combined_utterances) - 1:
                curr_utt = combined_utterances[i]
                nxt_utt = combined_utterances[i+1]
                fto = nxt_utt.start_time_seconds - curr_utt.end_time_seconds
                is_same_speaker = curr_utt.speaker_label == nxt_utt.speaker_label
                if fto <= self.turn_end_threshold_secs and is_same_speaker:
                    combined_utt = Utt(
                        curr_utt.speaker_label, curr_utt.start_time_seconds,
                        nxt_utt.end_time_seconds,
                        "{} {}".format(curr_utt.transcript, nxt_utt.transcript))
                    combined_utterances[i] = combined_utt
                    del combined_utterances[i+1]
                else:
                    i += 1
            new_map[file_name] = combined_utterances
        self.successful = True
        return new_map

    ################################# GETTERS ###############################

    def was_successful(self) -> bool:
        return self.successful

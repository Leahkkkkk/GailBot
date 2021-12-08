# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:57:50
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-07 17:47:49
# Standard imports
from typing import Dict, Any, List, Tuple
import re
from copy import deepcopy
# Local imports
from Src.components import GBPlugin, PluginMethodSuite, Utt


class TurnConstruct(GBPlugin):

    def __init__(self) -> None:
        super().__init__()
        self.turn_end_threshold_secs = 0.1

    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_input: PluginMethodSuite) -> List[Utt]:
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
                        "{} {}".format(curr_utt.text, nxt_utt.text))
                    combined_utterances[i] = combined_utt
                    del combined_utterances[i+1]
                else:
                    i += 1
            new_map[file_name] = combined_utterances
        self.successful = True
        return new_map

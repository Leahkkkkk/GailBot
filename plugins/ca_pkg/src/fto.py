# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:57:50
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-07 17:41:59
# Standard imports
from typing import Dict, Any, List, Tuple
import re
# Local imports
from gailbot.plugins import GBPlugin, PluginMethodSuite, Utt

class Fto(GBPlugin):

    def __init__(self) -> None:
        super().__init__()

    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_input: PluginMethodSuite) -> List[Utt]:
        # Get the input from the dependency
        utterances: List[Utt] = dependency_outputs["pauses"]
        new_utterances = list()
        for i in range(len(utterances)-1):
            curr_utt = utterances[i]
            nxt_utt = utterances[i+1]
            fto = nxt_utt.start_time_seconds - curr_utt.end_time_seconds
            curr_utt.text += ' [FTO: {}] '.format(str(round(fto, 1)))
            new_utterances.append(curr_utt)
        new_utterances.append(utterances[-1])
        self.successful = True
        return new_utterances

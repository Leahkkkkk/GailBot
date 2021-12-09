# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-09 12:52:36
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-09 13:15:16

# Standard imports
from typing import Dict, Any, List, Tuple
from copy import deepcopy
# Local imports
from .vars import *
# Third party imports
from Src import GBPlugin, PluginMethodSuite, Utt


class TCU(GBPlugin):
    """
    Convert utt objects per data file to TCUs
    Plugin Dependencies: None
    Assumptions:
        1. Each Data file is part of the same conversation.
    """

    def __init__(self) -> None:
        super().__init__()

    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_input: PluginMethodSuite) -> List[Utt]:
        """
        Combine all words for each data file into tcus for the entire conversation
        """
        # Obtain utterances map
        utterances_map = plugin_input.get_utterances()
        tcu_map = dict()
        for identifier, utterances in utterances_map.items():
            tcus = self._create_tcus(utterances)
            tcu_map[identifier] = tcus
        # Combine the transcripts
        combined_tcus = self._combine_transcripts(tcu_map)
        self.successful = True
        return combined_tcus

    def _create_tcus(self, utterances: List[Utt]) -> List[Utt]:
        tcus = [deepcopy(utt) for utt in utterances]
        i = 0
        while i < len(tcus) - 1:
            curr_utt = tcus[i]
            next_utt = tcus[i+1]
            # Calculate the FTO
            fto = next_utt.end_time_seconds - curr_utt.start_time_seconds
            if fto < TURN_END_THRESHOLD_SECS and \
                    curr_utt.speaker_label == next_utt.speaker_label:
                # Create the new Utt
                combined_utt = Utt(
                    curr_utt.speaker_label, curr_utt.start_time_seconds,
                    next_utt.end_time_seconds,
                    "{} {}".format(curr_utt.text, next_utt.text))
                tcus[i] = combined_utt
                del tcus[i+1]
            else:
                i += 1
        return tcus

    def _combine_transcripts(self, tcu_map: Dict[str, List[Utt]]) -> List[Utt]:
        """
        Combine tcus for individual data files into a tcu list for the
        conversation, keeping original speaker labels.
        """
        combined = list()
        for tcus in tcu_map.values():
            combined.extend(tcus)
        # Sort based on start time
        combined.sort(key=lambda utt: utt.start_time_seconds)
        return combined

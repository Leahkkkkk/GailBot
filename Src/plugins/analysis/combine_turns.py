# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:57:50
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-07 12:48:58
# Standard imports
from typing import Dict, Any, List, Tuple
import re
# Local imports
from Src.components import GBPlugin, PluginMethodSuite, Utt


class CombineTurns(GBPlugin):

    def __init__(self) -> None:
        pass

    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_input: PluginMethodSuite) -> List[Utt]:
        # Combine all the utterances in the utterance map into a single
        # conversation.
        try:
            combined = list()
            turns_map: Dict[str, List[Utt]
                            ] = dependency_outputs["turn_construct"]
            for turns in turns_map.values():
                combined.extend(turns)
            combined.sort(key=lambda utt: utt.start_time_seconds)
            return combined
        except Exception as e:
            print("combine turns", e)

        ################################# GETTERS ###############################

    def was_successful(self) -> bool:
        return True

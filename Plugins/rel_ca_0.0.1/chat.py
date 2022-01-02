# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:57:50
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-08 15:19:45
# Standard imports


from typing import Dict, Any, List, Tuple
import re
import io
# Local imports
from Src.components import GBPlugin, PluginMethodSuite, Utt


class CHAT(GBPlugin):

    def __init__(self) -> None:
        super().__init__()

    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_input: PluginMethodSuite) -> List[Utt]:
        # Combine all the utterances in the utterance map into a single
        # conversation.
        utterances: List[Utt] = dependency_outputs["gaps"]
        count = 0
        data = [
            "@Begin\n@Languages:\t{0}\n".format("eng"),
            "@Options:\tCA\n",
            "@Media:\t{0},audio\n".format("test"),
            "@Comment:\t{0}\n".format("absolute"),
            "@Transcriber:\tGailbot 0.3.0\n",
            "@Location:\t{0}\n".format("Hilab"),
            "@Room Layout:\t{0}\n".format("big"),
            "@Situation:\t{0}\n@New Episode\n".format("test")
        ]
        path = "{}/{}.cha".format(plugin_input.get_result_directory_path(),
                                  str(count))
        with io.open(path, "w", encoding='utf-8') as outfile:
            for item in data:
                outfile.write(item)
            for utt in utterances:
                turn = '{0}\t{1} {4}{2}_{3}{4}\n'.format(
                    utt.speaker_label, utt.text, utt.start_time_seconds, utt.end_time_seconds,
                    0x15)
                outfile.write(turn)
        self.successful = True

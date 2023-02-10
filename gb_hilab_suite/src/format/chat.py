# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-24 10:54:53
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-24 12:16:03

from typing import Dict, Any
# Local imports
from gailbot.plugins.plugin import Plugin, Methods, Utt

from gb_hilab_suite.src.gb_hilab_suite import *

class ChatPlugin(Plugin):

    def __init__(self) -> None:
        super().__init__()

    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_input: Methods):
        """
        Prints the entire tree in a user-specified chat format
        """
        cm = dependency_outputs["conv_model"]
        varDict = {
                GAPS: CHAT_GAPMARKER,
                MARKER1: OVERLAPMARKER_CURR_START,
                MARKER2: OVERLAPMARKER_CURR_END,
                MARKER3: OVERLAPMARKER_NEXT_START,
                MARKER4: OVERLAPMARKER_NEXT_END,
                PAUSES: CHAT_PAUSE,
                FASTSPEECH_START: FASTSPEECH_START,
                FASTSPEECH_END: FASTSPEECH_END,
                SLOWSPEECH_START: SLOWSPEECH_START,
                SLOWSPEECH_END: SLOWSPEECH_END
        }

        root = cm.getTree(False)
        newUttMap = dict()
        myFunction = cm.outer_buildUttMapWithChange(0)
        myFunction(root, newUttMap, varDict)

        # start printing to file
        data = [
            "@Begin\n@Languages:\t{0}\n".format("eng")
        ]
        path = "{}/conversation.cha".format(plugin_input.get_result_directory_path())

        utterances = newUttMap
        with open(path, "w", encoding='utf-8') as outfile:
            for item in data:
                outfile.write(item)
            for _, (_, nodeList) in enumerate(utterances.items()):
                curr_utt = cm.getWordFromNode(nodeList)

                l = []
                for word in curr_utt:
                    l.append(word.text)
                txt = ' '.join(l)

                sLabel = SPEAKERLABEL + str(curr_utt[0].sLabel)

                turn = '{0}\t{1} {2}{4}_{3}{4}\n'.format(
                    sLabel, txt, curr_utt[0].startTime, curr_utt[-1].endTime,
                    0x15)

                outfile.write(turn)
        self.successful = True
        return
# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:57:50
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-05-12 13:19:34
# Standard imports
from typing import Dict, Any, List, Tuple
import re
import io
# Local imports
from gailbot.plugins import GBPlugin, PluginMethodSuite, Utt
from markerdef import *

class chat(GBPlugin):

    def __init__(self) -> None:
        super().__init__()

    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_input: PluginMethodSuite):
        """
        Prints the entire tree in a user-specified chat format
        """
        try:
            cm = dependency_outputs["convModelPlugin"]
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
            count = 0
            data = [
                "@Begin\n@Languages:\t{0}\n".format("eng")
            ]
            path = "{}/{}.cha".format(plugin_input.get_result_directory_path(),
                                    str(count))

            utterances = newUttMap
            with io.open(path, "w", encoding='utf-8') as outfile:
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

        except Exception as E:
            print("exception in chat")
            print(E)
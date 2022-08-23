# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:57:50
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-05-03 17:51:03
# Standard imports


from typing import Dict, Any, List, Tuple
import re
import io
# Local imports
from gailbot.plugins import GBPlugin, PluginMethodSuite, Utt
from markerdef import *


class txt(GBPlugin):

    def __init__(self) -> None:
        super().__init__()

    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_input: PluginMethodSuite):
        """
        Prints the entire tree in a user-specified format
        """
        try:
            cm = dependency_outputs["convModelPlugin"]

            varDict = {
                GAPS: TXT_GAPMARKER,
                OVERLAPS: TXT_OVERLAPMARKER,
                MARKER1: TXT_OVERLAPMARKER,
                MARKER2: TXT_OVERLAPMARKER,
                MARKER3: TXT_OVERLAPMARKER,
                MARKER4: TXT_OVERLAPMARKER,
                PAUSES: TXT_PAUSE,
            }

            root = cm.getTree(False)
            newUttMap = dict()
            myFunction = cm.outer_buildUttMapWithChange(0)
            myFunction(root, newUttMap, varDict)

            count = 100
            data = ["this is a txt file"]
            path = "{}/{}.txt".format(plugin_input.get_result_directory_path(),
                                      str(count))

            utterances = newUttMap

            with io.open(path, "w", encoding='utf-8') as outfile:
                for item in data:
                    outfile.write(item)
                for i, (id, nodeList) in enumerate(utterances.items()):
                    curr_utt = cm.getWordFromNode(nodeList)
                    l = []
                    for word in curr_utt:
                        l.append(word.text)
                    txt = ' '.join(l)

                    sLabel = TXT_SPEAKERLABEL + str(curr_utt[0].sLabel)
                    turn = '{0}\t{1} {2}{4}_{3}{4}\n'.format(
                        sLabel, txt, curr_utt[0].startTime, curr_utt[-1].endTime,
                        0x15)
                    outfile.write(turn)
            self.successful = True
            return

        except Exception as E:
            print("exception in txt")
            print(E)

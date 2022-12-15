# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:57:50
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-08 15:19:45
# Standard imports
from typing import Dict, Any
from gailbot.plugins import GBPlugin, PluginMethodSuite
import csv
from markerdef import *

class csvWordLevel(GBPlugin):

    def __init__(self) -> None:
        super().__init__()

    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_input: PluginMethodSuite):
        """
        Prints the entire tree into a CSV file
        """
        try:
            cm = dependency_outputs["convModelPlugin"]
            varDict = {
                GAPS: CSV_GAPMARKER,
                OVERLAPS: CSV_OVERLAPMARKER,
                MARKER1: CSV_OVERLAPMARKER,
                MARKER2: CSV_OVERLAPMARKER,
                MARKER3: CSV_OVERLAPMARKER,
                MARKER4: CSV_OVERLAPMARKER,
                PAUSES: CSV_PAUSE
            }

            root = cm.getTree(False)
            newUttMap = dict()
            myFunction = cm.outer_buildUttMapWithChange(0)
            myFunction(root, newUttMap, varDict)

            count = 0

            path = "{}/{}.csv".format(plugin_input.get_result_directory_path(),
                                     "wordLevel" + str(count))

            with open(path, 'w', newline='') as outfile:
                writer = csv.writer(outfile)

                writer.writerow(["SPEAKER LABEL", "TEXT", "START TIME",
                                 "END TIME"])
                utterances = newUttMap
                for _, (_, nodeList) in enumerate(utterances.items()):
                    curr_utt = cm.getWordFromNode(nodeList)

                    for word in curr_utt:
                        sLabel = curr_utt[0].sLabel
                        if curr_utt[0].sLabel not in INTERNAL_MARKER_SET:
                            sLabel = CSV_SPEAKERLABEL + str(curr_utt[0].sLabel)
                            writer.writerow([word.sLabel, word.text,
                                             word.startTime, word.endTime])
                        else:
                            writer.writerow([word.sLabel, word.text,
                                             word.startTime, word.endTime])

            self.successful = True
            return

        except Exception as E:
            print("exception in csvWordLevel")
            print(E)
            self.successful = False
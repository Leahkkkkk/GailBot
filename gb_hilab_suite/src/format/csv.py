# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-24 10:54:53
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-24 12:16:45


from typing import Dict, Any
import csv
# Local imports
from gailbot.plugins.plugin import Plugin, Methods, Utt
from gb_hilab_suite.src.gb_hilab_suite import *

class CSVPlugin(Plugin):

    def __init__(self) -> None:
        super().__init__()

    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                    plugin_input: Methods):
        self._utterance_level(dependency_outputs, plugin_input)
        self._word_level(dependency_outputs, plugin_input)
        self.successful = True

    def _utterance_level(
        self,
        dependency_outputs: Dict[str, Any],
        plugin_input: Methods
    ):

        """
        Prints the entire tree into a CSV file
        """
        cm = dependency_outputs["conv_model"]
        varDict = {
            GAPS: CSV_GAPMARKER,
            OVERLAPS: CSV_OVERLAPMARKER,
            MARKER1: CSV_OVERLAPMARKER,
            MARKER2: CSV_OVERLAPMARKER,
            MARKER3: CSV_OVERLAPMARKER,
            MARKER4: CSV_OVERLAPMARKER,
            PAUSES: CSV_PAUSE,
        }

        root = cm.getTree(False)
        newUttMap = dict()
        myFunction = cm.outer_buildUttMapWithChange(0)
        myFunction(root, newUttMap, varDict)

        path = "{}/{}.csv".format(plugin_input.get_result_directory_path(),
                                "utterance_level")

        with open(path, 'w', newline='') as outfile:
            writer = csv.writer(outfile)

            writer.writerow(["SPEAKER LABEL", "TEXT", "START TIME",
                                "END TIME"])

            utterances = newUttMap
            for _, (_, nodeList) in enumerate(utterances.items()):
                curr_utt = cm.getWordFromNode(nodeList)

                l = []
                for word in curr_utt:
                    l.append(word.text)
                txt = ' '.join(l)

                sLabel = ""
                if (curr_utt[0].sLabel != "*GAP" and
                    curr_utt[0].sLabel != "pauses"):
                    sLabel = CSV_SPEAKERLABEL + str(curr_utt[0].sLabel)
                    writer.writerow([sLabel, txt, curr_utt[0].startTime,
                                        curr_utt[-1].endTime])
                else:
                    writer.writerow(["", txt, curr_utt[0].startTime,
                                        curr_utt[-1].endTime])

    def _word_level(
        self,
        dependency_outputs: Dict[str, Any],
        plugin_input: Methods
    ):
        cm = dependency_outputs["conv_model"]
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

        path = "{}/{}.csv".format(plugin_input.get_result_directory_path(),
                                    "word_level")

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




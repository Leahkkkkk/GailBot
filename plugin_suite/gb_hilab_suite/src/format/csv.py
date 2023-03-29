# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-24 10:54:53
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-24 12:16:45


from typing import Dict, Any
import csv
# Local imports
from gailbot import Plugin, UttObj, GBPluginMethods
from gb_hilab_suite.src.core.conversation_model import ConversationModel
from gb_hilab_suite.src.config import MARKER, THRESHOLD, LABEL, PLUGIN_NAME

class CSVPlugin(Plugin):

    def __init__(self) -> None:
        super().__init__()

    def apply(self, dependency_outputs: Dict[str, Any],
                    methods: GBPluginMethods):
        self._utterance_level(dependency_outputs, methods)
        self._word_level(dependency_outputs, methods)
        self.successful = True

    def _utterance_level(
        self,
        dependency_outputs: Dict[str, Any],
        methods: GBPluginMethods
    ):

        """
        Prints the entire tree into a CSV file
        """
        cm: ConversationModel = dependency_outputs[PLUGIN_NAME.ConvModel]
        varDict = {
            MARKER.GAPS: LABEL.CSV_GAPMARKER,
            MARKER.OVERLAPS: LABEL.CSV_OVERLAPMARKER,
            MARKER.MARKER1: LABEL.CSV_OVERLAPMARKER,
            MARKER.MARKER2: LABEL.CSV_OVERLAPMARKER,
            MARKER.MARKER3: LABEL.CSV_OVERLAPMARKER,
            MARKER.MARKER4: LABEL.CSV_OVERLAPMARKER,
            MARKER.PAUSES: LABEL.CSV_PAUSE,
        }

        root = cm.getTree(False)
        newUttMap = dict()
        myFunction = cm.outer_buildUttMapWithChange(0)
        myFunction(root, newUttMap, varDict)

        path = "{}/{}.csv".format(methods.output_path,
                                "utterance_level")

        with open(path, 'w', newline='') as outfile:
            writer = csv.writer(outfile)

            writer.writerow(["SPEAKER LABEL", "TEXT", "START TIME", "END TIME"])

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
                    sLabel = LABEL.CSV_SPEAKERLABEL + str(curr_utt[0].sLabel)
                    writer.writerow([sLabel, txt, curr_utt[0].startTime,
                                        curr_utt[-1].endTime])
                else:
                    writer.writerow(["", txt, curr_utt[0].startTime,
                                        curr_utt[-1].endTime])

    def _word_level(
        self,
        dependency_outputs: Dict[str, Any],
        methods: GBPluginMethods
    ):
        cm: ConversationModel = dependency_outputs[PLUGIN_NAME.ConvModel]
        varDict = {
            MARKER.GAPS: LABEL.CSV_GAPMARKER,
            MARKER.OVERLAPS: LABEL.CSV_OVERLAPMARKER,
            MARKER.MARKER1: LABEL.CSV_OVERLAPMARKER,
            MARKER.MARKER2: LABEL.CSV_OVERLAPMARKER,
            MARKER.MARKER3: LABEL.CSV_OVERLAPMARKER,
            MARKER.MARKER4: LABEL.CSV_OVERLAPMARKER,
            MARKER.PAUSES: LABEL.CSV_PAUSE
        }

        root = cm.getTree(False)
        newUttMap = dict()
        myFunction = cm.outer_buildUttMapWithChange(0)
        myFunction(root, newUttMap, varDict)

        path = "{}/{}.csv".format(methods.output_path,
                                    "word_level")

        with open(path, 'w', newline='') as outfile:
            writer = csv.writer(outfile)

            writer.writerow(["SPEAKER LABEL", "TEXT", "START TIME", "END TIME"])
            utterances = newUttMap
            for _, (_, nodeList) in enumerate(utterances.items()):
                curr_utt = cm.getWordFromNode(nodeList)

                for word in curr_utt:
                    sLabel = curr_utt[0].sLabel
                    if curr_utt[0].sLabel not in MARKER.INTERNAL_MARKER_SET:
                        sLabel = LABEL.CSV_SPEAKERLABEL + str(curr_utt[0].sLabel)
                        writer.writerow([word.sLabel, word.text,
                                            word.startTime, word.endTime])
                    else:
                        writer.writerow([word.sLabel, word.text,
                                            word.startTime, word.endTime])




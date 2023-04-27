# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-24 10:32:30
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-24 12:26:25

import logging
import io
from typing import Dict, Any, List
from dataclasses import dataclass
# Local imports
from gailbot import Plugin, GBPluginMethods, UttObj
from gb_hilab_suite.src.core.conversation_model import ConversationModel
from gb_hilab_suite.src.config import MARKER, THRESHOLD, PLUGIN_NAME


class PausePlugin(Plugin):
    def __init__(self) -> None:
        super().__init__()

    def apply(self, dependency_outputs: Dict[str, Any],
                     methods: GBPluginMethods) -> List[UttObj]:
        """
        Inserts new nodes into the BST, which represents a pause.

        1. Iterate through the word-level dictionary and retrieve an utterance
           pair
        2. If by the same speaker, check the FTO of the utterance pair. If it
           matches the criterion for a pause, insert a pause marker into the
           tree. Else, do nothing.

        Args:
            dependency_outputs (Dict[str, Any]):
            methods (PluginMethodSuite):

        Returns:
            convModelPlugin: the current conv model wrapper object
        """
        # Get the output of the previous plugin
        cm: ConversationModel = dependency_outputs[PLUGIN_NAME.ConvModel]
        utterances = cm.getUttMap(False)

        mapIter = cm.map_iterator(utterances)  # iterator
        i = mapIter.iter()  # i is the iterable object
        while i.hasNextPair():
            pair = i.nextPair()
            curr_utt = cm.getWordFromNode(pair[0])
            nxt_utt = cm.getWordFromNode(pair[1])

            if curr_utt[0].sLabel == nxt_utt[0].sLabel:
                fto = round(nxt_utt[0].startTime - curr_utt[-1].endTime, 2)
                markerText = ""
                if  (THRESHOLD.LB_LATCH <= fto) and (fto <= THRESHOLD.UB_LATCH):
                    logging.debug("pauses")
                    markerText = "({1}{0}{2}{0}{3})".format(MARKER.MARKER_SEP,
                                                            str(MARKER.MARKERTYPE) +
                                                            str(MARKER.KEYVALUE_SEP) +
                                                            str(MARKER.PAUSES),
                                                            str(MARKER.MARKERINFO) +
                                                            str(MARKER.KEYVALUE_SEP) +
                                                            str(MARKER.LATCH_DELIM),
                                                            str(MARKER.MARKERSPEAKER) +
                                                            str(MARKER.KEYVALUE_SEP) +
                                                            str(curr_utt[-1].sLabel))
                    cm.insertToTree(curr_utt[-1].endTime,
                                    nxt_utt[0].startTime,
                                    MARKER.PAUSES,
                                    markerText)
                elif THRESHOLD.LB_PAUSE <= fto <= THRESHOLD.UB_PAUSE:
                    logging.debug("pauses")
                    # TODO: 0.8 vs -0.8
                    markerText = "({1}{0}{2}{0}{3})".format(MARKER.MARKER_SEP,
                                                            str(MARKER.MARKERTYPE) +
                                                            str(MARKER.KEYVALUE_SEP) +
                                                            str(MARKER.PAUSES),
                                                            str(MARKER.MARKERINFO) +
                                                            str(MARKER.KEYVALUE_SEP) +
                                                            str(round(
                                                                fto, 1)),
                                                            str(MARKER.MARKERSPEAKER) +
                                                            str(MARKER.KEYVALUE_SEP) +
                                                            str(curr_utt[-1].sLabel))
                    cm.insertToTree(curr_utt[-1].endTime,
                                    nxt_utt[0].startTime,
                                    MARKER.PAUSES,
                                    markerText)
                elif THRESHOLD.LB_MICROPAUSE == fto \
                        <= THRESHOLD.UB_MICROPAUSE:
                    logging.debug("pauses")
                    markerText = "({1}{0}{2}{0}{3})".format(MARKER.MARKER_SEP,
                                                            str(MARKER.MARKERTYPE) +
                                                            str(MARKER.KEYVALUE_SEP) +
                                                            str(MARKER.PAUSES),
                                                            str(MARKER.MARKERINFO) +
                                                            str(MARKER.KEYVALUE_SEP) +
                                                            str(round(
                                                                fto, 1)),
                                                            str(MARKER.MARKERSPEAKER) +
                                                            str(MARKER.KEYVALUE_SEP) +
                                                            str(curr_utt[-1].sLabel))
                    cm.insertToTree(curr_utt[-1].endTime,
                                    nxt_utt[0].startTime,
                                    MARKER.PAUSES,
                                    markerText)
                elif fto >= THRESHOLD.LB_LARGE_PAUSE:
                    logging.debug("pauses")
                    markerText = "({1}{0}{2}{0}{3})".format(MARKER.MARKER_SEP,
                                                            str(MARKER.MARKERTYPE) +
                                                            str(MARKER.KEYVALUE_SEP) +
                                                            str(MARKER.PAUSES),
                                                            str(MARKER.MARKERINFO) +
                                                            str(MARKER.KEYVALUE_SEP) +
                                                            str(round(
                                                                fto, 1)),
                                                            str(MARKER.MARKERSPEAKER) +
                                                            str(MARKER.KEYVALUE_SEP) +
                                                            str(curr_utt[-1].sLabel))
                    cm.insertToTree(curr_utt[-1].endTime,
                                    nxt_utt[0].startTime,
                                    MARKER.PAUSES,
                                    markerText)

        cm.buildUttMap()
        self.successful = True
        return cm

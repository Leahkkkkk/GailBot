# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:57:50
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-24 12:12:08
# Standard imports
import io
from typing import Dict, Any, List
# Local imports
from gailbot.plugins.plugin import Plugin, Methods
from gb_hilab_suite.src.gb_hilab_suite import *


class GapPlugin(Plugin):

    def __init__(self) -> None:
        super().__init__()
        self.lb_gap = GAPS_LB

    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_input: Methods) -> List:
        """
        Inserts new nodes into the BST, which represents a gap.

        1. Iterate through the word-level dictionary and retrieve an utterance
           pair
        2. Check the FTO of the utterance pair. If it matches the criterion for
           a gap and the current and next utterance are not by the same speaker,
           insert a gap marker into the tree. Else, do nothing.

        Args:
            dependency_outputs (Dict[str, Any]):
            plugin_input (Methods):

        Returns:
            convModelPlugin: the current conv model wrapper object
        """
        # Get the output of the previous plugin
        cm = dependency_outputs["conv_model"]
        utterances = cm.getUttMap(False)

        mapIter = cm.map_iterator(utterances)  # iterator
        i = mapIter.iter()  # i is the iterable object

        # while there is still an utterance pair,
        while i.hasNextPair():
            pair = i.nextPair()
            curr_utt = cm.getWordFromNode(pair[0])
            nxt_utt = cm.getWordFromNode(pair[1])

            # calculate the floor transfer offset
            fto = round(nxt_utt[0].startTime -
                        curr_utt[-1].endTime, 2)

            # only add a gap marker if speakers are different
            if fto >= self.lb_gap and \
                    curr_utt[0].sLabel != nxt_utt[0].sLabel:

                markerText = "({1}{0}{2}{0}{3})".format(
                    MARKER_SEP,
                    str(MARKERTYPE) +
                    str(KEYVALUE_SEP) +
                    str(GAPS),
                    str(MARKERINFO) +
                    str(KEYVALUE_SEP) +
                    str(round(fto, 1)),
                    str(MARKERSPEAKER) +
                    str(KEYVALUE_SEP) +
                    "NONE")
                # insert marker into the tree
                cm.insertToTree(curr_utt[-1].endTime,
                                nxt_utt[0].startTime,
                                GAPS,
                                markerText)
        self.successful = True
        return cm

# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-24 10:32:30
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-24 12:26:25


import io
from typing import Dict, Any, List
from dataclasses import dataclass
# Local imports
from gailbot.plugins.plugin import Plugin, Methods, Utt
from gb_hilab_suite.src.gb_hilab_suite import *


class PausePlugin(Plugin):
    def __init__(self) -> None:
        super().__init__()

        @dataclass
        class Thresholds:
            lb_latch = LB_LATCH
            ub_latch = UB_LATCH

            lb_pause = LB_PAUSE
            ub_pause = UB_PAUSE
            lb_micropause = LB_MICROPAUSE
            ub_micropause = UB_MICROPAUSE
            lb_large_pause = LB_LARGE_PAUSE

        @dataclass
        class Delimiters:
            latch_marker = u'\u2248'

        self.thresholds = Thresholds
        self.delimiters = Delimiters

    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_input: Methods) -> List[Utt]:
        """
        Inserts new nodes into the BST, which represents a pause.

        1. Iterate through the word-level dictionary and retrieve an utterance
           pair
        2. If by the same speaker, check the FTO of the utterance pair. If it
           matches the criterion for a pause, insert a pause marker into the
           tree. Else, do nothing.

        Args:
            dependency_outputs (Dict[str, Any]):
            plugin_input (PluginMethodSuite):

        Returns:
            convModelPlugin: the current conv model wrapper object
        """
        # Get the output of the previous plugin
        cm = dependency_outputs["conv_model"]
        utterances = cm.getUttMap(False)

        mapIter = cm.map_iterator(utterances)  # iterator
        i = mapIter.iter()  # i is the iterable object
        while i.hasNextPair():
            pair = i.nextPair()
            curr_utt = cm.getWordFromNode(pair[0])
            nxt_utt = cm.getWordFromNode(pair[1])

            if curr_utt[0].sLabel == nxt_utt[0].sLabel:
                fto = round(nxt_utt[0].startTime -
                            curr_utt[-1].endTime, 2)

                markerText = ""
                if self.thresholds.lb_latch <= fto <= self.thresholds.ub_latch:
                    markerText = "({1}{0}{2}{0}{3})".format(MARKER_SEP,
                                                            str(MARKERTYPE)
                                                            + str(KEYVALUE_SEP) +
                                                            str(PAUSES),
                                                            str(MARKERINFO) +
                                                            str(KEYVALUE_SEP) +
                                                            str(self.delimiters.latch_marker),
                                                            str(MARKERSPEAKER) +
                                                            str(KEYVALUE_SEP) +
                                                            str(curr_utt[-1].sLabel))
                    cm.insertToTree(curr_utt[-1].endTime,
                                    nxt_utt[0].startTime,
                                    PAUSES,
                                    markerText)
                elif self.thresholds.lb_pause <= fto <= self.thresholds.ub_pause:
                    # TODO: 0.8 vs -0.8
                    markerText = "({1}{0}{2}{0}{3})".format(MARKER_SEP,
                                                            str(MARKERTYPE) +
                                                            str(KEYVALUE_SEP) +
                                                            str(PAUSES),
                                                            str(MARKERINFO) +
                                                            str(KEYVALUE_SEP) +
                                                            str(round(
                                                                fto, 1)),
                                                            str(MARKERSPEAKER) +
                                                            str(KEYVALUE_SEP) +
                                                            str(curr_utt[-1].sLabel))
                    cm.insertToTree(curr_utt[-1].endTime,
                                    nxt_utt[0].startTime,
                                    PAUSES,
                                    markerText)
                elif self.thresholds.lb_micropause <= fto \
                        <= self.thresholds.ub_micropause:
                    markerText = "({1}{0}{2}{0}{3})".format(MARKER_SEP,
                                                            str(MARKERTYPE) +
                                                            str(KEYVALUE_SEP) +
                                                            str(PAUSES),
                                                            str(MARKERINFO) +
                                                            str(KEYVALUE_SEP) +
                                                            str(round(
                                                                fto, 1)),
                                                            str(MARKERSPEAKER) +
                                                            str(KEYVALUE_SEP) +
                                                            str(curr_utt[-1].sLabel))
                    cm.insertToTree(curr_utt[-1].endTime,
                                    nxt_utt[0].startTime,
                                    PAUSES,
                                    markerText)
                elif fto >= self.thresholds.lb_large_pause:
                    markerText = "({1}{0}{2}{0}{3})".format(MARKER_SEP,
                                                            str(MARKERTYPE) +
                                                            str(KEYVALUE_SEP) +
                                                            str(PAUSES),
                                                            str(MARKERINFO) +
                                                            str(KEYVALUE_SEP) +
                                                            str(round(
                                                                fto, 1)),
                                                            str(MARKERSPEAKER) +
                                                            str(KEYVALUE_SEP) +
                                                            str(curr_utt[-1].sLabel))
                    cm.insertToTree(curr_utt[-1].endTime,
                                    nxt_utt[0].startTime,
                                    PAUSES,
                                    markerText)

        cm.buildUttMap()
        self.successful = True

# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:57:50
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-24 12:11:42
# Standard imports
import io
from typing import Dict, Any, List
# Local imports
from gailbot.plugins.plugin import Plugin, Methods, Utt
from gb_hilab_suite.src.core import Word

from gb_hilab_suite.src.gb_hilab_suite import *


class OverlapPlugin(Plugin):

    def __init__(self) -> None:
        super().__init__()
        self.marker_limit = OVERLAP_MARKERLIMIT


    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_input: Methods) -> List[Utt]:
        """
        Inserts new nodes into the BST, which represent an overlap.

        1. Iterate through the word-level dictionary and retrieve an utterance
           pair
        2. If there is an overlap between the two utterances, get the 4
           overlap positions for the marker insertions.
        3. Add the overlap markers into the tree.
        Args:
            dependency_outputs (Dict[str, Any]):
            plugin_input (PluginMethodSuite):

        Returns:
            convModelPlugin: the current conv model wrapper object
        """

        # Get the output of the previous plugin
        cm = dependency_outputs["conv_model"]
        utterances = cm.getUttMap(False)
        unique_id = 0

        mapIter = cm.map_iterator(utterances) # iterator
        i = mapIter.iter() # i is the iterable object
        while i.hasNextPair():
            pair = i.nextPair()
            curr_utt = cm.getWordFromNode(pair[0])
            nxt_utt = cm.getWordFromNode(pair[1])

            # In the case of an overlap, get its 4 marker positions
            if nxt_utt[0].startTime < curr_utt[-1].endTime:

                curr_x, curr_y, nxt_x, nxt_y = self._get_overlap_positions(
                    curr_utt, nxt_utt)
                if (curr_x, curr_y, nxt_x, nxt_y) == (-1, -1, -1, -1):
                    continue

                if curr_x >= len(curr_utt):
                    curr_x = -1
                if nxt_x >= len(nxt_utt):
                    nxt_x = -1
                if curr_y >= len(curr_utt):
                    curr_y = -1
                if nxt_y >= len(nxt_utt):
                    nxt_y = -1

                markerText1 = "({1}{0}{2}{0}{3})".format(MARKER_SEP,
                                                    str(MARKERTYPE) +
                                                    str(KEYVALUE_SEP) +
                                                    str(MARKER1),
                                                    str(MARKERINFO) +
                                                    str(KEYVALUE_SEP) +
                                                    str(unique_id),
                                                    str(MARKERSPEAKER) +
                                                    str(KEYVALUE_SEP) +
                                                    curr_utt[0].sLabel)

                markerText2 = "({1}{0}{2}{0}{3})".format(MARKER_SEP,
                                                    str(MARKERTYPE) +
                                                    str(KEYVALUE_SEP) +
                                                    str(MARKER2),
                                                    str(MARKERINFO) +
                                                    str(KEYVALUE_SEP) +
                                                    str(unique_id),
                                                    str(MARKERSPEAKER) +
                                                    str(KEYVALUE_SEP) +
                                                    curr_utt[0].sLabel)

                markerText3 = "({1}{0}{2}{0}{3})".format(MARKER_SEP,
                                                    str(MARKERTYPE) +
                                                    str(KEYVALUE_SEP) +
                                                    str(MARKER3),
                                                    str(MARKERINFO) +
                                                    str(KEYVALUE_SEP) +
                                                    str(unique_id),
                                                    str(MARKERSPEAKER) +
                                                    str(KEYVALUE_SEP) +
                                                    nxt_utt[0].sLabel)

                markerText4 = "({1}{0}{2}{0}{3})".format(MARKER_SEP,
                                                    str(MARKERTYPE) +
                                                    str(KEYVALUE_SEP) +
                                                    str(MARKER4),
                                                    str(MARKERINFO) +
                                                    str(KEYVALUE_SEP) +
                                                    str(unique_id),
                                                    str(MARKERSPEAKER) +
                                                    str(KEYVALUE_SEP) +
                                                    nxt_utt[0].sLabel)

                # insert the overlap markers into the tree
                cm.insertToTree(curr_utt[curr_x].startTime,
                                curr_utt[curr_x].startTime,
                                OVERLAPS,
                                markerText1)
                cm.insertToTree(curr_utt[curr_y].endTime,
                                curr_utt[curr_y].endTime,
                                OVERLAPS,
                                markerText2)
                cm.insertToTree(nxt_utt[nxt_x].startTime,
                                nxt_utt[nxt_x].startTime,
                                OVERLAPS,
                                markerText3)
                cm.insertToTree(nxt_utt[nxt_y].endTime,
                                nxt_utt[nxt_y].endTime,
                                OVERLAPS,
                                markerText4)

                unique_id += 1

        cm.buildUttMap()
        utterances = cm.getUttMap(False)
        self.successful = True
        return cm

    def _get_overlap_positions(self, curr_utt: List[Word], nxt_utt: List[Word]):
        """
        Return the position of where the overlap markers should be inserted.
        """

        # check speaker label
        if curr_utt[0].sLabel == nxt_utt[0].sLabel:
            return (-1, -1, -1, -1)

        # when there is an overlap and diff speakers
        next_start = nxt_utt[0].startTime
        next_end = nxt_utt[-1].endTime
        curr_start = curr_utt[0].startTime
        curr_end = curr_utt[-1].endTime

        # do dummy value
        curr_overlap_start_pos = 0
        curr_overlap_end_pos = 0

        # iterate through every word in the current utterance
        for word in curr_utt:
            if word.startTime < next_end and word.endTime > next_start:
                # overlap happening
                if curr_overlap_start_pos != 0 and curr_overlap_end_pos == 0:
                    curr_overlap_end_pos = curr_overlap_start_pos
                    curr_overlap_end_pos += 1
                else:
                    curr_overlap_end_pos += 1

            else:
                if curr_overlap_end_pos == 0:
                    curr_overlap_start_pos += 1
                else:
                    break

        next_overlap_start_pos = 0
        next_overlap_end_pos = len(nxt_utt) - 1

        # iterate through every word in the next utterance
        for word in nxt_utt:
            if word.startTime < curr_end and word.endTime > curr_start:
                # overlap happening
                if next_overlap_start_pos != 0 and next_overlap_end_pos == 0:
                    next_overlap_end_pos = next_overlap_start_pos
                    next_overlap_end_pos += 1
                else:
                    next_overlap_end_pos += 1
            else:
                if next_overlap_end_pos == 0:
                    next_overlap_start_pos += 1
                else:
                    break

        if curr_overlap_end_pos == 0 and next_overlap_end_pos == 0:
            return (-1, -1, -1, -1)

        return (curr_overlap_start_pos,
                curr_overlap_end_pos,
                next_overlap_start_pos,
                next_overlap_end_pos)

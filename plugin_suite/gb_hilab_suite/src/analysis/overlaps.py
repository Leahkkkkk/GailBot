# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:57:50
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-24 12:11:42
# Standard imports
from typing import Dict, Any, List
import logging
# Local imports
from gailbot import Plugin, UttObj, GBPluginMethods
from gb_hilab_suite.src.core.nodes import Word
from gb_hilab_suite.src.core.conversation_model import ConversationModel
from gb_hilab_suite.src.configs import load_internal_marker, load_threshold, PLUGIN_NAME, MARKER_FORMATTER
MARKER = load_internal_marker() 
THRESHOLD = load_threshold()
class OverlapPlugin(Plugin):
    def __init__(self) -> None:
        super().__init__()
        self.marker_limit = THRESHOLD.OVERLAP_MARKERLIMIT

    def apply(self, 
                     dependency_outputs: Dict[str, Any],
                     methods: GBPluginMethods) -> List[UttObj]:
        """
        Inserts new nodes into the BST, which represent an overlap.

        1. Iterate through the word-level dictionary and retrieve an utterance
           pair
        2. If there is an overlap between the two utterances, get the 4
           overlap positions for the marker insertions.
        3. Add the overlap markers into the tree.
        Args:
            dependency_outputs (Dict[str, Any]):
            methods (PluginMethodSuite):

        Returns:
            convModelPlugin: the current conv model wrapper object
        """

        # Get the output of the previous plugin
        cm: ConversationModel = dependency_outputs[PLUGIN_NAME.ConvModel]
        utterances = cm.getUttMap(False)
        unique_id = 0

        mapIter = cm.map_iterator(utterances) # iterator
        i = mapIter.iter() # i is the iterable object
        logging.debug(f"start analyze overlap")
        while i.hasNextPair():
            pair = i.nextPair()
            curr_utt = cm.getWordFromNode(pair[0])
            nxt_utt = cm.getWordFromNode(pair[1])

            # In the case of an overlap, get its 4 marker positions
            if nxt_utt[0].startTime < curr_utt[-1].endTime:
                logging.debug(f"overlap detected between {nxt_utt[0].startTime} and {curr_utt[-1].endTime}")
                curr_x, curr_y, nxt_x, nxt_y = self._get_overlap_positions(curr_utt, nxt_utt)
                logging.debug(f"get overlap position {curr_x}, {curr_y}, {nxt_x}, {nxt_y}")
                if (curr_x, curr_y, nxt_x, nxt_y) == (-1, -1, -1, -1):
                    logging.warn(f"detect overlap between the same speaker")
                    continue

                if curr_x >= len(curr_utt):
                    curr_x = -1
                if nxt_x >= len(nxt_utt):
                    nxt_x = -1
                if curr_y >= len(curr_utt):
                    curr_y = -1
                if nxt_y >= len(nxt_utt):
                    nxt_y = -1

                fst_start = MARKER_FORMATTER.TYPE_INFO_SP.format(
                    MARKER.OVERLAP_FIRST_START, str(unique_id), curr_utt[0].sLabel)
                fst_end = MARKER_FORMATTER.TYPE_INFO_SP.format(
                    MARKER.OVERLAP_FIRST_END, str(unique_id), curr_utt[0].sLabel)
                snd_start = MARKER_FORMATTER.TYPE_INFO_SP.format(
                    MARKER.OVERLAP_SECOND_START, str(unique_id), nxt_utt[0].sLabel)
                snd_end = MARKER_FORMATTER.TYPE_INFO_SP.format(
                    MARKER.OVERLAP_SECOND_END, str(unique_id), nxt_utt[0].sLabel)

                logging.debug(f"insert overlap markers to the tree: first start:\
                        {fst_start}, first end: {fst_end}, snd_start: {snd_start}, snd_end: {snd_end} \
                        current speaker {curr_utt[0].sLabel} , next speaker: {nxt_utt[0].sLabel}")
                # insert the overlap markers into the tree
                cm.insertToTree(curr_utt[curr_x].startTime,
                                curr_utt[curr_x].startTime,
                                MARKER.OVERLAPS,
                                fst_start)
                cm.insertToTree(curr_utt[curr_y].endTime,
                                curr_utt[curr_y].endTime,
                                MARKER.OVERLAPS,
                                fst_end)
                cm.insertToTree(nxt_utt[nxt_x].startTime,
                                nxt_utt[nxt_x].startTime,
                                MARKER.OVERLAPS,
                                snd_start)
                cm.insertToTree(nxt_utt[nxt_y].endTime,
                                nxt_utt[nxt_y].endTime,
                                MARKER.OVERLAPS,
                                snd_end)
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

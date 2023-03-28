# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-24 09:03:48
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-24 12:08:07

# Standard imports
from typing import Any, Dict, List
import random
import re
from math import floor
from gailbot import Plugin, GBPluginMethods,  UttObj
from gb_hilab_suite.src.core.nodes import Node


class WordTreePlugin(Plugin):
    """Creates a Binary Search Tree of nodes for word-level analysis"""

    def __init__(self):
        super().__init__()

    def apply(self, dependency_outputs: Dict[str, Any],
                     methods: GBPluginMethods) -> Node:
        """
        Adds words from an utterance map to construct a balanced BST with each
        node containing a Word object corresponding to a word from transcript.
        Goes through all of the utterances and sorts them.

        1. Loop through utterances to check number of speakers in this file
        2. For every utterance (word-level), add to the tree
        3. When there is more than one file being read in, increment label by i
           to make each speaker label unique.

        Args:
            dependency_outputs (Dict[str, Any]):
            methods (PluginMethodSuite):

        Returns:
            Node: root node of the BST
        """
        utterances_map: Dict[str, List[UttObj]] = methods.get_utterance_objects()
        root = None

        i = 0
        if len(utterances_map.values()) == 1 and list(utterances_map.values())[0] == []:
            root = Node(0, 1, "0", "empty")
        else:
            for _, utterances in utterances_map.items():
                k = self.__speakerNum(utterances)
                random.shuffle(utterances)
                for utt in utterances:
                    if (root == None):
                        root = Node(utt.start,
                                    utt.end,
                                    # NOTE
                                    "0" + str(self._getIntLabel(utt.speaker) + i),
                                    utt.text)
                    else:
                        self._insert(
                            root, 
                            utt.start,
                            utt.end,
                            "0" + str(self._getIntLabel(utt.speaker) + i),
                            utt.text)
                i += k
            
        self.successful = True
        return root
    ######################################################################
    ################## BELOW ARE HELPER FUNCTIONS ########################
    ######################################################################

    def _insert(self, root: Node, start_time: float, end_time: float,
               speaker_label: str, text: str) -> Node:
        """
        Inserts a new node into the BST using start time (in secs) as index.

        Args:
            start_time (float): start time.
            end_time (float): End time.
            speaker_label (str): Speaker label.
            text (str): Word that the node stores.

        Returns:
             Node
        """
        if root is None:
            return Node(start_time, end_time, speaker_label, text)
        else:
            if root.val.startTime == start_time:
                return
            elif root.val.startTime < start_time:
                root.right = self._insert(
                    root.right, start_time, end_time, speaker_label, text)
            else:
                root.left = self._insert(
                    root.left, start_time, end_time, speaker_label, text)
        return root

    def __sortedArrayToBST(self, arr: List[UttObj]):
        """
        Makes the binary search tree balanced
        credit: https://www.geeksforgeeks.org/sorted-array-to-balanced-bst/

        Args:
            arr (Utt): list of uttered words

        Returns:
            Node: root of the balanced BST
        """
        if not arr:
            return None

        mid = floor((len(arr)) / 2)
        root = Node(
            arr[mid].start,
            arr[mid].end,
            arr[mid].speaker,
            arr[mid].text)
        root.left = self.__sortedArrayToBST(arr[:mid])
        root.right = self.__sortedArrayToBST(arr[mid+1:])

        return root

    # return the number of spealer in utterances
    def __speakerNum(self, utterances: List[UttObj]):
        """
        Returns the number of speakers in a file.

        Args:
            utterances (Utt): list of uttered words

        Returns:
            int: number of speakers
        """
        speakerSet = set()
        for utt in utterances:
            if utt.speaker not in speakerSet:
                speakerSet.add(utt.speaker)
        return len(speakerSet)


    def _getIntLabel(self, speakerLabel) -> int:
        patterns = [
        r"(?i)speaker\s?(\d+)",
        r"(?i)speaker(\d+)",
        r"(?i)speaker(\d{2})",
        r"(?i)speaker_?0?(\d)",
        r"(\d+)"
        ]

        # Try each pattern in turn and return the first matching integer
        for pattern in patterns:
            match = re.search(pattern, speakerLabel)
            if match:
                return int(match.group(1))
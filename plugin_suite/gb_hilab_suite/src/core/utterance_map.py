# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-24 09:12:13
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-24 11:58:42

# Standard imports
from typing import List, Any, Dict
#import re
from copy import deepcopy
# Local imports
from gb_hilab_suite.src.configs import INTERNAL_MARKER, load_threshold
from gailbot import Plugin, GBPluginMethods
from gb_hilab_suite.src.core.nodes import Node
MARKER = INTERNAL_MARKER 
THRESHOLD = load_threshold()
class UtteranceMapPlugin(Plugin):
    def __init__(self) -> None:
        super().__init__()
        self.turn_end_threshold_secs = THRESHOLD.TURN_END_THRESHOLD_SECS

    def apply(self, 
                     dependency_outputs: Dict[str, Any],
                     methods: GBPluginMethods) -> Dict:
        """
        Initializes, populates and returns a word-level dictionary of utterances,
        which are represented by Word objects.

        Args:
            dependency_outputs (Dict[str, Any]):
            methods (PluginMethodSuite):

        Returns:
            Dict: a dictionary of utterances.
        """
        root: Node = dependency_outputs["WordTreePlugin"]
        # create the dictionary here
        uttDict : Dict[str, List[Node]] = dict()
        # set the ID as 0 as first list element, populate dict and pop it
        myFunction = self.outer_create_dict(0)
        myFunction(root, uttDict)
        self.successful = True
        return uttDict

    ######################## HELPERS #######################################

    def outer_create_dict(self, id_arg):
        id = id_arg
       
        def create_dict(currNode: Node, uttDict: Dict[str, List[Node]]):
            nonlocal id
            currSL = currNode.val.sLabel

            """
            Given the root of a tree, create an utterance dictionary that
            maps a speaker ID to a list of utterances.

            Args:
                currNode (Node): current node to be added
                uttDict (Dict[int:List[Node]]): utterance map
            """
            if currNode.left is not None:
                create_dict(currNode.left, uttDict)

            if (currNode.val.startTime is not None) and (currSL not in MARKER.INTERNAL_MARKER_SET):

                # create the first list in our dictionary
                if id == 0:
                    newList = list()
                    newList.append(currNode)
                    id += 1
                    # create a new list with updated speaker label ID
                    uttDict[id] = newList

                elif id < 2:
                    # calculate fto & combine utterance based on sLabel + threshold
                    fto = currNode.val.startTime - uttDict[id][-1].val.endTime
                    if currSL == uttDict[id][-1].val.sLabel and fto < self.turn_end_threshold_secs:
                        uttDict[id].append(currNode)
                    # if not, create a new list add current node to new list
                    else:
                        newList = list()
                        newList.append(currNode)
                        id += 1
                        uttDict[id] = newList

                else:
                    # calculate fto & combine utterance based on sLabel + threshold
                    fto = currNode.val.startTime - uttDict[id][-1].val.endTime

                    index2 = id
                    while index2 > 1 and uttDict[index2][-1].val.sLabel in MARKER.INTERNAL_MARKER_SET:
                        index2 -= 1
                    fto2 = currNode.val.startTime - \
                        uttDict[index2][-1].val.endTime

                    index3 = id
                    while index3 > 1 and (uttDict[index3][-1].val.sLabel != currSL):
                        index3 -= 1
                    fto3 = currNode.val.startTime - \
                        uttDict[index3][-1].val.endTime

                    if currSL == uttDict[id][-1].val.sLabel and fto < self.turn_end_threshold_secs:
                        uttDict[id].append(currNode)
                    elif currSL == uttDict[index2][-1].val.sLabel and fto2 < self.turn_end_threshold_secs:
                        uttDict[index2].append(currNode)
                    elif fto3 < self.turn_end_threshold_secs and currSL == uttDict[index3][-1].val.sLabel:
                        uttDict[index3].append(currNode)

                    # if not, create a new list add current node to new list
                    else:
                        newList = list()
                        newList.append(currNode)
                        id += 1
                        uttDict[id] = newList

            if currNode.right is not None:
                create_dict(currNode.right, uttDict)
                
        return create_dict

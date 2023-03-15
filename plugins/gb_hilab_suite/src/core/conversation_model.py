# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-24 09:26:01
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-24 12:30:15


from copy import deepcopy
from typing import Dict, Any, List

# Local imports
from gb_hilab_suite.src.core.nodes import Word, Node
from gb_hilab_suite.src.core.utterance_map import UtteranceMapPlugin
from gailbot.plugins.plugin import Plugin, Methods, Utt
from gb_hilab_suite.src.gb_hilab_suite import *


class ConversationModel:
    """
    This class is a wrapper around ConversationModel, with helper methods to interact
    with the underlying data structure.
    Intended to be used for API calls by subsequent layers.
    """

    Tree = None
    Maps = dict()

    ######################################################################
    ################## BELOW ARE PUBLIC FUNCTIONS ########################
    ######################################################################

    ################## BELOW ARE ITERATOR CLASSES ######################
    class map_iterator:
        """
        Inner class that implements an iterator for the utterance map
        """

        def __init__(self, map):
            """
            Sets the map to iterator over, with an initialized list of keys
            """
            self.map = map
            self.list = list(self.map.keys())

        def iter(self):
            """
            Returns the iterator object (the dictionary) itself
            """
            self.curr = 0
            return self

        def hasNext(self):
            return self.curr < len(self.list)

        def next(self):
            """
            Iterates through all iterable items in the specified dictionary
            """
            if self.hasNext():
                result = self.list[self.curr]
                self.curr += 1
                return self.map[result]
            else:
                raise StopIteration

        def hasNextPair(self):
            return self.curr < len(self.list) and self.curr + 1 < len(self.list)

        def nextPair(self):
            """
            Returns a pair of utterances from the specified dictionary. If there
            is only one last utterance, return with an empty list.
            """
            if self.hasNextPair():
                result = [self.map[self.list[self.curr]],
                          self.map[self.list[self.curr + 1]]]
                self.curr += 1
                return result
            elif self.curr == len(self.list) - 1:
                result = [self.map[self.list[self.curr]],
                          []]
                self.curr += 1
                return result
            else:
                raise StopIteration

        def reset(self):
            """
            Sets the iterator back to its starting point
            """
            self.curr = 0
            return self

    ################## BELOW ARE TREE FUNCTIONS ########################
    # @dataclass
    class tree_iterator:
        """
        Inner class that implements an iterator of the tree
        """

        def __init__(self, root):
            """
            Returns the iterator object (of the tree)
            """
            self.root = root
            self.list = []
            self.root.inorder(self.list)

        def iter(self):
            """
            Returns the iterable initialized to be at the left most node
            """
            # curr should equal left most node
            self.curr = 0
            return self

        def next(self):
            """
            Return the value of the curr node while advancing to point to next
            node
            """
            if self.curr < len(self.list):
                result = self.list[self.curr]
                self.curr += 1
                return result
            else:
                raise StopIteration

        def hasNext(self):
            """
            Return true if the iterator is not at the end of the tree
            """
            return self.curr < len(self.list)

        def __reset__(self):
            """
            Reset to point to the left most node
            """
            self.curr = 0
            return self


    def getTree(self, copy: bool) -> Node:
        """
        Returns either the current tree itself or its deep copy.

        Args:
            copy (bool): boolean to indicate whether or not to return a deep
                         copy of the tree.

        Returns:
            Node: either the root node of the current tree itself or its deep
                  copy
        """
        if copy:
            return deepcopy(self.Tree)
        return self.Tree

    def getTurnMap(self, copy: bool) -> map:
        """
        Returns either the word-level dictionary itself or its deep copy.

        Args:
            copy (bool): boolean to indicate whether or not to return a deep
                         copy of the word-level dictionary.

        Returns:
            Map: either the word-level dictionary itself or its deep copy.
        """
        if copy:
            return deepcopy(self.Maps["map1"])
        return self.Maps["map1"]

    def getConvDict(self, copy: bool) -> map:
        """
        Returns either the conversation-level dictionary itself or its
        deep copy.

        Args:
            copy (bool): boolean to indicate whether or not to return a deep
                         copy of the conversation-level dictionary.

        Returns:
            Map: either the conversation-level dictionary itself or its deep
                 copy.
        """
        if copy:
            return deepcopy(self.Maps["map3"])
        return self.Maps["map3"]

    def insertToTree(self, startTime, endTime, sLabel, text) -> None:
        """
        Inserts a new node into the tree.
        """
        self.Tree.insert(self.Tree, startTime, endTime, sLabel, text)

    def searchTree(self, startTime) -> Word:
        """
        Searches for a node based on its start time in the tree.
        """
        return self.Tree.search(self.Tree, startTime)

    def deleteFromTree(self, startTime) -> None:
        """
        Deletes a node, which is found based on its start time, from the tree.
        """
        self.Tree.deleteNode(self.Tree, startTime)

    ################## BELOW ARE UTTMAP FUNCTIONS ########################

    def buildUttMap(self):
        """
        Called to rebuild the utterance map after modification of the tree

        (Note: reuse the outer_create_dict of utteranceDict plugin)
        """
        root = self.Tree
        uttDict = dict()
        ud = UtteranceMapPlugin()
        myFunction = ud.outer_create_dict(0)
        myFunction(root, uttDict)
        self.Maps["map1"] = uttDict

    def toReplace(self, inputNode, varDict):
        """
        Called to rebuild the utterance map after modification of the tree

        (Note: reuse the outer_create_dict of utteranceDict plugin)
        """

        currSL = inputNode.val.sLabel

        if inputNode.val.sLabel in INTERNAL_MARKER_SET:
            arr = inputNode.val.text[1 : len(inputNode.val.text)-1].split(MARKER_SEP)
            currSL = (arr[-1].split(KEYVALUE_SEP))[-1]
            temp = arr[0].split(KEYVALUE_SEP)[-1]
            markerInfo = arr[1].split(KEYVALUE_SEP)[-1]

            if inputNode.val.sLabel in varDict:
                surfaceFormat = varDict[temp]

                # specific to XMLSCHEMA plugin for PAUSES marker HACK
                if surfaceFormat == PAUSES:
                    newNode = Node(inputNode.val.startTime,
                               inputNode.val.endTime,
                               currSL,
                               surfaceFormat + KEYVALUE_SEP + markerInfo)
                    # print(surfaceFormat + KEYVALUE_SEP + markerInfo)
                    return newNode

                newNode = Node(inputNode.val.startTime,
                               inputNode.val.endTime,
                               currSL,
                               surfaceFormat)
                return newNode

            for _, (underlyFormat, val) in enumerate(varDict.items()):
                if inputNode.val.text.find(underlyFormat) != -1:
                    newNode = Node(inputNode.val.startTime,
                                   inputNode.val.endTime,
                                   currSL,
                                   val)
                    return newNode

            newNode = Node(inputNode.val.startTime,
                           inputNode.val.endTime,
                           currSL,
                           inputNode.val.text)
            return newNode
        return inputNode

    def outer_buildUttMapWithChange(self, id_arg):
        id = id_arg

        def buildUttMapWithChange(currNode, outputUttDict, varDict):
            """
            Called to build a utterance map with marker nodes substituted with the
            corresponding external format

            """
            nonlocal id
            currSL = currNode.val.sLabel
            if currNode.val.sLabel in INTERNAL_MARKER_SET:
                arr = currNode.val.text[1 : len(currNode.val.text)-1].split(MARKER_SEP)
                currSL = (arr[-1].split(KEYVALUE_SEP))[-1]

            if currNode.left is not None:
                buildUttMapWithChange(currNode.left, outputUttDict, varDict)

            if currNode.val.startTime is not None:
                # create the first list in our dictionary
                if (id == 0):
                    newList = list()
                    newList.append(self.toReplace(currNode, varDict))
                    id += 1
                    outputUttDict[id] = newList

                elif id < 2:
                    # calculate fto & combine utterance based on sLabel + threshold
                    fto = currNode.val.startTime - outputUttDict[id][-1].val.endTime

                    if currSL == outputUttDict[id][-1].val.sLabel and fto < TURN_END_THRESHOLD_SECS:
                        outputUttDict[id].append(self.toReplace(currNode, varDict))
                    # if not, create a new list add current node to new list
                    else:
                        newList = list()
                        newList.append(self.toReplace(currNode, varDict))
                        id += 1
                        outputUttDict[id] = newList

                else:
                    # calculate fto & combine utterance based on sLabel + threshold
                    fto = currNode.val.startTime - outputUttDict[id][-1].val.endTime

                    index2 = id
                    while index2 > 1 and outputUttDict[index2][-1].val.sLabel in INTERNAL_MARKER_SET:
                        index2 -= 1
                    fto2 = currNode.val.startTime - outputUttDict[index2][-1].val.endTime

                    index3 = id
                    while index3 > 1 and (outputUttDict[index3][-1].val.sLabel != currSL):
                        index3 -= 1
                    fto3 = currNode.val.startTime - outputUttDict[index3][-1].val.endTime

                    if currSL == outputUttDict[id][-1].val.sLabel and fto < TURN_END_THRESHOLD_SECS:
                        outputUttDict[id].append(self.toReplace(currNode, varDict))
                    elif currSL == outputUttDict[index2][-1].val.sLabel and fto2 < TURN_END_THRESHOLD_SECS:
                        outputUttDict[index2].append(self.toReplace(currNode, varDict))
                    elif fto3 < TURN_END_THRESHOLD_SECS and currSL == outputUttDict[index3][-1].val.sLabel:
                        outputUttDict[index3].append(self.toReplace(currNode, varDict))

                    # if not, create a new list add current node to new list
                    else:
                        newList = list()
                        newList.append(self.toReplace(currNode, varDict))
                        id += 1
                        outputUttDict[id] = newList

            if currNode.right is not None:
                buildUttMapWithChange(currNode.right, outputUttDict, varDict)

        return buildUttMapWithChange

    def getUttMap(self, copy: bool):
        """
        Returns either the utterance-level dictionary itself or its
        deep copy.

        Args:
            copy (bool): boolean to indicate whether or not to return a deep
                         copy of the utterance-level dictionary.

        Returns:
            Map: either the utterance-level dictionary itself or its deep
                 copy.
        """
        if copy:
            return deepcopy(self.Maps["map1"])
        return self.Maps["map1"]

    # def printUttMap(self):
    #     """
    #     Prints the keys and values of the word-level dictionary.
    #     """
    #     for key, item in self.Maps["map1"].items():
    #         print(key)
    #         for i in item:
    #             print(i.val.text, end=' ')
    #         print()

    # TODO: Change the list generation loops to list comprehension.
    def getWordFromNode(self, listNode):
        """
        Return a list of inner Words from a list of Node

        Args:
            listNode (list[Node]): a list of Node

        Returns:
            list of inner Words
        """
        return [node.val for node in listNode]

    def getUttFromUttMap(self, id, copy: bool):
        """
        Get the utterance speficied by the id
        """
        listNode = self.Maps["map1"][id]
        listWord = list()

        if copy:
            for node in listNode:
                listWord.append(deepcopy(node.val))
        else:
            for node in listNode:
                listWord.append(node.val)
        return listWord

    def insertNodeToUtt(self, id, newNode, pos):
        """
        Insert a new node to the utterance list specified by the id
        """
        self.Maps["map1"][id].insert(pos, newNode)

    def updateUttMap(self, map):
        """
        Update the given map to ConversationModel
        """
        self.Maps["map1"] = map

    ################## BELOW ARE SPEAKERMAP FUNCTIONS ########################
    def getSpeakerMap(self, copy: bool) -> map:
        """
        Returns either the speaker-level dictionary itself or its deep copy.

        Args:
            copy (bool): boolean to indicate whether or not to return a deep
                         copy of the speaker-level dictionary.

        Returns:
            Map: either the speaker-level dictionary itself or its deep copy.
        """
        if copy:
            return deepcopy(self.Maps["map2"])
        return self.Maps["map2"]

    # def printSpeakerMap(self, speakerDict):
    #     """
    #     Prints the keys and values of the speaker-level dictionary.
    #     """
    #     # iterate through the speaker dictionary by its speaker labels
    #     for sLabelKey, item in speakerDict.items():
    #         print("Speaker #: ", end='')
    #         print(sLabelKey)

    #         # iterate through the value, which is a Dict of Dicts
    #         for utterancesList in item["utteranceList"]:
    #             for utterances in utterancesList:
    #                 print(utterances.val.text, end=' ')
    #             print()

    ################## HELPER FUNCTIONS ########################




class ConversationModelPlugin(Plugin):
    def __init__(self) -> None:
        super().__init__()

    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_input: Plugin) -> ConversationModel:
        """
        Initializes, populates and returns an instance of ConversationModel,
        which contains a tree and three maps.

        Args:
            dependency_outputs (Dict[str, Any]):
            plugin_input (PluginMethodSuite):

        Returns:
            ConversationModelPlugin: a wrapper object.
        """

        cm = ConversationModel()

        cm.Tree = dependency_outputs["word_tree"]

        cm.Maps = dict()
        cm.Maps["map1"] = dependency_outputs["utterance_map"]
        cm.Maps["map2"] = dependency_outputs["speaker_map"]
        cm.Maps["map3"] = dependency_outputs["conversation_map"]

        self.successful = True
        return cm

# -*- coding: utf-8 -*-
# @Author: 2022 spring interns
# @Date:   2022-2-12
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-05-03 17:48:15

# Standard imports
from typing import List, Any, Dict
#import re
from copy import deepcopy
# Local imports
from gailbot.plugins import GBPlugin, PluginMethodSuite, Utt
from layer00.treeComponents import Word, Node


class speakerDict(GBPlugin):

    def __init__(self) -> None:
        super().__init__()

    def printDict(self, speakerDict):
        """
        Prints the keys and values of a given speaker-level dictionary,
        which maps speaker labels to lists of utterances (represented as
        Word objects)

        Args:
            speakerDict (Dict[str, Dict[]]):
        """
        # iterate through the speaker dictionary by its speaker labels
        for sLabelKey, item in speakerDict.items():
            print("Speaker #: ", end='')
            print(sLabelKey)

            # iterate through the value, which is a Dict of Dicts
            for utterancesList in item["utteranceList"]:
                for utterances in utterancesList:
                    print(utterances.val.text, end=' ')
                print()

    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_input: PluginMethodSuite) -> Dict[int, Dict[str, Any]]:
        """
        Creates a dictionary for speaker-level analysis of transcription.

        1. Create a new speaker dictionary
        2. Iterates through every utterance in the given word-level dictionary
        3. If the speaker dictionary has an existing speaker label for the
           current utterance being iterated over in the word-level dictionary,
           add the utterance to the speaker dictionary.
           Else, create a new list of utterances with that speaker label in the
           speaker dictionary.

        Args:
            dependency_outputs (Dict[str, Any]):
            plugin_input (PluginMethodSuite):

        Returns:
            Dict[int, Dict[str, Any]]: Dict of Dicts for each speaker
        """
        utteranceDict = dependency_outputs["utteranceDict"]

        # create the dictionary here
        speakerDict = dict()

        # iterate through each utterance in the utterance dictionary
        for utteranceList in utteranceDict.values():

            # if speaker label in dictionary, add utterance to dict
            if utteranceList[0].val.sLabel in speakerDict:
                speakerDict[utteranceList[0].val.sLabel]["utteranceList"].append(
                    utteranceList)
            else:
                # if not, create new utterance list for the speaker dictionary
                newList = list()
                newDict = dict()
                speakerDict[utteranceList[0].val.sLabel] = newDict
                speakerDict[utteranceList[0].val.sLabel]["utteranceList"] = newList

        self.successful = True
        return speakerDict

# -*- coding: utf-8 -*-
# @Author: 2022 spring interns
# @Date:   2022-2-12
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-03-18 09:44:32

# Standard imports
from typing import Any, Dict
# import re / import List
from copy import deepcopy
# Local imports
from gailbot.plugins import GBPlugin, PluginMethodSuite

class conversationDict(GBPlugin):

    def __init__(self) -> None:
        super().__init__()

    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_input: PluginMethodSuite) -> Dict:
        """
        Creates a dictionary for conversational-level analysis of transcription.

        Args:
            dependency_outputs (Dict[str, Any]):
            plugin_input (PluginMethodSuite):

        Returns:
            Dict[str, Dict[str, Dict]]: for conversational-level analysis
        """
        try:
            conversationDict = dict()
            conversationDict["wordLevel"] = dict()
            conversationDict["uttLevel"] = dict()
            conversationDict["speakerLevel"] = dict()
            conversationDict["convLevel"] = dict()
            self.successful = True
            return conversationDict

        except Exception as E:
            print("exception in conversation")
            print(E)
            path = "{}/{}.txt".format(plugin_input.get_result_directory_path(), "exception_constructTree")
            with io.open(path, "w", encoding='utf-8') as outfile:
                outfile.write(E)
                self.successful = False

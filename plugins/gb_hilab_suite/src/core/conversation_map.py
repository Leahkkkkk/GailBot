# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-24 09:24:19
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-24 11:47:50

# Standard imports
from typing import Any, Dict
# import re / import List
from copy import deepcopy
# Local imports
from gailbot.plugins.plugin import Plugin, Methods, Utt

class ConversationMapPlugin(Methods):

    def __init__(self) -> None:
        super().__init__()

    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_input: Plugin) -> Dict:
        """
        Creates a dictionary for conversational-level analysis of transcription.

        Args:
            dependency_outputs (Dict[str, Any]):
            plugin_input (PluginMethodSuite):

        Returns:
            Dict[str, Dict[str, Dict]]: for conversational-level analysis
        """
        conversationDict = dict()
        conversationDict["wordLevel"] = dict()
        conversationDict["uttLevel"] = dict()
        conversationDict["speakerLevel"] = dict()
        conversationDict["convLevel"] = dict()
        self.successful = True
        return conversationDict
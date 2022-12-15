# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-02-24 12:08:41
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-05-03 17:48:10
# Standard imports
from typing import Any, Dict
# import re / import List
from copy import deepcopy
# Local imports
from gailbot.plugins import GBPlugin, PluginMethodSuite, Utt
from layer00.convModel import convModel
from dataclasses import dataclass


class convModelPlugin(GBPlugin):

    def __init__(self) -> None:
        super().__init__()

    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_input: PluginMethodSuite) -> convModel:
        """
        Initializes, populates and returns an instance of convModel,
        which contains a tree and three maps.

        Args:
            dependency_outputs (Dict[str, Any]):
            plugin_input (PluginMethodSuite):

        Returns:
            convModelPlugin: a wrapper object.
        """
        cm = convModel()

        cm.Tree = dependency_outputs["constructTree"]

        cm.Maps = dict()
        cm.Maps["map1"] = dependency_outputs["utteranceDict"]
        cm.Maps["map2"] = dependency_outputs["speakerDict"]
        cm.Maps["map3"] = dependency_outputs["conversationDict"]

        self.successful = True
        return cm

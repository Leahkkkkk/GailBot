# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-09 13:15:46
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-09 13:18:57
# Standard imports
from typing import Dict, Any, List, Tuple
from copy import deepcopy
# Local imports
from .vars import *
# Third party imports
from Src import GBPlugin, PluginMethodSuite, Utt


class Overlps(GBPlugin):
    """
    Detect overlapping speech between TCUs and add delimiters to mark this speech.
    Dependencies: TCU
    """

    def __init__(self) -> None:
        super().__init__()

    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_input: PluginMethodSuite) -> List[Utt]:
        # Obtain results from TCU plugin
        tcus: List[Utt] = dependency_outputs["TCU"]

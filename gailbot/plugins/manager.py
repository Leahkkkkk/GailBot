# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 13:22:01
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-08 13:46:26


from typing import Dict, List
from dataclasses import dataclass


from .plugin import Plugin
from .suite import PluginSuite

@dataclass
class PluginDetails:
    pass

class PluginManager:
    """
    Manage multiple plugins suites that can br registered, including
    storing the plugin files, parsing the config files, and instantiating
    plugin objects from files.
    """

    def __init__(self):
        pass

    def register_suite(self, suite_name : str, source_path : str) -> Dict:
        """Register plugin suite and return details"""
        pass

    def apply_suite(self, plugin_names : List[str]) -> Dict:
        pass

    def get_suite_details(self, suite_name : str) -> Dict:
        pass




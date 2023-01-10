# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 13:22:01
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-10 15:01:16


from typing import Dict, List, Any
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

    def __init__(
        self,
        workspace_dir : str
    ):
        pass

    def reset_workspace(self) -> bool:
        pass

    def register_suite(
        self,
        suite_name : str,
        conf_path : str
    ) -> Dict:
        """Register plugin suite and return details"""
        pass

    def apply_suite(
        self,
        suite_name : str,
        plugin_names : List[str],
        base_input : Any
    ) -> Dict:
        pass

    def get_suite_details(
        self,
        suite_name : str
    ) -> Dict:
        pass

    def _download_official_plugins(self):
        pass




# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 13:22:39
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-08 13:45:41

from typing import Dict, List
from dataclasses import dataclass


from .plugin import Plugin


class PluginSuite:
    """
    Manages a suite of plugins and responsible for loading, queries, and
    execution.
    Needs to store the details of each plugin (source file etc.)
    """

    def __init__(
        self,
        dependency_map : Dict[str, str],
        plugins : List[Plugin]
    ):
        pass

    def __repr__(self):
        pass

    def __call__(
        self,
        plugin_names : List[str]
    ) -> Dict:
        """
        Apply the specified plugins when possible and return the results
        summary
        """
        pass

    def is_plugin(self, plugin_name : str) -> bool:
        pass

    def plugin_names(self) -> List[str]:
        """Get names of all plugins"""
        pass

    def plugin_details(self, plugin_name : str) -> Dict:
        pass

    def check_potential_executions(self, plugin_names : List[str]) -> List[str]:
        """
        Get the names of the plugins that will actually run if the given
        plugins were attempted to be executed.
        """
        pass

    def dependency_graph(self) -> Dict:
        """Return the entire dependency graph as a dictionary"""
        pass


    def _load_plugin(self):
        pass


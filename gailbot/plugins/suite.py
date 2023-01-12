# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 13:22:39
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-12 14:34:14

from typing import Dict, List, Any
from dataclasses import dataclass

from gailbot.core.pipeline import Pipeline, Component, ComponentResult, ComponentState
from gailbot.core.utils.general import (
    is_file,
    is_directory,
    paths_in_dir,
    get_name
)

from .plugin import Plugin, Methods

class PluginComponent(Component):

    def __init__(self, plugin : Plugin):
        self.plugin = plugin

    def __call__(
        self,
        dependency_outputs : Dict[str, ComponentResult],
        methods : Methods
    ):

        # Extract the actual dependeny results
        dep_outputs = {
            k : v.result for k,v in dependency_outputs.items()
        }
        # Simply call the plugin and return its results
        result = self.plugin.apply(dep_outputs, methods)
        return ComponentResult(
            state=ComponentState.SUCCESS if self.plugin.is_successful else \
                ComponentState.FAILED,
            result=result,
            runtime=0
        )


# TODO: Implement mechanism for creating dependency map and dynamically loading
# plugin classes from config files.
class PluginSuite:
    """
    Manages a suite of plugins and responsible for loading, queries, and
    execution.
    Needs to store the details of each plugin (source file etc.)
    """

    _SUITE_CONFIG_EXT = "toml"

    def __init__(
        self,
        suite_dir_path : str
    ):
        if not is_directory(suite_dir_path):
            raise Exception(
                f"Not a directory: {suite_dir_path}"
            )
        # Load the conf file
        # TODO: Add a more sophisticated way - for now this just gets
        # the first toml file.
        self.conf_path = paths_in_dir(
            suite_dir_path,extensions=[self._SUITE_CONFIG_EXT])[0]
        self.name = get_name(suite_dir_path)

        self.plugins : Dict[str, Plugin] = dict()

        # Generate the dependency map and load a pipeline component
        self.dependency_map : Dict[str, List[str] ]= dict()
        self.components = {
            k : PluginComponent(v) for k,v in self.plugins.items()
        }
        self.pipeline = Pipeline(self.dependency_map,self.components)


    @property
    def name(self) -> str:
        return self.name

    @property
    def is_ready(self):
        pass

    def details(self) -> Dict:
        pass

    def __repr__(self):
        pass

    def __call__(
        self,
        base_input : Any,
        methods : Methods
    ) -> Dict:
        """
        Apply the specified plugins when possible and return the results
        summary
        """
        result = self.pipeline({
            "base_input" : base_input,
            "methods" : methods
        })
        return result# TODO: Determine exact type of result and return the correct thing/

    def is_plugin(self, plugin_name : str) -> bool:
        return plugin_name in self.plugins

    def plugin_names(self) -> List[str]:
        """Get names of all plugins"""
        return list(self.plugins.keys())

    def plugin_details(self, plugin_name : str) -> Dict:
        # TODO: Potentially store additional things beyond plugin dependencies

        if self.is_plugin(plugin_name):
            return {
                "dependencies" : self.dependency_map[plugin_name]
            }

    # def check_potential_executions(self, plugin_names : List[str]) -> List[str]:
    #     """
    #     Get the names of the plugins that will actually run if the given
    #     plugins were attempted to be executed.
    #     """
    #     pass

    def dependency_graph(self) -> Dict:
        """Return the entire dependency graph as a dictionary"""
        return self.pipeline.dependency_graph()

# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 13:22:39
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 13:10:57

import sys
import os
from typing import Dict, List, Any
from dataclasses import dataclass
import time
import importlib
import imp

from gailbot.core.pipeline import Pipeline, Component, ComponentResult, ComponentState
from gailbot.core.utils.general import (
    is_file,
    is_directory,
    paths_in_dir,
    get_name
)

from .plugin import Plugin, Methods

class PluginComponent(Component):
    """
    This is an adapter because the Plugin expects different args as compared
    to pipeline components.
    This is needed to so that ComponentResult component is not passed to the user.
    """

    def __init__(self,
        plugin : Plugin
    ):
        self.plugin = plugin

    def __repr__(self):
        return str(self.plugin)

    def __call__(
        self,
        dependency_outputs : Dict[str, ComponentResult],
        methods : Methods
    ):
        """
        In addition to dependency outputs, this expects methods which can be
        passed to the individual plugins.
        """

        # Extract the actual dependency results
        dep_outputs = {
            k : v.result for k,v in dependency_outputs.items()
        }
        # Simply call the plugin and return its results
        start = time.time()
        result = self.plugin.apply(dep_outputs, methods)
        elapsed = time.time() - start
        return ComponentResult(
            state=ComponentState.SUCCESS if self.plugin.is_successful else \
                ComponentState.FAILED,
            result=result,
            runtime=elapsed
        )


# TODO: Implement mechanism for creating dependency map and dynamically loading
# plugin classes from config files.
class PluginSuite:
    """
    Manages a suite of plugins and responsible for loading, queries, and
    execution.
    Needs to store the details of each plugin (source file etc.)
    """

    def __init__(
        self,
        dict_conf : Dict
    ):

        # TODO: Parse the dict config to generate the plugins map and
        # dependency map.
        """ a dictionary of the dependency map  -> pipeline argument  """
        self.dict_conf = dict_conf

        # NOTE: This is where classes should be dynamically loaded.
        # self.plugins : Dict[str, Plugin] = dict()
        # self.dependency_map : Dict[str, List[str] ]= dict()
        self.dependency_map, self.plugins = self._load_from_config(dict_conf)

        """ we ge the plugin, wrapped in component """
        # Wrap the plugins in PluginComponent
        self.components = {
            k : PluginComponent(v) for k,v in self.plugins.items()
        }

        # Init the pipeline based on the components
        self.pipeline = Pipeline(self.dependency_map,self.components)
        # Add vars here from conf.
        self._name = dict_conf["suiteName"]

        # TODO: Add mechanism to make sure all the required plugins were loaded.

        self._is_ready = True


    @property
    def name(self) -> str:
        return self._name

    @property
    def is_ready(self):
        return self._is_ready


    def __repr__(self):
        return (
            f"Suite: {self.name}\n"
            f"Dependency map: {self.dependency_graph()}"
        )

    def __call__(
        self,
        base_input : Any,
        methods : Methods
    ) -> Dict:
        """
        Apply the specified plugins when possible and return the results
        summary
        """
        result = self.pipeline(
            base_input=base_input, 
            additional_component_kwargs={
                "methods" : methods
            }
        )

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

    def dependency_graph(self) -> Dict:
        """Return the entire dependency graph as a dictionary"""
        return self.pipeline.get_dependency_graph()


    ##########
    # PRIVATE
    ##########

    # TODO: Need to implement a robust method to load plugins.
    def _load_from_config(self, dict_config : Dict) -> None:
        """
        dict_config must have the keys:
            suite_name : Name of suite
            module_path : Path to the module containing all plugins
            plugins : List of all the plugin names
            plugins : List[Dict]
                - Each dict has:
                    - name : Name of the plugin
                    - dependencies : names of plugins this is dependant on.
                    - module name : Name of module this plugin is in.
        """
        # Add path to the imports
        abs_path = dict_config["path"]
        sys.path.append(abs_path)
        pkg_name = dict_config["suiteName"]

        dependency_map = dict()
        plugins = dict()
        """ TODO: test this  -- path dependency / relative path & absolute path"""
        for plugin, conf in dict_config["plugins"].items():
            module_name = conf["moduleName"]
            module_path = f"{pkg_name}.{module_name}"
            rel_path = conf["path"]
            path = f"{abs_path}/{rel_path}"
            clazz_name = conf["className"]

            spec = importlib.util.spec_from_file_location(
                module_path, path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_path] = module
            spec.loader.exec_module(module)
            clazz = getattr(module, clazz_name)
            instance = clazz()

            dependency_map[clazz_name] = conf["dependencies"]
            plugins[clazz_name] = instance

        return dependency_map, plugins # used to generate pipeline 


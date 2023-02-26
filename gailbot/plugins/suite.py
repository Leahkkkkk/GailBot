# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 13:22:39
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 13:10:57

import sys
import os
from typing import Dict, List, Any, TypedDict
from dataclasses import dataclass
import time
import importlib
import imp
from gailbot.core.utils.logger import makelogger
from .plugin import Plugin, Methods
from gailbot.configs import top_level_config_loader

from gailbot.core.pipeline import (
    Pipeline, 
    Component, 
    ComponentResult, 
    ComponentState)

PLUGIN_CONFIG = top_level_config_loader().plugin

logger = makelogger("pluginSuite")

class PluginResult(ComponentResult):
    """
    Class containing the result of a component object.
    """
    state: ComponentState = ComponentState.FAILED
    result: Any = None
    runtime: float  = 0

class PluginComponent(Component):
    """
    This is an adapter because the Plugin expects different args as compared
    to pipeline components.
    This is needed to so that ComponentResult component is not passed to the user.
    """
    def __init__(self,
        plugin : Plugin
    ):
        """ 
        Giving a plugin, wrap it to a component class , so that it 
        it can be executed by the pipeline 
        """
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
        try:
            result = self.plugin.apply(dep_outputs, methods)
        except Exception as e:
            result = f"Error: {e}"
            logger.error(e)
            
        elapsed = time.time() - start
        return PluginResult(
            state=ComponentState.SUCCESS if self.plugin.is_successful else \
                ComponentState.FAILED,
            result=result,
            runtime=elapsed
        )


class PluginSuite:
    """
    Manages a suite of plugins and responsible for loading, queries, and
    execution.
    Needs to store the details of each plugin (source file etc.)
    """

    def __init__(
        self,
        dict_conf : Dict,
        abs_path: str
    ):

        """ a dictionary of the dependency map  -> pipeline argument  """
        self.dict_conf = dict_conf
        self.dependency_map, self.plugins = self._load_from_config(dict_conf, abs_path)
        
        # Wrap the plugins in PluginComponent
        self.components = {
            k : PluginComponent(v) for k,v in self.plugins.items()
        }

        # Init the pipeline based on the components
        self.pipeline = Pipeline(dependency_map = self.dependency_map,
                                 components = self.components,
                                 num_threads=PLUGIN_CONFIG.num_threads)
        
        # Add vars here from conf.
        self._name = dict_conf["suite_name"]
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
            additional_component_kwargs= {
                "methods" : methods
            }
        )

        return result

    def is_plugin(self, plugin_name : str) -> bool:
        """ given a name , return true if the plugin is in the plugin suite """
        return plugin_name in self.plugins

    def plugin_names(self) -> List[str]:
        """Get names of all plugins"""
        return list(self.plugins.keys())

    def plugin_details(self, plugin_name : str) -> Dict:
        # TODO: Potentially store additional things beyond plugin dependencies
        if self.is_plugin(plugin_name):
            return {"dependencies" : self.dependency_map[plugin_name]}

    def dependency_graph(self) -> Dict:
        """Return the entire dependency graph as a dictionary"""
        return self.pipeline.get_dependency_graph()


    ##########
    # PRIVATE
    ##########

    def _load_from_config(self, dict_config, abs_path: str ) -> None:
        """
        load the plugin suite, the information about the each plugin name, 
        and its path is stored in the dict_config, all path information 
        is relative to the abs_path
        
        Args: 
        dict_config must have the keys:
            suite_name : Name of suite
            plugins : List[Dict]
                - Each dict has:
                    - plugin_name : Name of the plugin
                    - dependencies : names of plugins this is dependant on.
                    - module_name : Name of module this plugin is in.
                    - rel_path: the relative path of the plugin script, 
                                the path is relative to the suite path
                                
        abs_path: the absolute path where the plugin suite directory is relative
                  to, each plugins's absolute path can be form as 
                  "<abs_path>/<suite_name>/<rel_path>"
        """
        pkg_name = dict_config["suite_name"]
        dependency_map = dict()
        plugins = dict()
        
        logger.info(dict_config)
        logger.info(f"absolute path: {abs_path}")
        
        for conf in dict_config["plugins"]:
            module_name = conf["module_name"]
            module_full_name = f"{pkg_name}.{module_name}"
            rel_path = conf["rel_path"]
            path = os.path.join(abs_path, pkg_name, rel_path)
            clazz_name = conf["plugin_name"]
            spec = importlib.util.spec_from_file_location(
                module_full_name, path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_full_name] = module
            spec.loader.exec_module(module)
            clazz = getattr(module, clazz_name)
            instance = clazz()

            dependency_map[clazz_name] = conf["dependencies"]
            plugins[clazz_name] = instance
            
        return dependency_map, plugins # used to generate pipeline


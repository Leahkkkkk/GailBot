# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 13:22:39
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 13:10:57

import sys
import os
from typing import Dict, List, Any, Tuple
import time
from pydantic import BaseModel

from .plugin import Plugin, Methods
from gailbot.core.utils.logger import makelogger
from gailbot.configs import PLUGIN_CONFIG
from gailbot.core.pipeline import Pipeline, Component, ComponentResult, ComponentState
from gailbot.core.utils.general import is_file

import importlib


logger = makelogger("pluginSuite")


class PluginResult(ComponentResult):
    """
    Class containing the result of a component object.
    """

    state: ComponentState = ComponentState.FAILED
    result: Any = None
    runtime: float = 0


class MetaData(BaseModel):
    """
    schema for base meta-data
    """

    Author: str
    Email: str
    Version: str


class PluginComponent(Component):
    """
    This is an adapter because the Plugin expects different args as compared
    to pipeline components.
    This is needed to so that ComponentResult component is not passed to the user.
    """

    def __init__(self, plugin: Plugin):
        """
        Giving a plugin, wrap it to a component class , so that it
        it can be executed by the pipeline
        """
        logger.info(plugin)
        self.plugin = plugin

    def __repr__(self):
        return str(self.plugin)

    def __call__(
        self,
        dependency_outputs: Dict[str, ComponentResult] = {},
        methods: Methods = None,
    ):
        """
        In addition to dependency outputs, this expects methods which can be
        passed to the individual plugins.
        """
        # Extract the actual dependency results
        logger.info("plugin component called")
        dep_outputs = {k: v.result for k, v in dependency_outputs.items()}
        logger.info("get the dependency output")
        # Simply call the plugin and return its results
        start = time.time()
        try:
            result = self.plugin.apply(dep_outputs, methods)
        except Exception as e:
            result = f"Error: {e}"
            logger.error(e, exc_info=e)

        elapsed = time.time() - start

        return PluginResult(
            state=ComponentState.SUCCESS
            if self.plugin.is_successful
            else ComponentState.FAILED,
            result=result,
            runtime=elapsed,
        )


class PluginSuite:
    """
    Manages a suite of plugins and responsible for loading, queries, and
    execution.
    Needs to store the details of each plugin (source file etc.)
    """

    def __init__(self, dict_conf: Dict, abs_path: str):
        """a dictionary of the dependency map  -> pipeline argument"""
        self.dict_conf = dict_conf
        self.source_path = abs_path
        # metadata and document_path will be loaded in _load_from_config
        self.metadata: MetaData = None
        self.document_path: str = None
        self.formatmd_path: str = None
        self.dependency_map, self.plugins = self._load_from_config(dict_conf, abs_path)

        # Wrap the plugins in PluginComponent
        self.components = {k: PluginComponent(v) for k, v in self.plugins.items()}

        # Init the pipeline based on the components
        self.pipeline = Pipeline(
            dependency_map=self.dependency_map,
            components=self.components,
            num_threads=PLUGIN_CONFIG.THREAD_NUM,
        )
        # Add vars here from conf.
        self._name = dict_conf["suite_name"]
        self._is_ready = True
        self.is_official = False

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_ready(self):
        return self._is_ready

    def set_to_official_suite(self):
        """set the plugin to official plugin"""
        self.is_official = True

    def __repr__(self):
        return (
            f"Plugin Suite: {self.name}\n" f"Dependency map: {self.dependency_graph()}"
        )

    def __str__(self) -> str:
        return (
            f"Plugin Suite: {self.name}\n" f"Dependency map: {self.dependency_graph()}"
        )

    def __call__(self, base_input: Any, methods: Methods) -> Dict:
        """
        Apply the specified plugins when possible and return the results
        summary
        """
        logger.info(methods)
        logger.info(base_input)

        pipeline = Pipeline(
            dependency_map=self.dependency_map,
            components=self.components,
            num_threads=1,
        )

        result = pipeline(
            base_input=base_input, additional_component_kwargs={"methods": methods}
        )
        return result

    def is_plugin(self, plugin_name: str) -> bool:
        """given a name , return true if the plugin is in the plugin suite"""
        return plugin_name in self.plugins

    def plugin_names(self) -> List[str]:
        """Get names of all plugins"""
        return list(self.plugins.keys())

    def plugin_details(self, plugin_name: str) -> Dict:
        if self.is_plugin(plugin_name):
            return {"dependencies": self.dependency_map[plugin_name]}

    def dependency_graph(self) -> Dict:
        """Return the entire dependency graph as a dictionary"""
        return self.pipeline.get_dependency_graph()

    def get_meta_data(self) -> MetaData:
        """get the metadata about this plugin"""
        return self.metadata

    ##########
    # PRIVATE
    ##########
    def _load_from_config(
        self, dict_config, abs_path: str
    ) -> Tuple[Dict[str, List[str]], Dict[str, Plugin]]:
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
        suite_name = dict_config["suite_name"]
        dependency_map: Dict[str, List] = dict()
        plugins: Dict[str, Plugin] = dict()
        logger.info(dict_config)
        logger.info(f"absolute path: {abs_path}")

        metadata = dict_config["metadata"]
        MetaData(**metadata)
        self.metadata = metadata
        self.document_path = os.path.join(abs_path, suite_name, PLUGIN_CONFIG.DOCUMENT)
        self.formatmd_path = os.path.join(abs_path,suite_name, PLUGIN_CONFIG.FORMAT )
        assert is_file(self.document_path)
        
        for conf in dict_config["plugins"]:
            module_name = conf["module_name"]
            module_full_name = f"{suite_name}.{module_name}"
            rel_path = conf["rel_path"]
            path = os.path.join(abs_path, suite_name, rel_path)
            clazz_name = conf["plugin_name"]
            spec = importlib.util.spec_from_file_location(module_full_name, path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_full_name] = module
            spec.loader.exec_module(module)
            clazz = getattr(module, clazz_name)
            instance = clazz()
            dependency_map[clazz_name] = conf["dependencies"]
            plugins[clazz_name] = instance
        logger.info(f"plugin dependency map {dependency_map}")
        logger.info(f"pluins {plugins}")
        return dependency_map, plugins  # used to generate pipeline

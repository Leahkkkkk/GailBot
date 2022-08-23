# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:13:08
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-05-03 12:22:41
# Standard library imports
from typing import Dict, Any, List, Tuple
# Local imports
from .apply_config import ApplyConfig
from .manager_summary import PluginManagerSummary
from .plugin_details import PluginDetails
from .config import PluginConfig
from .plugin_source import PluginSource
from .loader import PluginLoader
from .logic import PluginPipelineLogic
from .plugin_execution_summary import PluginExecutionSummary
from ..pipeline import Pipeline, Stream
from ..io import IO


class PluginManager:

    def __init__(self) -> None:
        # Objects
        self.loader = PluginLoader()
        self.io = IO()
        # Vars.
        self.config_file_extension = "json"
        self.pipeline_name = "plugin_pipeline"
        self.pipeline_num_threads = 3

    ############################ MODIFIERS ##################################

    def register_plugins_from_directory(self, dir_path: str,
                                        check_subdirectories: bool = True) -> int:
        """
        Register a plugin from the specified directory.
        All configuration files from the directory are used to initialize all
        plugins.

        Args:
            dir_path (str): Path to the directory.
            check_subdirectories (bool):
                If True, checks all subdirectories for configuration files.

        Returns:
            (int): Number of plugins loaded from directory.
        """
        if not self.io.is_directory(dir_path):
            return 0
        # Load all possible config files
        _, paths = self.io.path_of_files_in_directory(
            dir_path, [self.config_file_extension], check_subdirectories)
        return sum([self.register_plugin_using_config_file(path) for path in paths])

    def register_plugin_using_config_file(self, config_file_path: str) -> bool:
        """
        Register a plugin from a configuration file directly.

        Args:
            config_file_path (str): Path to the configuration file.

        Returns:
            (bool): True if successfully loaded. False otherwise.
        """
        # Generate config object and load
        _, data = self.io.read(config_file_path)
        return self.register_plugin_using_config_data(data)

    def register_plugin_using_config_data(self, data: Dict[str, Any]) -> bool:
        """
        Register a plugin using a dictionary representation of PluginConfig.

        Args:
            data (Dict[str,Any]):
                Mapping from all keys in PluginConfig to their values.

        Returns:
            (bool): True if successfully configured. False otherwise.
        """
        try:
            success, config = self._generate_config(data)
            if not success:
                return False
            return self.loader.load_plugin_using_config(config)
        except Exception as e:
            print(e)

    def apply_plugins(self, apply_configs: Dict[str, ApplyConfig]) \
            -> PluginManagerSummary:
        """
        Apply all plugins defined by the given plugin configs.
        The plugins must be previously registered.

        Args:
            apply_configs (Dict[str,ApplyConfig]):
                Mapping from plugin name to ApplyConfig.

        Returns:
            (PluginManagerSummary): Summary for executing all plugins.
        """
        did_generate, pipeline = self._generate_execution_pipeline(
            apply_configs)
        if not did_generate:
            return self._generate_summary({}, apply_configs)
        pipeline.set_base_input(apply_configs)
        pipeline.execute()
        return self._generate_summary(
            pipeline.get_execution_summary(), apply_configs)

    ############################# GETTERS ###################################

    def is_plugin(self, plugin_name: str) -> bool:
        """
        Determine if the plugin is available.

        Args:
            plugin_name (str)

        Returns:
            (bool): True if the plugin is available. False otherwise.
        """
        return self.loader.is_plugin_loaded(plugin_name)

    def get_plugin_names(self) -> List[str]:
        """
        Get the names of all available plugins.

        Returns:
            (List[str])
        """
        return self.loader.get_loaded_plugin_names()

    def get_plugin_details(self, plugin_name: str) -> PluginDetails:
        """
        Get PluginDetails for the specified plugin if it is available.

        Args:
            plugin_name (str): Name of plugin.

        Returns:
            (PluginDetails)
        """
        if not self.is_plugin(plugin_name):
            return
        source: PluginSource = self.loader.get_plugin(plugin_name)
        return PluginDetails(
            source.plugin_name, source.plugin_dependencies,
            source.number_of_dependencies, source.plugin_file_path,
            source.plugin_author, source.plugin_input_type,
            source.plugin_output_type)

    def get_all_plugin_details(self) -> Dict[str, PluginDetails]:
        """
        Get mapping from plugin name to PluginDetails for all available plugins.

        Returns:
            (Dict[str,PluginDetails])
        """
        details = dict()
        plugin_names = self.loader.get_loaded_plugin_names()
        for plugin_name in plugin_names:
            details[plugin_name] = self.get_plugin_details(plugin_name)
        return details

    ########################### PRIVATE METHODS #############################

    def _generate_config(self, data: Dict[str, Any]) \
            -> Tuple[bool, PluginConfig]:
        try:
            config = PluginConfig(
                data["plugin_name"], data["plugin_dependencies"],
                data["plugin_file_path"],
                data["plugin_source_name"], data["plugin_class_name"])
            return (True, config)
        except Exception as e:
            print(e)
            return (False, None)

    def _generate_execution_pipeline(
            self, apply_configs: Dict[str, ApplyConfig]) -> Tuple[bool, Pipeline]:
        """
        Generate a pipeline given a mapping from plugin name to ApplyConfig.
        All plugins must be loaded.
        """
        pipeline = Pipeline(self.pipeline_name, self.pipeline_num_threads)
        pipeline.set_logic(PluginPipelineLogic())
        for plugin_name in apply_configs.keys():
            if not self._add_plugin_with_dependencies(
                    pipeline, plugin_name, apply_configs):
                return (False, None)
        return (True, pipeline)

    def _add_plugin_with_dependencies(
            self, pipeline: Pipeline,
            plugin_name: str, apply_configs: Dict[str, ApplyConfig]) -> bool:
        """
        Add a plugin and its required dependencies to the given pipeline using
        the given ApplyConfig's.
        All the plugins must be loaded.
        """
        # Plugin must be loaded.
        if not self.loader.is_plugin_loaded(plugin_name) or \
                not plugin_name in apply_configs:
            return False
        # Do not re-load component
        if plugin_name in pipeline.get_component_names():
            return True
        # Load the dependencies
        plugin_source: PluginSource = self.loader.get_plugin(plugin_name)
        for dependency in plugin_source.plugin_dependencies:
            if not self._add_plugin_with_dependencies(
                    pipeline, dependency, apply_configs):
                return False
        # Add actual plugin
        return pipeline.add_component(
            plugin_name, plugin_source, plugin_source.plugin_dependencies)

    def _generate_summary(self, execution_summary: Dict[str, Any],
                          apply_configs: Dict[str, ApplyConfig]) \
            -> PluginManagerSummary:
        """
        Generate the summary for executing all plugins in the pipeline.

        Args:
            execution_summary (Dict[str,Any]):
                Summary obtained by executing a Pipeline
        """
        try:
            # Initializing the plugin summaries.
            total_time_seconds = 0
            successful_plugins = list()
            failed_plugins = list()
            plugin_summaries = dict()
            # Summary only generated for plugins that were selected.
            plugin_names = list(apply_configs.keys())
            for plugin_name in plugin_names:
                # Means plugin was executed and we can get summary.
                if plugin_name in execution_summary.keys() and \
                        execution_summary[plugin_name]["state"] == "successful":
                    summary = execution_summary[plugin_name]
                    stream: Stream = summary["result"]
                    # TODO: This keeps causing issues.
                    if stream != None:
                        plugin_summary: PluginExecutionSummary = \
                            stream.get_stream_data()
                        plugin_summaries[plugin_name] = plugin_summary
                        total_time_seconds += plugin_summary.runtime_seconds
                        if plugin_summary.was_successful:
                            successful_plugins.append(
                                plugin_summary.plugin_name)
                        else:
                            failed_plugins.append(plugin_summary.plugin_name)
                # Plugin was not executed.
                else:
                    plugin_summaries[plugin_name] = PluginExecutionSummary(
                        plugin_name, [], {}, None, 0, False)
                    failed_plugins.append(plugin_name)
            return PluginManagerSummary(
                total_time_seconds, successful_plugins, failed_plugins,
                plugin_summaries)
        except Exception as e:
            print(e)

# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:13:08
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-07 17:10:55
# Standard library imports
from typing import Callable, Dict, Any
from time import time
# Local imports
from ..pipeline import Stream, Logic
from .plugin import Plugin
from .plugin_source import PluginSource
from .apply_config import ApplyConfig
from .plugin_execution_summary import PluginExecutionSummary


class PluginPipelineLogic(Logic):

    def __init__(self) -> None:
        super().__init__()
        # Adding all logic methods

    def get_preprocessor(self, component_name: str) \
            -> Callable[[Dict[str, Stream]], Any]:
        """
        Override the super class method to make sure same method is returned
        for any component.
        """
        return self._preprocessor_plugin

    def get_processor(self, component_name: str) \
            -> Callable[[object, Any], Any]:
        """
        Override the super class method to make sure same method is returned
        for any component.
        """
        return self._processor_plugin

    def get_postprocessor(self, component_name: str) -> Callable[[Any], Stream]:
        """
        Override the super class method to make sure same method is returned
        for any component.
        """
        return self._post_processor_plugin

    def is_component_supported(self, component_name: str) -> bool:
        """
        In this pipeline, any component may be supported.
        """
        return True

    ########################### PRIVATE METHODS #############################

    def _preprocessor_plugin(self, streams: Dict[str, Stream]) \
            -> Dict[str, ApplyConfig]:
        """
        Extract apply configs from the base input.
        """
        return streams

    def _processor_plugin(self, plugin_source:  PluginSource,
                          streams: Dict[str, Stream]) \
            -> PluginExecutionSummary:
        """
        Applies the plugin specified by the plugin source using the given
        ApplyConfig.
        Returns PluginExecutionSummary for the specified plugin.
        """
        # Extract the apply configs from base input.
        apply_configs = streams["base"].get_stream_data()
        parent_plugin_outputs = self._get_parent_plugin_outputs(
            plugin_source, streams)
        apply_config = apply_configs[plugin_source.plugin_name]
        plugin: Plugin = plugin_source.plugin_object
        # Get the plugin dependency outputs
        start_time = time()
        output = plugin.apply_plugin(parent_plugin_outputs,
                                     *apply_config.args, **apply_config.kwargs)
        successful = plugin.was_successful()
        if not successful:
            raise Exception()
        total_time = time() - start_time

        summary = PluginExecutionSummary(
            plugin_source.plugin_name, apply_config.args,
            apply_config.kwargs, output, total_time, successful)
        # Generating the plugin summary.
        return summary

    def _post_processor_plugin(self, summary: PluginExecutionSummary) -> Stream:
        """
        Package the PluginExecutionSummary as a Stream.
        """
        return Stream(summary)

    def _get_parent_plugin_outputs(self, plugin_source: PluginSource,
                                   streams: Dict[str, Stream]) -> Dict[str, Any]:
        """
        Obtain a mapping from the plugins dependencies to their results.
        """
        dependency_outputs = dict()
        dependencies = plugin_source.plugin_dependencies
        for dependency in dependencies:
            if dependency in streams:
                summary: PluginExecutionSummary = \
                    streams[dependency].get_stream_data()
                dependency_outputs[dependency] = summary.output
        return dependency_outputs

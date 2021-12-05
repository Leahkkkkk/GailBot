# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:48:19
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-05 14:19:04
from typing import Dict, Any, List
from abc import abstractmethod
from copy import deepcopy
# Local imports
from .payload import Payload
from ..plugin_manager import Plugin, PluginConfig, PluginManager, ApplyConfig, \
    PluginManagerSummary
from ..shared_models import Utt


class PluginMethodSuite:

    def __init__(self, payload: Payload) -> None:
        self.payload = payload

    def get_utterances(self):
        return self.payload.source_addons.utterances_map

    def get_result_directory_path(self):
        return self.payload.source.hook.get_temp_directory_path()


class GBPlugin(Plugin):
    @abstractmethod
    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_method_suite: PluginMethodSuite) -> Any:
        """
        This method is called to apply the plugin on a single source.

        Args:
            dependency_outputs (Dict[str,Any]):
                Map from any plugins this one is dependant on to their outputs.
            plugin_input (AnalysisPluginInput):
                Object that provides utility methods for this source.

        Returns:
            (Any): This is stored as the output for this plugin.
        """
        pass

    @abstractmethod
    def was_successful(self) -> bool:
        """
        Determine if the plugin executed successfully.

        Returns:
            (bool): True if the plugin was successful. False otherwise.
        """
        pass


class PluginsStage:

    def __init__(self) -> None:
        self.plugin_manager = PluginManager()

    ############################# MODIFIERS ##################################

    def register_plugins(self, plugins_data_list: List[Dict[str, Any]]) \
            -> List[str]:
        current_plugins = self.plugin_manager.get_plugin_names()
        for data in plugins_data_list:
            self.plugin_manager.register_plugin_using_config_data(data)
        return [plugin_name for plugin_name in self.plugin_manager.get_plugin_names()
                if plugin_name not in current_plugins]

    def apply_plugins(self, payload: Payload) -> None:
        if not self._can_apply_plugins(payload):
            return
        # Generate apply configs
        apply_configs = self._generate_plugin_configs(payload)
        # Apply plugins
        manager_summary: PluginManagerSummary = \
            self.plugin_manager.apply_plugins(apply_configs)

        ######################## PRIVATE METHODS ################################

    def _can_apply_plugins(self, payload: Payload) -> bool:
        plugins_to_apply = [
            "turn_construct",
            "overlaps",
            "pauses",
            "combine_turns",
            "fto",
            "gaps",
            "chat"]
        return all([self.plugin_manager.is_plugin(plugin_name)
                    for plugin_name in plugins_to_apply])

    def _generate_plugin_configs(self, payload):
        plugin_names = [
            "turn_construct",
            "overlaps",
            "pauses",
            "combine_turns",
            "fto",
            "gaps",
            "chat"]
        apply_configs = dict()
        for plugin_name in plugin_names:
            plugin_input = PluginMethodSuite(payload)
            apply_configs[plugin_name] = ApplyConfig(
                plugin_name, [plugin_input], {})
        return apply_configs

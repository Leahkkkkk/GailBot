# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:48:19
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-07 17:27:10
from typing import Dict, Any, List
from abc import abstractmethod
from copy import deepcopy

# Local imports
from .payload import Payload
from ..plugin_manager import Plugin, PluginConfig, PluginManager, ApplyConfig, \
    PluginManagerSummary
from ..shared_models import Utt, GailBotSettings


class PluginMethodSuite:

    def __init__(self, payload: Payload) -> None:
        self.payload = payload

    def get_utterances(self) -> Dict:
        return self.payload.source_addons.utterances_map

    def get_result_directory_path(self) -> str:
        return self.payload.source.hook.get_temp_directory_path()

    def get_audio_paths(self) -> Dict:
        audio_map = dict()
        for data_file in self.payload.source.conversation.data_files:
            audio_map[data_file.identifier] = data_file.audio_path
        return audio_map


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
        # Add log statements
        payload.source_addons.logger.info("Successful plugins {}".format(
            manager_summary.successful_plugins))
        if len(manager_summary.failed_plugins) > 0:
            payload.source_addons.logger.warning("Failed plugins {}".format(
                manager_summary.failed_plugins))
        payload.source_addons.logger.info("Runtime {} seconds".format(
            manager_summary.total_runtime_seconds))

        ######################## PRIVATE METHODS ################################

    def _can_apply_plugins(self, payload: Payload) -> bool:
        settings: GailBotSettings = payload.source.settings_profile.settings
        plugins_to_apply = settings.plugins.plugins_to_apply
        return all([self.plugin_manager.is_plugin(plugin_name)
                    for plugin_name in plugins_to_apply])

    def _generate_plugin_configs(self, payload):
        settings: GailBotSettings = payload.source.settings_profile.settings
        plugin_names = settings.plugins.plugins_to_apply
        apply_configs = dict()
        for plugin_name in plugin_names:
            plugin_input = PluginMethodSuite(payload)
            apply_configs[plugin_name] = ApplyConfig(
                plugin_name, [plugin_input], {})
        return apply_configs

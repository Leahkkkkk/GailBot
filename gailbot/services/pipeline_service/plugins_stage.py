# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:48:19
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-23 11:48:33
from typing import Dict, Any, List
from abc import abstractmethod

# Local imports
from .payload import Payload
from gailbot.core.io import GailBotIO
from gailbot.plugin.plugin_manager import (
    Plugin,
    PluginManager,
    ApplyConfig,
    PluginManagerSummary
)
from gailbot.services.objects import Utt, GailBotSettings


class PluginMethodSuite:
    """
    Method suite provided to Plugins containing methods on a per-source level.
    """

    def __init__(self, payload: Payload) -> None:
        self.io = GailBotIO()
        self.payload = payload
        self.result_dir = "{}/{}".format(
            self.payload.source.hook.get_temp_directory_path(),
            "plugins_results")
        if not self.io.is_directory(self.result_dir):
            self.io.create_directory(self.result_dir)

    def get_utterances(self) -> Dict[str, Utt]:
        """
        Obtain the utterances map generated for this source.

        Returns:
            (Dict[str,Utt]):
                Map from each data file to utterances generated for that file.
        """
        return self.payload.source_addons.utterances_map

    def get_result_directory_path(self) -> str:
        """
        Obtain the result directory path for this source.
        """
        return self.result_dir

    def get_audio_paths(self) -> Dict[str, str]:
        """
        Obtain a map from each data file in the source to its corresponding
        audio file.

        Returns:
            (Dict[str,str])
        """
        audio_map = dict()
        for data_file in self.payload.source.conversation.data_files:
            audio_map[data_file.identifier] = data_file.audio_path
        return audio_map


class GBPlugin(Plugin):

    def __init__(self):
        self.successful = False

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

    def was_successful(self) -> bool:
        """
        Determine if the plugin executed successfully.

        Returns:
            (bool): True if the plugin was successful. False otherwise.
        """
        return self.successful


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

    def get_registered_plugin_names(self) -> List[str]:
        return self.plugin_manager.get_plugin_names()

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

from typing import Dict, Any, List
from abc import abstractmethod
# Local imports
from ....plugin_manager import Plugin
from ..models import Payload, Utt, ProcessStatus
from ....plugin_manager import PluginManager, PluginManagerSummary, ApplyConfig
from ...helpers.gb_settings import GBSettingAttrs, GailBotSettings
from ...blackboards import PipelineBlackBoard


class PluginMethodSuite:

    def __init__(self, payload: Payload) -> None:
        self.payload = payload

    def get_utterances(self) -> Dict[str, Utt]:
        return self.payload.source.conversation.get_utterances()


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

    def __init__(self, blackboard: PipelineBlackBoard) -> None:
        self.blackboard = blackboard
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
            print("Cannot apply plugins")
            payload.status = ProcessStatus.FAILED
            return
        # Generate apply configs
        apply_configs = self._generate_plugin_configs(payload)
        # Apply plugins
        manager_summary: PluginManagerSummary = \
            self.plugin_manager.apply_plugins(apply_configs)
        # Determine if all plugins were successful
        # if all([plugin_name in manager_summary.successful_plugins
        #         for plugin_name in apply_configs.keys()]):
        payload.status = ProcessStatus.PLUGINS_APPLIED

        ######################## PRIVATE METHODS ################################

    def _can_apply_plugins(self, payload: Payload) -> bool:
        settings: GailBotSettings = payload.source.conversation.get_settings()
        plugins_to_apply = settings.get_value(
            GBSettingAttrs.plugins_to_apply)
        print(self.plugin_manager.get_plugin_names())
        print(plugins_to_apply)
        print(payload)
        return all([self.plugin_manager.is_plugin(plugin_name)
                    for plugin_name in plugins_to_apply]) and \
            payload.status == ProcessStatus.TRANSCRIBED

    def _generate_plugin_configs(self, payload) -> List[ApplyConfig]:
        settings: GailBotSettings = payload.source.conversation.get_settings()
        plugin_names = settings.get_value(
            GBSettingAttrs.plugins_to_apply)
        apply_configs = dict()
        for plugin_name in plugin_names:
            plugin_input = PluginMethodSuite(payload)
            apply_configs[plugin_name] = ApplyConfig(
                plugin_name, [plugin_input], {})
        return apply_configs

# Standard imports
from typing import Dict, Any, List
# Local imports
from .....plugin_manager import PluginManager, PluginManagerSummary, ApplyConfig
from ...organizer_service import GailBotSettings, RequestType
from ..pipeline_payload import SourcePayload
from .analysis_plugin_input import AnalysisPluginInput


class AnalysisStage:

    def __init__(self) -> None:
        self.plugin_manager = PluginManager()

    ############################# MODIFIERS ##################################

    def register_plugin_from_data(self, data: Dict[str, Any]) -> bool:
        """
        Register a single plugin from a data dictionary.

        Args:
            data (Dict[str,Any])

        Returns:
            (bool):
                True if the plugin is successfully registered, False otherwise.
        """
        return self.plugin_manager.register_plugin_using_config_data(data)

    def register_plugins_from_data(self, data_list: List[Dict[str, Any]]) \
            -> List[str]:
        """
        Register plugins using a list of configuration data dictionaries.

        Args:
            data_list (List[Dict[str,Any]]):
                List of data dictionaries.

        Returns:
            (List[str]): Names of plugins that were registered from the list.
        """
        current_plugins = self.get_plugin_names()
        for data in data_list:
            self.register_plugin_from_data(data)
        return [plugin_name for plugin_name in self.get_plugin_names()
                if plugin_name not in current_plugins]

    def analyze(self, payload: SourcePayload) -> bool:
        """
        Apply analysis plugins, as defined using the settings profile, to the
        payload.

        Args:
            payload (SourcePayload)

        Returns:
            (bool): True if all selected plugins are successfully executed,
                    False otherwise.
        """
        # Verify is analysis possible.
        if not self._can_analyze(payload):
            msg = "Cannot analyze"
            self._log_to_payload(payload, msg)
            self._log_error_to_payload(payload, msg)
            payload.set_analysis_status(False)
            return
        # Generate ApplyConfig for all plugins
        settings: GailBotSettings = payload.get_conversation().get_settings()
        apply_configs = dict()
        for plugin_name in settings.get_analysis_plugins_to_apply():
            plugin_input = AnalysisPluginInput(payload)
            apply_configs[plugin_name] = ApplyConfig(
                plugin_name, [plugin_input], {})
        # Apply all plugins.
        manager_summary: PluginManagerSummary = \
            self.plugin_manager.apply_plugins(apply_configs)
        payload.set_analysis_plugin_summaries(
            manager_summary.plugin_summaries)
        # Determine if the plugins were successfully run.
        if all([plugin_name in manager_summary.successful_plugins
                for plugin_name in apply_configs.keys()]):
            payload.set_analysis_status(True)
            msg = "[successfully applied plugins: {}".format(
                list(apply_configs.keys()))
        else:
            for plugin_name in manager_summary.failed_plugins:
                msg = "Analysis plugin failed: {}".format(plugin_name)
                self._log_error_to_payload(payload, msg)
            msg = "Analysis failed".format(payload.get_source_name())
        self._log_to_payload(payload, msg)

    ########################## GETTERS #######################################

    def is_plugin(self, plugin_name: str) -> bool:
        """
        Determine if the plugin exists.

        Args:
            plugin_name (str)

        Returns:
            (bool): True if the plugins are applied successfully, False otherwise.
        """
        return self.plugin_manager.is_plugin(plugin_name)

    def get_plugin_names(self) -> List[str]:
        """
        Obtain the names of the plugins.

        Returns:
            (List[str]): Names of plugins.
        """
        return self.plugin_manager.get_plugin_names()

    ######################## PRIVATE METHODS ################################

    def _can_analyze(self, payload: SourcePayload) -> bool:
        settings: GailBotSettings = payload.get_conversation().get_settings()
        plugins_to_apply = settings.get_analysis_plugins_to_apply()
        # All the plugins must be registered.
        return all([self.is_plugin(plugin_name)
                    for plugin_name in plugins_to_apply]) and \
            payload.is_transcribed()

    def _log_to_payload(self, payload: SourcePayload, msg: str) -> None:
        msg = "[Analysis Stage] [{}] {}".format(
            payload.get_source_name(), msg)
        payload.log(msg)

    def _log_error_to_payload(self, payload: SourcePayload, msg: str) -> None:
        msg = "[Analysis Stage] [{}] {}".format(
            payload.get_source_name(), msg)
        payload.log_error(msg)

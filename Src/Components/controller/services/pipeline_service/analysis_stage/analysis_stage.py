# Standard imports
from Src.Components.controller.services.organizer_service.source.source import Source
from typing import Dict, Any, List
# Local imports
from ......utils.threads import ThreadPool
from ......utils.manager import ObjectManager
from .....plugin_manager import PluginManager, PluginManagerSummary, ApplyConfig
from ...organizer_service import GailBotSettings, RequestType
from ..pipeline_payload import SourcePayload
from .analysis_plugin_input import AnalysisPluginInput


class AnalysisStage:


    def __init__(self) -> None:
        self.plugin_manager = PluginManager()

    ############################# MODIFIERS ##################################

    def register_plugin_from_data(self, data : Dict[str,Any]) -> bool:
        return self.plugin_manager.register_plugin_using_config_data(data)

    def register_plugins_from_data(self, data_list : List[Dict[str,Any]]) \
            -> List[str]:
        current_plugins = self.get_plugin_names()
        for data in data_list:
            self.register_plugin_from_data(data)
        return [plugin_name for plugin_name in self.get_plugin_names() \
            if plugin_name not in current_plugins]

    def analyze(self, payload : SourcePayload) -> bool:
        # Verify is analysis possible.
        if not self._can_analyze(payload):
            msg = "[{}] [Analysis stagee] Cannot analyze".format(
                payload.get_source_name())
            payload.log(RequestType.FILE, msg)
            payload.set_analysis_status(False)
            return
        # Generate ApplyConfig for all plugins
        settings : GailBotSettings = payload.get_conversation().get_settings()
        apply_configs = dict()
        for plugin_name in settings.get_analysis_plugins_to_apply():
            plugin_input = AnalysisPluginInput(
                payload.get_conversation().get_conversation_name(),
                payload.get_conversation().get_utterances(),
                payload.get_source_to_audio_map(),
                payload.get_conversation().get_source_file_paths(),
                payload.get_conversation().get_temp_directory_path(),
                payload.get_conversation().get_result_directory_path())
            apply_configs[plugin_name] = ApplyConfig(
                    plugin_name, [plugin_input],{})
        # Apply all plugins.
        manager_summary : PluginManagerSummary = \
            self.plugin_manager.apply_plugins(apply_configs)
        payload.set_analysis_plugin_summaries(
            manager_summary.plugin_summaries)
        # Determine if the plugins were successfully run.
        if all([plugin_name in manager_summary.successful_plugins \
                for plugin_name in apply_configs.keys()]):
            payload.set_analysis_status(True)
            msg = "[{}] [Analysis stage] successfully applied plugins: {}".format(
                payload.get_source_name(),list(apply_configs.keys()))
        else:
            msg = "[{}] [Analysis stage] Analysis failed".format(
                payload.get_source_name())
        payload.log(RequestType.FILE,msg)

    ########################## GETTERS #######################################

    def is_plugin(self, plugin_name : str) -> bool:
        return self.plugin_manager.is_plugin(plugin_name)

    def get_plugin_names(self) -> List[str]:
        return self.plugin_manager.get_plugin_names()

    ######################## PRIVATE METHODS ################################

    def _can_analyze(self, payload : SourcePayload) -> bool:
        settings : GailBotSettings = payload.get_conversation().get_settings()
        plugins_to_apply = settings.get_analysis_plugins_to_apply()
        # All the plugins must be registered.
        return all([self.is_plugin(plugin_name) \
                for plugin_name in plugins_to_apply]) and \
            payload.is_transcribed()

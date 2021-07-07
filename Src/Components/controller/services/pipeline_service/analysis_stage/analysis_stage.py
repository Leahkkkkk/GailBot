# Standard imports
from typing import Dict, Any, List
# Local imports
from ......utils.threads import ThreadPool
from ......utils.manager import ObjectManager
from .....plugin_manager import PluginManager, PluginManagerSummary, ApplyConfig
from ...gb_settings import GailBotSettings
from ..pipeline_payload import SourcePayload
from .analysis_plugin_input import AnalysisPluginInput

class AnalysisStage:

    def __init__(self, num_threads : int) -> None:

        ## Objects
        self.payloads = ObjectManager()
        self.plugin_manager = PluginManager()
        self.max_threads = 4
        if num_threads <= 0 or num_threads > self.max_threads:
            raise Exception("Invalid number of threads")
        self.thread_pool = ThreadPool(num_threads)
        self.thread_pool.spawn_threads()

    ############################# MODIFIERS ##################################

    def add_payload(self, payload_name : str,  payload : SourcePayload) -> bool:
        # Source is not added if the transcription stage is not passed.
        if not payload.transcription_successful:
            return False
        return self.payloads.add_object(payload_name, payload)

    def add_payloads(self, payloads : Dict[str,SourcePayload]) -> bool:
        return all([self.add_payload(payload_name, payload)] \
            for payload_name, payload in payloads.items())

    def remove_payload(self, payload_name : str) -> bool:
        return self.payloads.remove_object(payload_name)

    def clear_payloads(self) -> None:
        self.payloads.clear_objects()

    def register_plugin_from_data(self, data : Dict[str,Any]) -> bool:
        return self.plugin_manager.register_plugin_using_config_data(data)

    def register_plugins_from_data(self, data_list : List[Dict[str,Any]]) \
            -> List[str]:
        current_plugins = self.get_plugin_names()
        for data in data_list:
            self.register_plugin_from_data(data)
        return [plugin_name for plugin_name in self.get_plugin_names() \
            if plugin_name not in current_plugins]

    def analyze(self) -> None:
        payloads = self.payloads.get_all_objects()
        for _, payload in payloads.items():
            payload : SourcePayload
            settings : GailBotSettings = payload.conversation.get_settings()
            plugins_to_apply = settings.get_analysis_plugins_to_apply()
            apply_configs = dict()
            # All the plugins must be registered.
            if not all([self.is_plugin(plugin_name) \
                    for plugin_name in plugins_to_apply]):
                continue
            for plugin_name in plugins_to_apply:
                if self.plugin_manager.is_plugin(plugin_name):
                    # TODO: Determine exact plugin input
                    plugin_input = AnalysisPluginInput(
                        payload.conversation.get_conversation_name(),
                        payload.conversation.get_utterances(),
                        payload.source_to_audio_map,
                        payload.conversation.get_source_file_paths(),
                        payload.conversation.get_temp_directory_path(),
                        payload.conversation.get_result_directory_path())
                    apply_configs[plugin_name] = ApplyConfig(
                        plugin_name, [plugin_input],{})
            # One thread per conversation.
            self.thread_pool.add_task(
                self._execute_plugins_thread,[apply_configs, payload],{})
        # Waiting for all conversations to finish.
        self.thread_pool.wait_completion()

    ########################## GETTERS #########################################

    def get_payloads(self) -> Dict[str,SourcePayload]:
        return self.payloads.get_all_objects()

    def get_payload(self, payload_name : str) -> SourcePayload:
        return self.payloads.get_object(payload_name)

    def is_plugin(self, plugin_name : str) -> bool:
        return self.plugin_manager.is_plugin(plugin_name)

    def get_plugin_names(self) -> List[str]:
        return self.plugin_manager.get_plugin_names()

    ######################## PRIVATE METHODS ################################

    def _execute_plugins_thread(self,apply_configs : Dict[str,ApplyConfig],
            payload : SourcePayload) -> None:
        manager_summary : PluginManagerSummary = \
            self.plugin_manager.apply_plugins(apply_configs)
        # Set the summaries
        payload.analysis_plugin_summaries = manager_summary.plugin_summaries
        # Determine if the plugins were successfully run.
        if all([plugin_name in manager_summary.successful_plugins \
                for plugin_name in apply_configs.keys()]):
            payload.analysis_successful = True

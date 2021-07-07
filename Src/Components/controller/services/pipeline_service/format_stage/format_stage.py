# Standard imports
from typing import List, Dict, Any
# Local imports
from ......utils.threads import ThreadPool
from ......utils.manager import ObjectManager
from .....plugin_manager import PluginManager, PluginManagerSummary, ApplyConfig
from ...gb_settings import GailBotSettings
from ..pipeline_payload import SourcePayload
from .format_plugin_input import FormatPluginInput

class FormatStage:

    def __init__(self, num_threads : int) -> None:
        ## Objects
        self.payloads = ObjectManager()
        self.format_manager = ObjectManager()
        self.max_threads = 4
        if num_threads <= 0 or num_threads > self.max_threads:
            raise Exception("Invalid number of threads")
        self.thread_pool = ThreadPool(num_threads)
        self.thread_pool.spawn_threads()

    ############################### MODIFIERS ################################

    def add_payload(self, payload_name : str,  payload : SourcePayload) -> bool:
        # Source is not added if the transcription stage is not passed.
        if not payload.transcription_successful or \
                not payload.analysis_successful:
            return False
        return self.payloads.add_object(payload_name, payload)

    def add_payloads(self, payloads : Dict[str,SourcePayload]) -> bool:
        return all([self.add_payload(payload_name, payload)] \
            for payload_name, payload in payloads.items())

    def remove_payload(self, payload_name : str) -> bool:
        return self.payloads.remove_object(payload_name)

    def clear_payloads(self) -> None:
        self.payloads.clear_objects()

    def register_format(self, format_name : str,
            configs : List[Dict[str,Any]]) -> List[str]:
        plugin_manager = PluginManager()
        for config in configs:
            # All the plugins must be registered.
            if not all([plugin_manager.register_plugin_using_config_data(config)]):
                return []
        self.format_manager.add_object(format_name,plugin_manager)
        return plugin_manager.get_plugin_names()

    def apply_format(self) -> None:
        payloads = self.payloads.get_all_objects()
        for _, payload in payloads.items():
            payload : SourcePayload
            # Get the output format
            settings : GailBotSettings = payload.conversation.get_settings()
            output_format = settings.get_output_format()
            # Skip if the output format is not supported.
            if not self.is_format(output_format):
                continue
            # Apply the format plugins.
            plugin_manager : PluginManager = self.format_manager.get_object(
                output_format)
            apply_configs = dict()
            for plugin_name in plugin_manager.get_plugin_names():
                # TODO: Generate the correct input
                plugin_input = FormatPluginInput(
                    payload.conversation.get_conversation_name(),
                    payload.conversation.get_utterances(),
                    self._get_analysis_plugin_outputs(payload),
                    payload.conversation.get_temp_directory_path(),
                    payload.conversation.get_result_directory_path())
                apply_configs[plugin_name] = ApplyConfig(
                    plugin_name,[plugin_input],{})
            # One thread per conversation
            self.thread_pool.add_task(
                self._execute_plugins_thread,
                [apply_configs,plugin_manager,payload],{})
        self.thread_pool.wait_completion()

    ########################## GETTERS #########################################

    def get_payloads(self) -> Dict[str,SourcePayload]:
        return self.payloads.get_all_objects()

    def get_payload(self, payload_name : str) -> SourcePayload:
        return self.payloads.get_object(payload_name)

    def is_format(self, format_name : str) -> bool:
        return self.format_manager.is_object(format_name)

    def get_formats(self) -> List[str]:
        return self.format_manager.get_object_names()

    def is_format_plugin(self, format_name : str, plugin_name : str) -> bool:
        if not self.is_format(format_name):
            return False
        plugin_manager : PluginManager = \
            self.format_manager.get_object(format_name)
        return plugin_manager.is_plugin(plugin_name)

    def get_format_plugins(self, format_name : str) -> List[str]:
        if not self.is_format(format_name):
            return []
        plugin_manager : PluginManager = \
            self.format_manager.get_object(format_name)
        return plugin_manager.get_plugin_names()

    ######################## PRIVATE METHODS ##################################

    def _execute_plugins_thread(self,apply_configs : Dict[str,ApplyConfig],
            plugin_manager : PluginManager, payload: SourcePayload) -> None:
        manager_summary : PluginManagerSummary = \
            plugin_manager.apply_plugins(apply_configs)
        # Set plugin summaries
        payload.format_plugin_summaries = manager_summary.plugin_summaries
        # Check if all plugins successful
        if all([plugin_name in manager_summary.successful_plugins \
                for plugin_name in apply_configs.keys()]):
            payload.format_successful = True

    def _get_analysis_plugin_outputs(self, payload : SourcePayload) -> Dict[str,Any]:
        analysis_plugin_outputs = dict()
        for plugin_name, plugin_summary in \
                payload.analysis_plugin_summaries.items():
            analysis_plugin_outputs[plugin_name] = plugin_summary.output
        return analysis_plugin_outputs
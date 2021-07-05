# Standard imports
from typing import Dict, Any, List
# Local imports
from ......utils.threads import ThreadPool
from ......utils.manager import ObjectManager
from .....plugin_manager import PluginManager, PluginManagerSummary, ApplyConfig
from ...organizer_service import GailBotSettings
from ..source import Source
from .analysis_plugin_input import AnalysisPluginInput

class AnalysisStage:

    def __init__(self, num_threads : int) -> None:
        ## Objects
        self.sources = ObjectManager()
        self.plugin_manager = PluginManager()
        self.max_threads = 4
        if num_threads <= 0 or num_threads > self.max_threads:
            raise Exception("Invalid number of threads")
        self.thread_pool = ThreadPool(num_threads)
        self.thread_pool.spawn_threads()

    ############################# MODIFIERS ##################################

    def add_source(self, source_name : str, source : Source) -> bool:
        # Source is not added if the transcription stage is not passed.
        if not source.transcription_successful:
            return False
        return self.sources.add_object(source_name, source)

    def add_sources(self, sources : Dict[str,Source]) -> bool:
        return all([self.add_source(source_name, source) \
            for source_name, source in sources.items()])

    def remove_source(self, source_name : str) -> bool:
        return self.sources.remove_object(source_name)

    def clear_sources(self) -> None:
        self.sources.clear_objects()

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
        sources = self.sources.get_all_objects()
        for _, source in sources.items():
            source : Source
            # Get the names of plugins to apply
            settings : GailBotSettings = source.conversation.get_settings()
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
                        source.conversation.get_utterances(),
                        source.source_to_audio_map,
                        source.conversation.get_source_file_paths())
                    apply_configs[plugin_name] = ApplyConfig(
                        plugin_name, [plugin_input],{})
            # One thread per conversation.
            self.thread_pool.add_task(
                self._execute_plugins_thread,[apply_configs, source],{})
        # Waiting for all conversations to finish.
        self.thread_pool.wait_completion()

    ########################## GETTERS #########################################

    def get_sources(self) -> Dict[str,Source]:
        return self.sources.get_all_objects()

    def get_source(self, source_name : str) -> Source:
        return self.sources.get_object(source_name)

    def is_plugin(self, plugin_name : str) -> bool:
        return self.plugin_manager.is_plugin(plugin_name)

    def get_plugin_names(self) -> List[str]:
        return self.plugin_manager.get_plugin_names()

    ######################## PRIVATE METHODS ################################

    def _execute_plugins_thread(self,apply_configs : Dict[str,ApplyConfig],
            source : Source) -> None:
        manager_summary : PluginManagerSummary = \
            self.plugin_manager.apply_plugins(apply_configs)
        # Set the summaries
        source.analysis_plugin_summaries = manager_summary.plugin_summaries
        # Determine if the plugins were successfully run.
        if all([plugin_name in manager_summary.successful_plugins \
                for plugin_name in apply_configs.keys()]):
            source.analysis_successful = True

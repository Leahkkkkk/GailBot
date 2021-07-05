# Standard imports
from Src.Components.plugin_manager.plugin import Plugin
from typing import List, Dict, Any
# Local imports
from ......utils.threads import ThreadPool
from ......utils.manager import ObjectManager
from .....plugin_manager import PluginManager, PluginManagerSummary, ApplyConfig
from ...organizer_service import GailBotSettings
from ..source import Source
from .format_plugin_input import FormatPluginInput

class FormatStage:

    def __init__(self, num_threads : int) -> None:
        ## Objects
        self.sources = ObjectManager()
        self.format_manager = ObjectManager()
        self.max_threads = 4
        if num_threads <= 0 or num_threads > self.max_threads:
            raise Exception("Invalid number of threads")
        self.thread_pool = ThreadPool(num_threads)
        self.thread_pool.spawn_threads()

    ############################### MODIFIERS ################################

    def add_source(self, source_name : str, source : Source) -> bool:
        # Source only added if analysis stage passed.
        if not source.transcription_successful or \
                not source.analysis_successful:
            return False
        return self.sources.add_object(source_name, source)

    def add_sources(self, sources : Dict[str,Source]) -> bool:
        return all([self.add_source(source_name, source) \
            for source_name, source in sources.items()])

    def remove_source(self, source_name : str) -> bool:
        return self.sources.remove_object(source_name)

    def clear_sources(self) -> None:
        self.sources.clear_objects()

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
        sources = self.sources.get_all_objects()
        for _, source in sources.items():
            source : Source
            # Get the output format
            settings : GailBotSettings = source.conversation.get_settings()
            output_format = settings.get_output_format()
            # Skip if the output format is not supported.
            if not self.is_format(output_format):
                continue
            # Apply the format plugins.
            plugin_manager : PluginManager = self.format_manager.get_object(output_format)
            apply_configs = dict()
            for plugin_name in plugin_manager.get_plugin_names():
                # TODO: Generate the correct input
                plugin_input = FormatPluginInput(
                    source.conversation.get_utterances(),
                    self._get_analysis_plugin_outputs(source))
                apply_configs[plugin_name] = ApplyConfig(
                    plugin_name,[plugin_input],{})
            # One thread per conversation
            self.thread_pool.add_task(
                self._execute_plugins_thread,
                [apply_configs,plugin_manager,source],{})
        self.thread_pool.wait_completion()

    ############################### GETTERS ################################

    def get_sources(self) -> Dict[str,Source]:
        return self.sources.get_all_objects()

    def get_source(self, source_name : str) -> Source:
        return self.sources.get_object(source_name)

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

    ######################## PRIVATE METHODS ################################

    def _execute_plugins_thread(self,apply_configs : Dict[str,ApplyConfig],
            plugin_manager : PluginManager, source : Source) -> None:
        manager_summary : PluginManagerSummary = \
            plugin_manager.apply_plugins(apply_configs)
        # Set plugin summaries
        source.format_plugin_summaries = manager_summary.plugin_summaries
        # Check if all plugins successful
        if all([plugin_name in manager_summary.successful_plugins \
                for plugin_name in apply_configs.keys()]):
            source.format_successful = True

    def _get_analysis_plugin_outputs(self, source : Source) -> Dict[str,Any]:
        analysis_plugin_outputs = dict()
        for plugin_name, plugin_summary in source.analysis_plugin_summaries.items():
            analysis_plugin_outputs[plugin_name] = plugin_summary.output
        return analysis_plugin_outputs


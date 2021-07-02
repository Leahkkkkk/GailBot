
# Standard library imports
from typing import Any, List, Dict
# Local imports
from .....plugin_manager import PluginManager, PluginManagerSummary, ApplyConfig,\
                            PluginExecutionSummary
from .....organizer import Conversation
from ......utils.threads import ThreadPool
from ......utils.manager import ObjectManager
from ......utils.threads import ThreadPool
from ..analysis_stage import AnalysisStageResult
from .result import FormatStageResult
from .input import FormatPluginInput


class FormatStage:
    """
    Manages multiple loaded, supported formats.
    """

    def __init__(self) -> None:
        self.format_manager = ObjectManager()
        self.thread_pool = ThreadPool(4) # TODO: Remove hard-code.
        self.thread_pool.spawn_threads()

    ############################### MODIFIERS ################################

    def register_format(self, format_name : str,
            configs : List[Dict[str,Any]]) -> List[str]:
        plugin_manager = PluginManager()
        for config in configs:
            plugin_manager.register_plugin_using_config_data(config)
        self.format_manager.add_object(format_name, plugin_manager)
        return plugin_manager.get_plugin_names()

    def format_conversations(self, format_name : str,
            conversations : Dict[str,Conversation],
            analysis_stage_output : AnalysisStageResult) -> FormatStageResult:
        if not self.is_format(format_name):
            return FormatStageResult({})
        # TODO: Use the analysis_stage_output.
        # Format  each conversation
        plugin_manager = self.format_manager.get_object(format_name)
        summaries = dict()
        plugin_names = plugin_manager.get_plugin_names()
        for conversation_name, conversation in conversations.items():
            apply_configs = dict()
            for plugin_name in plugin_names:
                # TODO: Add args.
                plugin_input = FormatPluginInput(
                    self._get_analysis_stage_outputs(
                        conversation_name, analysis_stage_output))
                apply_configs[plugin_name] = ApplyConfig(
                    plugin_name, [plugin_input], {})
            self.thread_pool.add_task(
                self._format_thread, [conversation_name, plugin_manager,
                    apply_configs,summaries], {})
        self.thread_pool.wait_completion()
        # TODO: Add args to object
        return FormatStageResult(summaries)

    ############################### GETTERS ################################

    def is_format(self, format_name : str) -> bool:
        return self.format_manager.is_object(format_name)

    def get_formats(self) -> List[str]:
        return self.format_manager.get_object_names()

    def is_format_plugin(self, format_name : str, plugin_name : str) -> bool:
        if not self.is_format(format_name):
            return False
        plugin_manager : PluginManager = self.format_manager.get_object(
            format_name)
        return plugin_manager.is_plugin(plugin_name)

    def get_format_plugins(self, format_name : str) -> List[str]:
        if not self.is_format(format_name):
            return []
        plugin_manager : PluginManager = self.format_manager.get_object(
            format_name)
        return plugin_manager.get_plugin_names()

    ######################## PRIVATE METHODS ################################

    def _format_thread(self, conversation_name, plugin_manager : PluginManager,
            apply_configs : Dict[str,ApplyConfig],
            summaries : Dict[str,PluginManagerSummary]) -> None:
        summaries[conversation_name] = \
            plugin_manager.apply_plugins(apply_configs)

    def _get_analysis_stage_outputs(self, conversation_name : str,
            analysis_stage_result : AnalysisStageResult) -> Dict[str,Any]:
        results = dict()
        plugin_summaries = analysis_stage_result.analysis_summaries
        converstion_analysis_plugins_summary = plugin_summaries[conversation_name]
        for plugin_name, summary in converstion_analysis_plugins_summary.items():
            summary : PluginExecutionSummary
            results[plugin_name] = summary.output
        return results








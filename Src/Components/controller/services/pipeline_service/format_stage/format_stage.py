
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
        """
        Register a format with the specified name and list of PluginConfig
        dictionaries.

        Args:
            format_name (str): Name of the format.
            configs ( List[Dict[str,Any]]):
                List of dictionaries continaing data for PLuginConfig.

        Returns:
            (List[str]): Names of plugins that have been loaded in.
        """
        plugin_manager = PluginManager()
        for config in configs:
            plugin_manager.register_plugin_using_config_data(config)
        self.format_manager.add_object(format_name, plugin_manager)
        return plugin_manager.get_plugin_names()

    def format_conversations(self, format_name : str,
            conversations : Dict[str,Conversation],
            analysis_stage_output : AnalysisStageResult) -> FormatStageResult:
        """
        Format conversations using the specified format.

        Args:
            format_name (str): Name of format. Must have been loaded in.
            conversations (Dict[str,Conversation])
            analysis_Stage_output (AnalysisStageResult)

        Returns:
            (FormatStageResult)
        """
        summaries = dict()
        # Check if format exists
        if not self.is_format(format_name):
            for conversation_name in conversations.keys():
                summaries[conversation_name] = None
            return FormatStageResult(summaries)
        # Format  each conversation
        plugin_manager = self.format_manager.get_object(format_name)
        plugin_names = plugin_manager.get_plugin_names()
        for conversation_name, conversation in conversations.items():
            apply_configs = dict()
            for plugin_name in plugin_names:
                # Generating the input for the format plugins.
                plugin_input = self._generate_format_plugin_input(
                    conversation_name,conversation,analysis_stage_output)
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
        """
        Determine if the format exists.

        Args:
            format_name (str)

        Returns:
            (bool): True if the format exists. False otherwise.
        """
        return self.format_manager.is_object(format_name)

    def get_formats(self) -> List[str]:
        """
        Obtain a list of all the formats present.

        Returns:
            List[str]: Names of all registered formats.
        """
        return self.format_manager.get_object_names()

    def is_format_plugin(self, format_name : str, plugin_name : str) -> bool:
        """
        Determine if the format has the specified plugin.

        Args:
            format_name (str)
            plugin_name (str)

        Returns:
            (bool): True if the format has the plugin, False otherwise.
        """
        if not self.is_format(format_name):
            return False
        plugin_manager : PluginManager = self.format_manager.get_object(
            format_name)
        return plugin_manager.is_plugin(plugin_name)

    def get_format_plugins(self, format_name : str) -> List[str]:
        """
        Obtain the names of all the plugins in the specified format.

        Args:
            format_name (str)

        Returns:
            (List[str]): Names of all plugins for the format.
        """
        if not self.is_format(format_name):
            return []
        plugin_manager : PluginManager = self.format_manager.get_object(
            format_name)
        return plugin_manager.get_plugin_names()

    ######################## PRIVATE METHODS ################################

    def _format_thread(self, conversation_name, plugin_manager : PluginManager,
            apply_configs : Dict[str,ApplyConfig],
            summaries : Dict[str,PluginManagerSummary]) -> None:
        """
        Apply the format plugins.
        """
        summaries[conversation_name] = \
            plugin_manager.apply_plugins(apply_configs)

    def _generate_format_plugin_input(self, conversation_name : str,
            conversation : Conversation,
            analysis_stage_output : AnalysisStageResult) -> FormatPluginInput:
        """
        Generate input to the format plugin for the specified conversation.
        """
        utterances_map = conversation.get_utterances()
        analysis_plugin_outputs = dict()
        plugin_manager_summary =\
            analysis_stage_output.analysis_summaries[conversation_name]
        for plugin_name, plugin_summary in \
                plugin_manager_summary.plugin_summaries.items():
            analysis_plugin_outputs[plugin_name] = plugin_summary.output
        return FormatPluginInput(
            utterances_map,analysis_plugin_outputs)

    # TODO: Write methods to save conversations to file.
    def _save_conversations(self, conversations : Dict[str,Conversation]) -> None:
        pass

    def _save_conversation(self, conversation : Conversation) -> None:
        pass

# Standard library imports
from typing import Any, List, Dict
# Local imports
from .....plugin_manager import PluginManager, PluginManagerSummary, ApplyConfig
from .....organizer import Conversation
from ......utils.threads import ThreadPool
from ..transcription_stage import TranscriptionStageResult
from .input import AnalysisPluginInput
from .result import AnalysisStageResult

class AnalysisStage:
    """
    Stage in which transcription results can be analyzed to detect
    additional features using AnalysisPlugins
    """

    def __init__(self) -> None:
        ## Objects
        self.plugin_manager = PluginManager()
        self.thread_pool = ThreadPool(4) # TODO: Remove hard-code.
        self.thread_pool.spawn_threads()

    ########################## MODIFIERS ######################################

    def register_plugin_from_data(self, data : Dict[str,Any]) -> bool:
        """
        Register a plugin using a dictionary representation of PluginConfig.

        Args:
            data (Dict[str,Any]):
                Mapping from all keys in PluginConfig to their values.

        Returns:
            (bool): True if successfully configured. False otherwise.
        """
        return self.plugin_manager.register_plugin_using_config_data(data)

    def analyze(self, conversations : Dict[str,Conversation],
            transcription_stage_output : TranscriptionStageResult) \
                -> AnalysisStageResult:
        """
        Run each conversation therough the plugin pipeline.

        Args:
            conversations (Dict[str,Conversation]):
                Mapping from conversation name to the Conversation.
            transcription_stage_output (TranscriptionStageOutput):
                Output from the transcription stage.

        Returns:
            (AnalysisStageResult)
        """
        ## Unpack the transcription stage output
        # TODO: This might change.
        conversations_audio_sources = \
            transcription_stage_output.conversations_audio_sources
        conversations_status_maps = \
            transcription_stage_output.conversations_status_maps
        # Analyze each conversation
        summaries = dict()
        plugin_names = self.plugin_manager.get_plugin_names()
        for conversation_name, conversation in conversations.items():
            apply_configs = dict()
            for plugin_name in plugin_names:
                # Generating the input to the analaysis plugin.
                plugin_input = AnalysisPluginInput(
                    conversation.get_utterances(),
                    conversations_audio_sources[conversation_name],
                    conversation.get_source_file_paths())
                # Generating the apply_config for all plugins.
                apply_configs[plugin_name] = ApplyConfig(
                    plugin_name, [plugin_input],{})
            # One thread per conversation.
            self.thread_pool.add_task(
                self._analyze_thread, [conversation_name, apply_configs,
                    summaries],{})
        self.thread_pool.wait_completion()
        # Generating result.
        return AnalysisStageResult(summaries)

    ########################## GETTERS #########################################

    def is_plugin(self, plugin_name : str) -> bool:
        """
        Determine if the plugin exists.

        Args:
            plugin_name (str): Name of the plugin.

        Returns:
            (bool): True if the plugin exists. False otherwise.
        """
        return self.plugin_manager.is_plugin(plugin_name)

    def get_plugin_names(self) -> List[str]:
        """
        Obtain the names of all registered plugins.

        Returns:
            (List[str]): Name of all plugins.
        """
        return self.plugin_manager.get_plugin_names()

    ######################## PRIVATE METHODS ################################

    def _analyze_thread(self, conversation_name,
            apply_configs : Dict[str,ApplyConfig],
            summaries : Dict[str,PluginManagerSummary]) -> None:
        """
        Thread that applied plugins to a single conversation and stores the
        PluginExecutionSummary for that conversation.
        """
        summaries[conversation_name] = \
            self.plugin_manager.apply_plugins(apply_configs)

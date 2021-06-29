# Standard library imports
from typing import Any, List, Dict
# Local imports
from ....analyzer import Analyzer, AnalysisSummary, ApplyConfig
from ....organizer import Conversation
from .....utils.threads import ThreadPool
from .transcription_stage_results import TranscriptionStageResult
from .analysis_plugin_input import AnalysisPluginInput
from .analysis_stage_result import AnalysisStageResult

class AnalysisStage:

    def __init__(self) -> None:
        ## Objects
        self.analyzer = Analyzer()
        self.thread_pool = ThreadPool(4) # TODO: Remove hard-code.
        self.thread_pool.spawn_threads()

    def register_plugins_from_directory(self, dir_path : str) -> int:
        return self.analyzer.register_plugins_from_directory(dir_path)

    def analyze(self, conversations : Dict[str, Conversation],
            transcription_stage_output : TranscriptionStageResult) \
                -> AnalysisStageResult:
        ## Unpack the transcription stage output
        # TODO: This might change.
        conversations_audio_sources = \
            transcription_stage_output.conversations_audio_sources
        conversations_status_maps = \
            transcription_stage_output.conversations_status_maps
        # Analyze each conversation
        summaries = dict()
        plugin_names = self.analyzer.get_plugin_names()
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

    ######################## PRIVATE METHODS ################################

    def _analyze_thread(self, conversation_name,
            apply_configs : Dict[str,ApplyConfig],
            summaries : Dict[str,AnalysisSummary]) -> None:
        summaries[conversation_name] = \
            self.analyzer.apply_plugins(apply_configs)



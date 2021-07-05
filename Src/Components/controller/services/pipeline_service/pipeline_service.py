# Standard imports
from Src.Components.plugin_manager import plugin
from Src.Components.plugin_manager.plugin_execution_summary import PluginExecutionSummary
from typing import List, Tuple, Dict, Any
# Local imports
from .....utils.manager import ObjectManager
from ....pipeline import Pipeline
from ....organizer import Conversation
from ..fs_service import FileSystemService
from .service_summary import PipelineServiceSummary
from .transcription_stage.transcription_stage import TranscriptionStage
from .analysis_stage.analysis_stage import AnalysisStage
from .format_stage.format_stage import FormatStage
from .loader import PipelineServiceLoader
from .logic import PipelineServiceLogic
from .source import Source

class PipelineService:

    def __init__(self, num_threads : int) -> None:
        ## Vars.
        self.pipeline_name = "transcription_pipeline_service"
        self.max_threads = 4
        if num_threads <= 0 or num_threads > self.max_threads:
            raise Exception("Invalid number of threads")
        self.pipeline_num_threads = num_threads
        ## Stage Objects
        self.transcription_stage = TranscriptionStage(self.pipeline_num_threads)
        self.analysis_stage = AnalysisStage(self.pipeline_num_threads)
        self.format_stage = FormatStage(self.pipeline_num_threads)
        ## Others
        self.sources = ObjectManager()
        self.logic = PipelineServiceLogic()
        self.loader = PipelineServiceLoader()
        ## Initializing the pipeline
        self.pipeline = Pipeline(self.pipeline_name,self.pipeline_num_threads)
        self.pipeline.set_logic(self.logic)
        self.pipeline.add_component(
            "transcription_stage", self.transcription_stage)
        self.pipeline.add_component(
            "analysis_stage",self.analysis_stage,["transcription_stage"])
        self.pipeline.add_component(
            "format_stage",self.format_stage,["analysis_stage"])

    ################################# MODIFIERS #############################

    def add_source(self, source_name : str ,conversation : Conversation) -> bool:
        source = Source(source_name, conversation)
        return self.sources.add_object(source_name, source)

    def register_analysis_plugins(self, config_path : str) -> List[str]:
        success, data_list = \
            self.loader.parse_analysis_plugin_configuration_file(config_path)
        return self.analysis_stage.register_plugins_from_data(data_list)

    def register_format(self, config_path : str) -> Tuple[str,List[str]]:
        success, data = self.loader.parse_format_configuration_file(config_path)
        if not success:
            return (None,None)
        return self.format_stage.register_format(*data)

    def start(self) -> PipelineServiceSummary:
        self.pipeline.set_base_input(self.sources.get_all_objects())
        self.pipeline.execute()
        # TODO: Generate this summary.
        return self._generate_summary()

    ################################# GETTERS ###############################

    def get_analysis_plugin_names(self) -> List[str]:
        return self.analysis_stage.get_plugin_names()

    def get_format_names(self) -> List[str]:
        return self.format_stage.get_formats()

    def get_format_plugin_names(self, format_name  : str) -> List[str]:
        return self.format_stage.get_format_plugins(format_name)

    def is_source(self, source_name : str) -> bool:
        return self.sources.is_object(source_name)

    def get_conversation(self, source_name : str) -> Conversation:
        if self.is_source(source_name):
            return self.sources.get_object(source_name)

    def get_conversations(self) -> Dict[str,Conversation]:
        conversations = dict()
        sources = self.sources.get_all_objects()
        for source_name, source in sources:
            source : Source
            conversations[source_name] = source.conversation
        return conversations

    ########################## PRIVATE METHODS ###############################

    def _generate_summary(self) -> PipelineServiceSummary:
        summary = PipelineServiceSummary()
        sources = self.sources.get_all_objects()
        for source_name, source in sources.items():
            source : Source
            summary.source_names.append(source_name)
            if source.transcription_successful:
                summary.sources_transcribed.append(source_name)
            if source.analysis_successful:
                summary.sources_analyzed.append(source_name)
            if source.format_successful:
                summary.sources_formatted.append(source_name)

            for plugin_name, plugin_summary in \
                    source.analysis_plugin_summaries.items():
                summary.sources_analysis_plugin_summaries[plugin_name] = \
                    self._plugin_summary_as_dictionary(plugin_summary)
            for plugin_name, plugin_summary in \
                    source.format_plugin_summaries.items():
                summary.sources_format_plugin_summaries[plugin_name] = \
                    self._plugin_summary_as_dictionary(plugin_summary)
        return summary

    def _plugin_summary_as_dictionary(self,
            plugin_summary : PluginExecutionSummary) -> Dict[str,Any]:
        return {
            "plugin_name" : plugin_summary.plugin_name,
            "runtime" : plugin_summary.runtime_seconds,
            "was_successful" : plugin_summary.was_successful}






# Standard imports
from typing import List, Tuple, Dict, Any
# Local imports
from .....utils.manager import ObjectManager
from ....pipeline import Pipeline
from ....organizer import Conversation
from ....plugin_manager import PluginExecutionSummary
from ..fs_service import FileSystemService
from ..source import Source
from .service_summary import PipelineServiceSummary
from .transcription_stage.transcription_stage import TranscriptionStage
from .analysis_stage.analysis_stage import AnalysisStage
from .format_stage.format_stage import FormatStage
from .output_stage.output_stage import OutputStage
from .loader import PipelineServiceLoader
from .logic import PipelineServiceLogic
from .pipeline_payload import SourcePayload


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
        self.output_stage = OutputStage()
        ## Others
        self.sources = ObjectManager()
        self.payloads = ObjectManager()
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

    def add_source(self, source_name : str, source : Source) -> bool:
        payload = SourcePayload(source)
        return self.sources.add_object(source_name, source) and \
            self.payloads.add_object(source_name, payload)

    def add_sources(self, sources : Dict[str,Source]) -> bool:
        return all([self.add_source(name, source) \
            for name, source in sources.items()])

    def remove_source(self, source_name : str) -> bool:
        return self.sources.remove_object(source_name) and \
            self.payloads.remove_object(source_name)

    def register_analysis_plugins(self, config_path : str) -> List[str]:
        success, data_list = \
            self.loader.parse_analysis_plugin_configuration_file(config_path)
        if not success:
            return []
        return self.analysis_stage.register_plugins_from_data(data_list)

    def register_format(self, config_path : str) -> Tuple[str,List[str]]:
        success, data = self.loader.parse_format_configuration_file(config_path)
        if not success:
            return (None,None)
        return (data[0],self.format_stage.register_format(*data))

    def start(self) -> PipelineServiceSummary:
        self.pipeline.set_base_input(self.payloads.get_all_objects())
        self.pipeline.execute()
        # Run the output stage.
        self._execute_output_stage(self.payloads.get_all_objects())
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

    def get_source(self, source_name : str) -> Source:
       return self.sources.get_object(source_name)

    def get_sources(self) -> Dict[str,Source]:
        return self.sources.get_all_objects()

    ########################## PRIVATE METHODS ###############################

    def _generate_summary(self) -> PipelineServiceSummary:
        summary = PipelineServiceSummary()
        payloads = self.payloads.get_all_objects()
        for source_name, payload in payloads.items():
            payload : SourcePayload
            summary.source_names.append(source_name)
            if payload.transcription_successful:
                summary.sources_transcribed.append(source_name)
            if payload.analysis_successful:
                summary.sources_analyzed.append(source_name)
            if payload.format_successful:
                summary.sources_formatted.append(source_name)
            for plugin_name, plugin_summary in \
                    payload.analysis_plugin_summaries.items():
                summary.sources_analysis_plugin_summaries[plugin_name] = \
                    self._plugin_summary_as_dictionary(plugin_summary)
            for plugin_name, plugin_summary in \
                    payload.format_plugin_summaries.items():
                summary.sources_format_plugin_summaries[plugin_name] = \
                    self._plugin_summary_as_dictionary(plugin_summary)
        return summary

    def _plugin_summary_as_dictionary(self,
            plugin_summary : PluginExecutionSummary) -> Dict[str,Any]:
        return {
            "plugin_name" : plugin_summary.plugin_name,
            "runtime" : plugin_summary.runtime_seconds,
            "was_successful" : plugin_summary.was_successful}

    def _execute_output_stage(self, payloads : Dict[str,SourcePayload]) -> bool:
        return self.output_stage.output_payloads(payloads)







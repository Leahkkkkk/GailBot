# Standard imports
from typing import List, Tuple, Dict, Any
# Local imports
from .....utils.manager import ObjectManager
from ....pipeline import Pipeline
from ....plugin_manager import PluginExecutionSummary
from ..organizer_service import Source, RequestType
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
        self.transcription_stage = TranscriptionStage()
        self.analysis_stage = AnalysisStage()
        self.format_stage = FormatStage()
        self.output_stage = OutputStage()
        ## Others
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
        self.pipeline.add_component(
            "output_stage", self.output_stage, ["format_stage"])

    ################################# MODIFIERS #############################

    def add_source(self, source_name : str, source : Source) -> bool:
        payload = SourcePayload(source)
        if self.payloads.add_object(source_name, payload):
            msg = "[{}]  Added to pipeline service".format(source_name)
            payload.log(RequestType.FILE, msg)
            return True
        return False

    def add_sources(self, sources : Dict[str,Source]) -> bool:
        return all([self.add_source(name, source) \
            for name, source in sources.items()])

    def remove_source(self, source_name : str) -> bool:
        if self.payloads.is_object(source_name):
            payload : SourcePayload = self.payloads.get_object(source_name)
            msg = "[{}] Removed from pipeline service".format(source_name)
            payload.log(RequestType.FILE,msg)
            return self.payloads.remove_object(source_name)
        return False

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
        return self._generate_service_summary()

    ################################# GETTERS ###############################

    def get_analysis_plugin_names(self) -> List[str]:
        return self.analysis_stage.get_plugin_names()

    def get_format_names(self) -> List[str]:
        return self.format_stage.get_formats()

    def get_format_plugin_names(self, format_name  : str) -> List[str]:
        return self.format_stage.get_format_plugins(format_name)

    def is_source(self, source_name : str) -> bool:
        return self.payloads.is_object(source_name)

    def get_source(self, source_name : str) -> Source:
       if self.is_source(source_name):
           payload : SourcePayload = self.payloads.get_object(source_name)
           return payload.get_source()

    def get_sources(self) -> Dict[str,Source]:
        sources = dict()
        for source_name in self.payloads.get_object_names():
            sources[source_name] = self.get_source(source_name)
        return sources

    ########################## PRIVATE METHODS ###############################

    def _generate_service_summary(self) -> PipelineServiceSummary:
        payload_summaries = dict()
        for name , payload in self.payloads.get_all_objects().items():
            payload : SourcePayload
            payload_summaries[name] = payload.generate_summary()
        # Get all the successful payloads
        return PipelineServiceSummary(
            self.payloads.get_object_names(),
            list(self.payloads.get_filtered_objects(
                lambda name , payload : payload.is_transcribed()).keys()),
            list(self.payloads.get_filtered_objects(
                lambda name , payload : payload.is_analyzed()).keys()),
            list(self.payloads.get_filtered_objects(
                lambda name , payload : payload.is_formatted()).keys()),
            payload_summaries)


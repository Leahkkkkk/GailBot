# Standard library imports
from typing import List, Dict, Tuple
# Local imports
from ....pipeline import Pipeline
from ....organizer import Conversation
from .summary import PipelineServiceSummary
from .transcription_stage import TranscriptionStage
from .analysis_stage import AnalysisStage
from .format_stage import FormatStage
from .payload import PipelineServicePayload
from .logic import PipelineServiceLogic
from .loader import PipelineServiceLoader

class PipelineService:

    def __init__(self) -> None:
        ## Vars.
        self.pipeline_name = "transcription_pipeline_service"
        self.pipeline_num_threads = 4
        ## Stage Objects
        self.transcription_stage = TranscriptionStage()
        self.analysis_stage = AnalysisStage()
        self.format_stage = FormatStage()
        ## Others
        self.payload = PipelineServicePayload()
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

    def register_analysis_plugins(self, config_path : str) -> List[str]:
        names = self.analysis_stage.get_plugin_names()
        parsed_data = self.loader.parse_analysis_plugin_configuration_file(
            config_path)
        for data in parsed_data:
            self.analysis_stage.register_plugin_from_data(data)
        return [name for name in self.analysis_stage.get_plugin_names() \
                if name not in names]

    def register_format(self, config_path : str) -> Tuple[str,List[str]]:
        format_name, parsed_data = self.loader.parse_format_configuration_file(
            config_path)
        return (format_name,
            self.format_stage.register_format(format_name, parsed_data))

    def start_service(self) -> PipelineServiceSummary:
        # TODO: Do not hard-code format name
        self.payload.set_format("normal")
        self.pipeline.set_base_input(self.payload)
        self.pipeline.execute()
        return self._generate_pipeline_summary(
            self.payload,self.pipeline.get_execution_summary())

    ################################# GETTERS ###############################

    def get_analysis_plugin_names(self) -> List[str]:
        return self.analysis_stage.get_plugin_names()

    def get_format_names(self) -> List[str]:
        return self.format_stage.get_formats()

    def get_format_plugin_names(self, format_name : str) -> List[str]:
        return self.format_stage.get_format_plugins(format_name)

    def add_conversations(self, conversations : Dict[str,Conversation]) -> bool:
        return self.payload.add_conversations(conversations)

    def is_conversation(self, conversation_name : str) -> bool:
        return self.payload.is_conversation(conversation_name)

    def get_conversations(self) -> Dict[str,Conversation]:
        return self.payload.get_conversations()

    ########################## PRIVATE METHODS ###############################

    def _generate_pipeline_summary(self, payload : PipelineServicePayload,
            pipeline_summary : Dict) -> PipelineServiceSummary:
        print(pipeline_summary)
        return PipelineServiceSummary()






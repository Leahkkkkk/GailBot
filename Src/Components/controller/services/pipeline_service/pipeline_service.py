# Standard library imports
from typing import List, Dict
# Local imports
from ....pipeline import Pipeline
from ....organizer import Conversation
from .payload import PipelineServicePayload
from .summary import PipelineServiceSummary
from .logic import PipelineServiceLogic
from .transcription_stage import TranscriptionStage
from .analysis_stage import AnalysisStage
from .formatter_stage import FormatterStage

# Third party imports

class TranscriptionPipelineService:

    def __init__(self) -> None:
        ## Vars.
        self.pipeline_name = "transcription_pipeline_service"
        self.pipeline_num_threads = 4
        ## Stage objects
        self.transcription_stage = TranscriptionStage()
        self.analysis_stage = AnalysisStage()
        self.formatter_stage = FormatterStage()
        ## Other objects
        self.payload = PipelineServicePayload()
        self.pipeline_logic = PipelineServiceLogic()
        ## Initializing the pipeline
        self.pipeline = Pipeline(self.pipeline_name,self.pipeline_num_threads)
        self.pipeline.set_logic(self.pipeline_logic)
        self.pipeline.add_component(
            "transcription_stage", self.transcription_stage)
        self.pipeline.add_component(
            "analysis_stage",self.analysis_stage,["transcription_stage"])
        self.pipeline.add_component(
            "formatter_stage",self.formatter_stage,["analysis_stage"])

    ################################# MODIFIERS #############################

    def register_analysis_plugins_from_directory(self, dir_path : str) -> int:
        return self.analysis_stage.register_plugins_from_directory(dir_path)

    def add_conversation(self, conversation : Conversation) -> bool:
        return self.payload.add_conversation(conversation)

    def add_conversations(self, conversations : List[Conversation]) -> bool:
        return self.payload.add_conversations(conversations)

    def remove_conversation(self, conversation_name : str) -> bool:
        return self.payload.remove_conversation(conversation_name)

    def clear_conversations(self) -> bool:
        return self.payload.clear_conversations()

    def start_pipeline_service(self) -> PipelineServiceSummary:
        self.pipeline.set_base_input(self.payload)
        self.pipeline.execute()
        # TODO: Generate the results somehow.
        return PipelineServiceSummary()

    ################################# GETTERS ###############################

    def is_conversation(self, conversation_name : str) -> bool:
        return self.payload.is_conversation(conversation_name)

    def get_conversations(self) -> Dict[str,Conversation]:
        return self.payload.get_conversations()

    ############################ PRIVATE METHODS  ##########################
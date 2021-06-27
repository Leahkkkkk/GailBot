
from typing import List, Dict
# Local imports
from .....utils.manager import ObjectManager
from ....engines import Engines
from ....network import Network
from ....organizer import Conversation
from ....pipeline import Pipeline
from ....io import IO
from ..status import TranscriptionStatus
from .transcription_stage import TranscriptionStage
from .analysis_stage import AnalysisStage
from .formatter_stage import FormatterStage
from .pipeline_summary import PipelineServiceSummary
from .logic import PipelineServiceLogic
from .transcribable import Transcribable
# Third party imports

class TranscriptionPipelineService:

    def __init__(self) -> None:
        ## Vars.
        self.pipeline_name = "transcription_pipeline_service"
        self.pipeline_num_threads = 4
        self.transcription_stage_threads = 4
        ## Stage Objects
        self.transcription_stage = TranscriptionStage(
            self.transcription_stage_threads)
        self.analysis_stage = AnalysisStage()
        self.formatter_stage = FormatterStage()
        ## Initializing the pipeline
        self.pipeline = Pipeline(self.pipeline_name,self.pipeline_num_threads)
        self.pipeline.set_logic(PipelineServiceLogic())
        self.pipeline.add_component(
            "transcription_stage", self.transcription_stage)
        self.pipeline.add_component(
            "analysis_stage",self.analysis_stage,["transcription_stage"])
        self.pipeline.add_component(
            "formatter_stage",self.formatter_stage,["analysis_stage"])
        ## Other objects
        self.transcribables = ObjectManager()
    ################################# MODIFIERS #############################

    def add_conversation(self, conversation : Conversation) -> bool:
        return self.transcribables.add_object(
            conversation.get_conversation_name(),
            self._initialize_transcribable(conversation))

    def add_conversations(self, conversations : List[Conversation]) -> bool:
        return all([self.add_conversation(conv) for conv in conversations])

    def remove_conversation(self, conversation : Conversation) -> bool:
        return self.transcribables.remove_object(
            conversation.get_conversation_name())

    def clear_conversations(self) -> bool:
        return self.transcribables.clear_objects()

    def start_pipeline_service(self) -> PipelineServiceSummary:
        transcribables = list(self.transcribables.get_all_objects().values())
        self.pipeline.set_base_input(transcribables)
        self.pipeline.execute()
        return PipelineServiceSummary(
            list(self.get_successfully_transcribed_conversations().keys()),
            list(self.get_unsuccessfully_transcribed_conversations().keys()),
            list(self.get_ready_to_transcribe_conversations().keys()))

    ################################# GETTERS ###############################

    def is_conversation(self, conversation_name : str) -> bool:
        return self.transcribables.is_object(conversation_name)

    def get_successfully_transcribed_conversations(self) \
            -> Dict[str,Conversation]:
        return self._get_conversations_with_status(
            TranscriptionStatus.successful)

    def get_unsuccessfully_transcribed_conversations(self) \
            -> Dict[str,Conversation]:
        return self._get_conversations_with_status(
            TranscriptionStatus.unsuccessful)

    def get_ready_to_transcribe_conversations(self) \
            -> Dict[str,Conversation]:
        return self._get_conversations_with_status(TranscriptionStatus.ready)

    def get_all_conversations(self) -> Dict[str,Conversation]:
        return self._get_conversation_map(
            self.transcribables.get_all_objects())

    ############################ PRIVATE METHODS  ##########################

    def _initialize_transcribable(self, conversation : Conversation) \
            -> Transcribable:
        return Transcribable(
            conversation.get_conversation_name(),
            conversation)

    def _get_conversation_map(self, transcribable_map : Dict[str,Transcribable]) \
            -> Dict[str,Conversation]:
        conversation_map = dict()
        for conv_name, transcribable in transcribable_map.items():
            transcribable : Transcribable
            conversation_map[conv_name] = transcribable.conversation
        return conversation_map

    def _get_conversations_with_status(self, status : TranscriptionStatus) \
            -> Dict[str,Conversation]:
        transcribable_map =  self.transcribables.get_filtered_objects(
            lambda conv_name, transcribable :
                transcribable.conversation.get_transcription_status() == \
                    status)
        return self._get_conversation_map(transcribable_map)












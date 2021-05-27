# Standard imports
from typing import List
import itertools
# Local imports
from ....engines import Engines
from ....network import Network
from ....organizer import Conversation
from ....pipeline import Pipeline
from ....io import IO
from .transcription_stage import TranscriptionStage
from .summary import TranscriptionSummary
from .transcription_logic import TranscriptionLogic
from ..status import TranscriptionStatus
# Third party imports

class TranscriptionPipelineService:

    def __init__(self) -> None:
        self.pipeline = Pipeline("transcription_pipeline")
        self.pipeline.set_logic(TranscriptionLogic())
        self._initialize_transcription_pipeline_components(self.pipeline)
        self.successful_transcriptions = list()
        self.unsuccessful_transcriptions = list()
        self.ready_conversations = list()

    ################################# MODIFIERS #############################

    def start_transcription_process(self) -> None:
        if not self.is_ready_to_transcribe():
            return
        self.pipeline.set_base_input(self.ready_conversations)
        self.pipeline.execute()
        self._sort_conversations(self.get_all_conversations())

    def clear_conversations(self) -> None:
        self.successful_transcriptions.clear()
        self.unsuccessful_transcriptions.clear()
        self.ready_conversations.clear()

    ################################# GETTERS ###############################

    def is_configured(self) -> bool:
        return True

    def is_ready_to_transcribe(self) -> bool:
        return self.get_number_ready_for_transcription() > 0

    def get_transcription_summary(self) -> TranscriptionSummary:
        return TranscriptionSummary(
            self.get_names_successful_transcription(),
            self.get_names_unsuccessful_transcription(),
            self.get_names_ready_for_transcription(),
            self.get_number_successful_transcription(),
            self.get_number_unsuccessful_transcription(),
            self.get_number_ready_for_transcription(),
            self._get_transcription_runtime_seconds())

    def get_names_successful_transcription(self) -> List[str]:
        return self._get_names_from_conversations(
            self.successful_transcriptions)

    def get_names_unsuccessful_transcription(self) -> List[str]:
        return self._get_names_from_conversations(
            self.unsuccessful_transcriptions)

    def get_names_ready_for_transcription(self) -> List[str]:
        return self._get_names_from_conversations(
            self.ready_conversations)

    def get_number_successful_transcription(self) -> int:
        return len(self.successful_transcriptions)

    def get_number_unsuccessful_transcription(self) -> int:
        return len(self.unsuccessful_transcriptions)

    def get_number_ready_for_transcription(self) -> int:
        return len(self.ready_conversations)

    def get_number_all_conversations(self) -> int:
        return self.get_number_successful_transcription() + \
            self.get_number_unsuccessful_transcription() + \
            self.get_number_ready_for_transcription()

    def get_successful_transcriptions(self) -> List[Conversation]:
        return self.successful_transcriptions

    def get_unsuccessful_transcriptions(self) -> List[Conversation]:
        return self.unsuccessful_transcriptions

    def get_ready_transcriptions(self) -> List[Conversation]:
        return self.ready_conversations

    def get_all_conversations(self) -> List[Conversation]:
        return list(itertools.chain(
            self.get_successful_transcriptions(),
            self.get_unsuccessful_transcriptions(),
            self.get_ready_transcriptions()))

    ################################# SETTERS ###############################

    def add_conversations_to_transcribe(self,
            conversations : List[Conversation]) -> None:
        for conversation in conversations:
            conversation : Conversation
            if conversation.get_transcription_status() == \
                    TranscriptionStatus.ready:
                self.ready_conversations.append(conversation)

     ############################ PRIVATE METHODS  ##########################

    def _initialize_transcription_pipeline_components(
            self, pipeline : Pipeline) -> None:
        ts =  TranscriptionStage(
            engines =Engines(IO(),Network()), io=IO(),num_threads=10)
        pipeline.add_component(
            "transcription_stage",{"transcription_stage" :ts})
        pipeline.add_component("analyzer_stage", {"analyzer_stage" : None})
        pipeline.add_component("formatter_stage", {"formatter_stage" : None})

    def _get_names_from_conversations(self, conversations : List[Conversation])\
            -> List[str]:
        names = list()
        for conversation in conversations:
            conversation : Conversation
            names.append(conversation.get_conversation_name())
        return names

    def _sort_conversations(self, conversations : List[Conversation]) -> None:
        self.ready_conversations.clear()
        self.successful_transcriptions.clear()
        self.unsuccessful_transcriptions.clear()
        for conversation in conversations:
            status = conversation.get_transcription_status()
            if status == TranscriptionStatus.ready:
                self.ready_conversations.append(conversation)
            elif status == TranscriptionStatus.successful:
                self.successful_transcriptions.append(conversation)
            elif status == TranscriptionStatus.unsuccessful:
                self.unsuccessful_transcriptions.append(conversation)
            else:
                raise Exception("Invalid conversation status")

    def _get_transcription_runtime_seconds(self) -> int:
        time_seconds = 0
        execution_summary = self.pipeline.get_execution_summary()
        for component_summary in execution_summary.values():
            time_seconds += component_summary["runtime_seconds"]
        return time_seconds




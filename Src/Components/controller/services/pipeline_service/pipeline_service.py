# Standard imports
from typing import List, Dict
# Local imports
from .....utils.manager import ObjectManager
from ....engines import Engines
from ....network import Network
from ....organizer import Conversation
from ....pipeline import Pipeline
from ....io import IO
from .transcription_stage import TranscriptionStage
from .formatter_stage import FormatterStage
from .summary import TranscriptionSummary
from .transcription_logic import TranscriptionLogic
from ..status import TranscriptionStatus
# Third party imports

# TODO: Create a maximum limit on the number of threads.
class TranscriptionPipelineService:

    def __init__(self) -> None:
        self.pipeline_name = "Transcription_pipeline"
        # TODO: Make the num threads a configurable parameter.
        self.pipeline_num_threads = 4
        self.pipeline = Pipeline(self.pipeline_name)
        self.pipeline.set_logic(TranscriptionLogic())
        self._initialize_pipeline_components(self.pipeline)
        self.manager = ObjectManager()

    ################################# MODIFIERS #############################

    def add_conversation(self, conversation : Conversation) -> bool:
        """
        Add a conversation to transcribe.
        Conversation status must be 'ready'.
        """
        if self.manager.is_object(conversation.get_conversation_name()):
            return False
        return self.manager.add_object(
            conversation.get_conversation_name(),conversation)

    def add_conversations(self, conversations : List[Conversation]) -> bool:
        """
        Add multiple conversations to transcribe.
        Conversation status must be 'ready'.
        """
        return all([self.add_conversation(conversation) \
            for conversation in conversations])

    def start_transcription_pipeline(self) -> TranscriptionSummary:
        """
        Start the transcription process for conversations with status 'ready'.
        """
        conversations = list(self._get_conversations_with_status(
            TranscriptionStatus.ready).values())
        self.pipeline.set_base_input(conversations)
        self.pipeline.execute()
        return self.get_transcription_summary()

    def remove_conversation(self, conversation_name : str) -> bool:
        """
        Remove a conversation from the transcription pipeline.
        """
        return self.manager.remove_object(conversation_name)

    def remove_conversations(self, conversation_names : List[str]) -> bool:
        """
        Remove multiple conversations from the transcription pipeline.
        """
        return all([self.remove_conversation(name) \
            for name in conversation_names])

    def clear_conversations(self) -> bool:
        """
        Remove all conversations from the transcription pipeline.
        """
        return self.remove_conversations(self.manager.get_object_names())

    ################################# GETTERS ###############################

    def get_transcription_summary(self) -> TranscriptionSummary:
        """
        Obtain a summary of the previously executed transcription.
        """
        successful_names = list(
            self.get_successfully_transcribed_conversations().keys())
        unsuccessful_names = list(
            self.get_unsuccessfully_transcribed_conversations().keys())
        ready_names = list(self.get_ready_to_transcribe_conversations().keys())
        return TranscriptionSummary(
            successful_names, unsuccessful_names, ready_names,
            len(successful_names),len(unsuccessful_names),len(ready_names),
            self._get_total_runtime_seconds())

    def is_added_conversation(self, conversation_name : str) -> bool:
        """
        Determine if the conversation exists in the pipeline.
        """
        return self.manager.is_object(conversation_name)

    def get_successfully_transcribed_conversations(self) \
            -> Dict[str,Conversation]:
        """
        Obtain the conversations that have been successfully transcribed.
        """
        return self._get_conversations_with_status(
            TranscriptionStatus.successful)

    def get_unsuccessfully_transcribed_conversations(self) \
            -> Dict[str,Conversation]:
        """
        Obtain the conversations that have not been successfully transcribed.
        """
        return self._get_conversations_with_status(
            TranscriptionStatus.unsuccessful)

    def get_ready_to_transcribe_conversations(self) \
            -> Dict[str,Conversation]:
        """
        Obtain conversations that are ready to transcribe.
        """
        return self._get_conversations_with_status(TranscriptionStatus.ready)

    def get_all_conversations(self) -> Dict[str,Conversation]:
        """
        Obtain all conversations in the pipeline.
        """
        return self.manager.get_all_objects()

    ################################# SETTERS ###############################

    ############################ PRIVATE METHODS  ##########################

    def _initialize_pipeline_components(self, pipeline : Pipeline) -> None:
        """
        Configure the pipeline for the transcription process.
        """
        ## Objects
        transcription_stage = TranscriptionStage(
            engines = Engines(IO(),Network()),io=IO(),
            num_threads=self.pipeline_num_threads)
        ## Adding components
        pipeline.add_component(
            "transcription_stage",{"transcription_stage" : transcription_stage})
        pipeline.add_component("analyzer_stage", {"analyzer_stage" : None},
            ["transcription_stage"])
        pipeline.add_component("formatter_stage",
            {"formatter_stage" : FormatterStage},["analyzer_stage"])

    def _get_conversations_with_status(self,
            status : TranscriptionStatus) -> Dict[str,Conversation]:
        """
        Obtain all conversations with the specified status.
        """
        return self.manager.get_filtered_objects(
            lambda name, obj : obj.get_transcription_status() \
                == status)

    def _get_total_runtime_seconds(self) -> int:
        """
        Obtain the total runtime of the entire pipeline.
        """
        time_seconds = 0
        execution_summary = self.pipeline.get_execution_summary()
        for component_summary in execution_summary.values():
            time_seconds += component_summary["runtime_seconds"]
        return time_seconds








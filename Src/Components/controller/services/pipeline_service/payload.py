# Standard library imports
from dataclasses import dataclass
from typing import List, Dict, Any
# Local imports
from ....organizer import Conversation
from .....utils.manager import ObjectManager

# Third party imports

class StageResults:
    transcription_stage  : Any
    analysis_stage : Any
    formatter_stage : Any

class PipelineServicePayload:

    def __init__(self) -> None:
        ## Objects
        self.manager = ObjectManager()
        self.stage_results = StageResults()

    def add_conversation(self, conversation : Conversation) -> bool:
        return self.manager.add_object(
            conversation.get_conversation_name(),conversation)

    def add_conversations(self, conversations : List[Conversation]) -> bool:
        return all([self.add_conversation(conversation) \
            for conversation in conversations])

    def remove_conversation(self, conversation_name : str) -> bool:
        return self.manager.remove_object(conversation_name)

    def clear_conversations(self) -> bool:
        return self.manager.clear_objects()

    def is_conversation(self, conversation_name : str) -> bool:
        return self.manager.is_object(conversation_name)

    def get_conversations(self) -> Dict[str,Conversation]:
        return self.manager.get_all_objects()

    def get_transcription_stage_output(self) -> Any:
        return self.stage_results.transcription_stage

    def get_analysis_stage_output(self) -> Any:
        return self.stage_results.analysis_stage

    def get_formatter_stage_output(self) -> Any:
        return self.stage_results.formatter_stage

    def set_transcription_stage_output(self, output : Any) -> bool:
        self.stage_results.transcription_stage = output
        return True

    def set_analysis_stage_output(self, output : Any) -> bool:
        self.stage_results.analysis_stage = output
        return True

    def set_formatter_stage_output(self, output : Any) -> bool:
        self.stage_results.formatter_stage = output
        return True

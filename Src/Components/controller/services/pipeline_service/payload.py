# Standard library imports
from dataclasses import dataclass
from typing import List, Dict, Any
# Local imports
from ....organizer import Conversation
from .....utils.manager import ObjectManager
from .transcription_stage import TranscriptionStageResult
from .format_stage import FormatStageResult
from .analysis_stage import AnalysisStageResult

# Third party imports

@dataclass
class StageResults:
    transcription_stage  : TranscriptionStageResult = None
    analysis_stage : AnalysisStageResult = None
    format_stage : FormatStageResult = None

class PipelineServicePayload:

    def __init__(self) -> None:
        ## Vars.
        self.format_name = ""
        ## Objects
        self.manager = ObjectManager()
        self.stage_results = StageResults()

    ############################ MODIFIERS ###################################

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

    ############################ GETTERS ######################################

    def is_conversation(self, conversation_name : str) -> bool:
        return self.manager.is_object(conversation_name)

    def get_conversations(self) -> Dict[str,Conversation]:
        return self.manager.get_all_objects()

    def get_transcription_stage_output(self) -> TranscriptionStageResult:
        return self.stage_results.transcription_stage

    def get_analysis_stage_output(self) -> AnalysisStageResult:
        return self.stage_results.analysis_stage

    def set_format(self, format_name : str) -> str:
        self.format_name = format_name

    def get_format_stage_output(self) -> FormatStageResult:
        return self.stage_results.format_stage

    ############################ SETTERS ######################################

    def set_transcription_stage_output(self, output : TranscriptionStageResult)\
             -> bool:
        self.stage_results.transcription_stage = output
        return True

    def set_analysis_stage_output(self, output : AnalysisStageResult) -> bool:
        self.stage_results.analysis_stage = output
        return True

    def set_format_stage_output(self, output : FormatStageResult) -> bool:
        self.stage_results.format_stage = output
        return True

    def get_format(self) -> str:
        return self.format_name

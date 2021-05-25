# Standard imports
from typing import Dict, List, Any
# Local imports
from ....pipeline import Logic, Stream, Pipeline
from ....organizer import Conversation
from .transcription_stage import TranscriptionStage
# Third party imports

class TranscriptionLogic(Logic):

    def __init__(self) -> None:
        super().__init__()
        self._add_component_logic(
            "transcription_stage",self._transcription_stage_preprocessor,
            self._transcription_stage_processor,
            self._transcription_stage_postprocessor)
        self._add_component_logic(
            "analyzer_stage",self._analyzer_stage_preprocessor,
            self._analyzer_stage_processor,self._analyzer_stage_post_processor)
        self._add_component_logic(
            "formatter_stage", self._formatter_stage_preprocessor,
            self._formatter_stage_processor,self._formatter_stage_postprocessor)

    #### Transcription stage methods
    def _transcription_stage_preprocessor(self, streams : Dict[str,Stream]) \
             -> List[Conversation]:
        return streams["base"].get_stream_data()

    def _transcription_stage_processor(
            self, objects : Dict[str,Any], conversations : List[Conversation]) \
            -> Conversation:
        transcription_stage : TranscriptionStage \
            = objects["transcription_stage"]
        transcription_stage.set_conversations(conversations)
        transcription_stage.transcribe()
        return conversations

    def _transcription_stage_postprocessor(self,
            conversations : List[Conversation])  -> Stream:
        return Stream(conversations)

    def _analyzer_stage_preprocessor(self, streams : Dict[str,Stream]) \
            -> List[Conversation]:
        return streams["transcription_stage"].get_stream_data()

    def _analyzer_stage_processor(self, objects : Dict[str,Any],
            conversations : List[Conversation]) -> List[Conversation]:
        return conversations

    def _analyzer_stage_post_processor(self,conversations : List[Conversation]) \
            -> Stream:
        return Stream(conversations)

    def _formatter_stage_preprocessor(self, streams : Dict[str,Stream]) \
            -> List[Conversation]:
        return streams["analyzer_stage"].get_stream_data()

    def _formatter_stage_processor(self, objects : Dict[str,Any],
            conversations : List[Conversation])  -> List[Conversation]:
        return conversations

    def _formatter_stage_postprocessor(self, conversations : List[Conversation]) \
            -> Stream:
        return Stream(conversations)

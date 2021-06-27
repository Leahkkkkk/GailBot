# Standard imports
from typing import Dict, List, Any
# Local imports
from ....pipeline import Logic, Stream
from .transcription_stage import TranscriptionStage
from .analysis_stage import AnalysisStage
from .formatter_stage import FormatterStage
from .transcribable import Transcribable

# Third party imports

class PipelineServiceLogic(Logic):

    def __init__(self) -> None:
        super().__init__()
        # Adding all components
        self._add_component_logic(
            "transcription_stage", self._transcription_stage_preprocessor,
            self._transcription_stage_processor,self._wrap_as_stream)
        self._add_component_logic(
            "analysis_stage",self._analyzer_stage_preprocessor,
            self._analyzer_stage_processor, self._wrap_as_stream)
        self._add_component_logic(
            "formatter_stage", self._formatter_stage_preprocessor,
            self._formatter_stage_processor,self._wrap_as_stream)

    ### General

    def _wrap_as_stream(self, transcribables : List[Transcribable]) -> Stream:
        return Stream(transcribables)

    ### TranscriptionStage methods
    def _transcription_stage_preprocessor(self, streams : Dict[str,Stream]) \
            -> List[Transcribable]:
        return streams["base"].get_stream_data()

    def _transcription_stage_processor(self,
            transcription_stage : TranscriptionStage,
            transcribables : List[Transcribable]) -> List[Transcribable]:
        transcription_stage.add_transcribables(transcribables)
        transcription_stage.generate_utterances()
        return list(transcription_stage.get_transcribables().values())

    ### AnalyzerStage methods

    def _analyzer_stage_preprocessor(self, streams : Dict[str,Stream]) \
            -> List[Transcribable]:
        return streams["transcription_stage"].get_stream_data()

    def _analyzer_stage_processor(self, analysis_stage : AnalysisStage,
            transcribables : List[Transcribable]) -> List[Transcribable]:
        analysis_stage.add_transcribables(transcribables)
        analysis_stage.analyze()
        return transcribables

    ### FormatterStage methods

    def _formatter_stage_preprocessor(self, streams : Dict[str,Stream]) \
            -> List[Transcribable]:
        return streams["analysis_stage"].get_stream_data()

    def _formatter_stage_processor(self, formatter_stage : FormatterStage,
            transcribables : List[Transcribable]) -> List[Transcribable]:
        return transcribables













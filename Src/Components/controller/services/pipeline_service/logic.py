# Standard imports
from typing import Dict, List, Any
# Local imports
from ....pipeline import Logic, Stream
from .payload import PipelineServicePayload
from .transcription_stage import TranscriptionStage
from .analysis_stage import AnalysisStage
from .formatter_stage import FormatterStage

# Third party imports

class PipelineServiceLogic(Logic):

    def __init__(self) -> None:
        super().__init__()
        # Adding all components
        self._add_component_logic(
            "transcription_stage", self._unwrap_stream,
            self._transcription_stage_processor,self._wrap_as_stream)
        self._add_component_logic(
            "analysis_stage",self._unwrap_stream,
            self._analyzer_stage_processor, self._wrap_as_stream)
        self._add_component_logic(
            "formatter_stage", self._unwrap_stream,
            self._formatter_stage_processor,self._wrap_as_stream)

    ## General

    def _wrap_as_stream(self, payload : PipelineServicePayload) -> Stream:
        return Stream(payload)

    def _unwrap_stream(self, streams: Dict[str,Stream]) -> PipelineServicePayload:
        return streams["base"].get_stream_data()

    def _transcription_stage_processor(self,
            transcription_stage : TranscriptionStage,
            payload : PipelineServicePayload) \
            -> PipelineServicePayload:
        output = transcription_stage.generate_utterances(
            payload.get_conversations())
        payload.set_transcription_stage_output(output)
        return payload

    def _analyzer_stage_processor(self, analysis_stage : AnalysisStage,
            payload : PipelineServicePayload) -> PipelineServicePayload:
        output = analysis_stage.analyze(
            payload.get_transcription_stage_output())
        payload.set_analysis_stage_output(output)
        return output

    def _formatter_stage_processor(self, formatter_stage : FormatterStage,
            payload : PipelineServicePayload) -> PipelineServicePayload:
        # TODO Add FormatterStage calls.
        return payload




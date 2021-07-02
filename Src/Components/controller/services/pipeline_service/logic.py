# Standard imports
from typing import Dict, List, Any
# Local imports
from ....pipeline import Logic, Stream
from .payload import PipelineServicePayload
from .transcription_stage import TranscriptionStage
from .analysis_stage import AnalysisStage
from .format_stage import FormatStage

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
            "format_stage", self._unwrap_stream,
            self._format_stage_processor,self._wrap_as_stream)

    ## General

    def _wrap_as_stream(self, payload : PipelineServicePayload) -> Stream:
        """
        Wrap the payload as a Stream.
        """
        return Stream(payload)

    def _unwrap_stream(self, streams: Dict[str,Stream]) -> PipelineServicePayload:
        """
        Obtain the payload from the base input to the Pipeline.
        """
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
            payload.get_conversations(),
            payload.get_transcription_stage_output())
        payload.set_analysis_stage_output(output)
        return payload

    def _format_stage_processor(self, format_stage : FormatStage,
            payload : PipelineServicePayload) -> PipelineServicePayload:
        output = format_stage.format_conversations(
            payload.get_format(), payload.get_conversations(),
            payload.get_analysis_stage_output())
        payload.set_format_stage_output(output)
        return payload





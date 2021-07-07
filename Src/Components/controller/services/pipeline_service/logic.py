# Standard imports
from typing import Dict, List, Any
# Local imports
from ....pipeline import Logic, Stream
from .pipeline_payload import SourcePayload
from .transcription_stage.transcription_stage import TranscriptionStage
from .analysis_stage.analysis_stage import AnalysisStage
from .format_stage.format_stage import FormatStage

class PipelineServiceLogic(Logic):

    def __init__(self) -> None:
        super().__init__()
        # Adding all components
        self._add_component_logic(
            "transcription_stage", self._get_base_sources,
            self._transcription_stage_processor,self._wrap_sources_as_stream)
        self._add_component_logic(
            "analysis_stage",self._get_base_sources,
            self._analysis_stage_processor, self._wrap_sources_as_stream)
        self._add_component_logic(
            "format_stage", self._get_base_sources,
            self._format_stage_processor, self._wrap_sources_as_stream)

    def _get_base_sources(self, streams : Dict[str,Stream]) \
            -> Dict[str,SourcePayload]:
        return streams["base"].get_stream_data()

    def _wrap_sources_as_stream(self, payloads : Dict[str,SourcePayload]) \
            -> Stream:
        return Stream(payloads)

    ## TranscriptionStage

    def _transcription_stage_processor(self,
            transcription_stage : TranscriptionStage,
                payloads : Dict[str,SourcePayload]) -> Dict[str,SourcePayload]:
        transcription_stage.add_payloads(payloads)
        transcription_stage.generate_utterances()
        return transcription_stage.get_payloads

    ## AnalysisStage

    def _analysis_stage_processor(self,
            analysis_stage : AnalysisStage,
                payloads : Dict[str,SourcePayload]) -> Dict[str,SourcePayload]:
        analysis_stage.add_payloads(payloads)
        analysis_stage.analyze()
        return analysis_stage.get_payloads()

    ## FormatStage

    def _format_stage_processor(self,
            format_stage : FormatStage,
                payloads : Dict[str,SourcePayload]) -> Dict[str,SourcePayload]:
        format_stage.add_payloads(payloads)
        format_stage.apply_format()
        return format_stage.get_payloads()




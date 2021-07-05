# Standard imports
from typing import Dict, List, Any
# Local imports
from ....pipeline import Logic, Stream
from .source import Source
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

    def _get_base_sources(self, streams : Dict[str,Stream]) -> Dict[str,Source]:
        return streams["base"].get_stream_data()

    def _wrap_sources_as_stream(self, sources : Dict[str,Source]) -> Stream:
        return Stream(sources)

    ## TranscriptionStage

    def _transcription_stage_processor(self,
            transcription_stage : TranscriptionStage,
                sources : Dict[str,Source]) -> Dict[str,Source]:
        transcription_stage.add_sources(sources)
        transcription_stage.generate_utterances()
        return transcription_stage.get_sources()

    ## AnalysisStage

    def _analysis_stage_processor(self,
            analysis_stage : AnalysisStage,
                sources : Dict[str,Source]) -> Dict[str,Source]:

        analysis_stage.add_sources(sources)
        analysis_stage.analyze()
        return analysis_stage.get_sources()

    ## FormatStage

    def _format_stage_processor(self,
            format_stage : FormatStage,
                sources : Dict[str,Source]) -> Dict[str,Source]:
        format_stage.add_sources(sources)
        format_stage.apply_format()
        return format_stage.get_sources()




# # Standard imports
from typing import List, Tuple, Dict, Any
# Local imports
from ...utils.manager import ObjectManager
from ...pipeline import Pipeline, Logic, Stream
from ...plugin_manager import PluginExecutionSummary
from ...services import Source, SettingsProfile


class GBPipelineLogic(Logic):

    def __init__(self) -> None:
        super().__init__()
        # add the components
        self._add_component_logic(
            "transcription_stage", self._get_base_sources,
            self._transcription_stage_processor,
            self._wrap_payloads_as_stream)
        self._add_component_logic(
            "plugins_stage", self._get_base_sources,
            self._plugin_stage_processor,
            self._wrap_payloads_as_stream)
        self._add_component_logic(
            "output_stage", self._get_base_sources,
            self._output_stage_processor,
            self._wrap_payloads_as_stream)

    def _get_base_sources(self, streams: Dict[str, Stream]) \
            -> Dict[str, Any]:
        return streams["base"].get_stream_data()

    def _wrap_payloads_as_stream(self, payloads: Dict[str, Any]) \
            -> Stream:
        pass

    # TranscriptionStage

    def _transcription_stage_processor(self,
                                       transcription_stage: Any,
                                       payloads: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the transcription stage for each payload object in a separate
        thread.
        """
        pass

    # AnalysisStage

    def _plugin_stage_processor(self,
                                analysis_stage: Any,
                                payloads: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the analysis stage for each payload object in a separate
        thread.
        """
        pass

    # Output stage

    def _output_stage_processor(self,
                                output_stage: Any,
                                payloads: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the output stage for each payload object in a separate
        thread.
        """
        pass

    def _transcription_stage_thread(self, stage: Any,
                                    payload: Any) -> None:
        payload.log("Starting transcription stage....")
        stage.generate_utterances(payload)

    def _plugin_stage_thread(self, stage: Any,
                             payload: Any) -> None:
        payload.log("Starting analysis stage....")
        stage.analyze(payload)

    def _output_stage_thread(self, stage: Any,
                             payload: Any) -> None:
        payload.log("Starting output stage....")
        stage.output(payload)

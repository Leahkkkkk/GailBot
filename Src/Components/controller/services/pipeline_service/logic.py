# Standard imports
from typing import Dict, List, Any, Callable
# Local imports
from .....utils.threads import ThreadPool
from ....pipeline import Logic, Stream
from ..organizer_service import RequestType
from .pipeline_payload import SourcePayload
from .transcription_stage.transcription_stage import TranscriptionStage
from .analysis_stage.analysis_stage import AnalysisStage
from .format_stage.format_stage import FormatStage
from .output_stage.output_stage import OutputStage

class PipelineServiceLogic(Logic):
    """
    Central logic for the PipelineService
    The components are: 'transcription_stage', 'analysis_stage',
                        'format_stage', 'output_stage'
    Base data is expected to be Dict[str,SourcePayload]
    """

    NUM_THREADS = 4

    def __init__(self) -> None:
        super().__init__()
        # Adding all components
        self._add_component_logic(
            "transcription_stage", self._get_base_sources,
            self._transcription_stage_processor,self._wrap_payloads_as_stream)
        self._add_component_logic(
            "analysis_stage",self._get_base_sources,
            self._analysis_stage_processor, self._wrap_payloads_as_stream)
        self._add_component_logic(
            "format_stage", self._get_base_sources,
            self._format_stage_processor, self._wrap_payloads_as_stream)
        self._add_component_logic(
            "output_stage", self._get_base_sources,
            self._output_stage_processor, self._wrap_payloads_as_stream)
        # Initializing the thread pools
        self.thread_pool = ThreadPool(self.NUM_THREADS)
        self.thread_pool.spawn_threads()

    def _get_base_sources(self, streams : Dict[str,Stream]) \
            -> Dict[str,SourcePayload]:
        return streams["base"].get_stream_data()

    def _wrap_payloads_as_stream(self, payloads : Dict[str,SourcePayload]) \
            -> Stream:
        return Stream(payloads)

    ## TranscriptionStage

    def _transcription_stage_processor(self,
            transcription_stage : TranscriptionStage,
                payloads : Dict[str,SourcePayload]) -> Dict[str,SourcePayload]:
        """
        Executes the transcription stage for each payload object in a separate
        thread.
        """
        for payload_name, payload in payloads.items():
            self.thread_pool.add_task(
                self._transcription_stage_thread,
                [transcription_stage,payload],{})
        self.thread_pool.wait_completion()
        return payloads

    ## AnalysisStage

    def _analysis_stage_processor(self,
            analysis_stage : AnalysisStage,
                payloads : Dict[str,SourcePayload]) -> Dict[str,SourcePayload]:
        """
        Executes the analysis stage for each payload object in a separate
        thread.
        """
        for payload_name, payload in payloads.items():
            self.thread_pool.add_task(
                self._analysis_stage_thread,
                [analysis_stage,payload],{})
        self.thread_pool.wait_completion()
        return payloads

    ## FormatStage

    def _format_stage_processor(self,
            format_stage : FormatStage,
                payloads : Dict[str,SourcePayload]) -> Dict[str,SourcePayload]:
        """
        Executes the format stage for each payload object in a separate
        thread.
        """
        for payload_name, payload in payloads.items():
            self.thread_pool.add_task(
                self._format_stage_thread,
                [format_stage,payload],{})
        self.thread_pool.wait_completion()
        return payloads

    ## Output stage

    def _output_stage_processor(self,
            output_stage : OutputStage,
                payloads : Dict[str,SourcePayload]) -> Dict[str,SourcePayload]:
        """
        Executes the output stage for each payload object in a separate
        thread.
        """
        for payload_name, payload in payloads.items():
            self.thread_pool.add_task(
                self._output_stage_thread,
                [output_stage,payload],{})
        self.thread_pool.wait_completion()
        return payloads

    def _transcription_stage_thread(self, stage : TranscriptionStage,
            payload : SourcePayload) -> None:
        payload.log("Starting transcription stage....")
        stage.generate_utterances(payload)

    def _analysis_stage_thread(self, stage : AnalysisStage,
            payload : SourcePayload) -> None:
        payload.log("Starting analysis stage....")
        stage.analyze(payload)

    def _format_stage_thread(self, stage : FormatStage,
            payload : SourcePayload) -> None:
        payload.log("Starting format stage....")
        stage.apply_format(payload)

    def _output_stage_thread(self, stage : OutputStage,
            payload : SourcePayload) -> None:
        payload.log("Starting output stage....")
        stage.output(payload)

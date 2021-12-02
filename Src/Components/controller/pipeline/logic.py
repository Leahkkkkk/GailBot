# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-11-05 21:08:13
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-02 14:32:28
# # Standard imports
from typing import List, Tuple, Dict, Any
# Local imports
from ...utils.threads import ThreadPool
from ...utils.manager import ObjectManager
from ...pipeline import Pipeline, Logic, Stream
from ...plugin_manager import PluginExecutionSummary
from ...services import Source, SettingsProfile
from .transcription_stage import TranscriptionStage
from .plugins_stage import PluginsStage
from .output_stage import OutputStage
from .models import Payload


class GBPipelineLogic(Logic):

    NUM_THREADS = 4

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
        # Initializing the thread pools
        self.thread_pool = ThreadPool(self.NUM_THREADS)
        self.thread_pool.spawn_threads()

    def _get_base_sources(self, streams: Dict[str, Stream]) \
            -> Dict[str, Payload]:
        return streams["base"].get_stream_data()

    def _wrap_payloads_as_stream(self, payloads: Dict[str, Payload]) \
            -> Stream:
        return Stream(payloads)

    # TranscriptionStage

    def _transcription_stage_processor(self,
                                       transcription_stage: Any,
                                       payloads: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the transcription stage for each payload object in a separate
        thread.
        """
        print("transcription stage processor ")
        for payload_name, payload in payloads.items():
            self.thread_pool.add_task(
                self._transcription_stage_thread,
                [transcription_stage, payload], {})
        print("Waiting...")
        self.thread_pool.wait_completion()
        return payloads

    # AnalysisStage

    def _plugin_stage_processor(
            self, plugins_stage: Any,
            payloads: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the analysis stage for each payload object in a separate
        thread.
        """
        print("Plugins stage processor")
        for payload_name, payload in payloads.items():
            self.thread_pool.add_task(
                self._plugins_stage_thread,
                [plugins_stage, payload], {})
        print("Waiting...")
        self.thread_pool.wait_completion()
        print("Done plugins")
        return payloads

    # Output stage

    def _output_stage_processor(self,
                                output_stage: Any,
                                payloads: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the output stage for each payload object in a separate
        thread.
        """
        print("Output stage ")
        for payload_name, payload in payloads.items():
            self.thread_pool.add_task(
                self._output_stage_thread,
                [output_stage, payload], {})
        print("Waiting...")
        self.thread_pool.wait_completion()
        print("Completed!")
        return payloads

    def _transcription_stage_thread(self, stage: TranscriptionStage,
                                    payload: Any) -> None:
        stage.generate_utterances(payload)

    def _plugins_stage_thread(self, stage: PluginsStage,
                              payload: Payload) -> None:

        stage.apply_plugins(payload)

    def _output_stage_thread(self, stage: OutputStage,
                             payload: Payload) -> None:
        stage.output(payload)

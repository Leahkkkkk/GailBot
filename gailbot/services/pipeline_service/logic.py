# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:27:23
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-23 11:45:55
# # Standard imports
from typing import List, Tuple, Dict, Any
from datetime import datetime
import time
import logging
# Local imports
from .payload import Payload
from gailbot.core.pipeline import (
    Pipeline,
    Logic,
    Stream
)
from gailbot.utils.threads import ThreadPool



class GBPipelineLogic(Logic):

    NUM_THREADS = 10

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

    def _transcription_stage_processor(
            self, transcription_stage: Any,
            payloads: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the transcription stage for each payload object in a separate
        thread.
        """
        for payload_name, payload in payloads.items():
            self.thread_pool.add_task(
                self._transcription_stage_thread,
                [transcription_stage, payload], {})
        self.thread_pool.wait_completion()
        return payloads

    def _transcription_stage_thread(self, stage: Any,
                                    payload: Payload) -> None:
        payload.source_addons.logger.info("{0} TRANSCRIPTION STAGE {0}".format(
            "*" * 20))
        payload.source_addons.stats.process_start_time = datetime.now()
        start_time = time.time()
        stage.generate_utterances(payload)
        payload.source_addons.stats.transcription_time_sec = \
            time.time() - start_time
        payload.source_addons.logger.info(
            "Runtime {} seconds ".format(payload.source_addons.stats.transcription_time_sec))
        payload.source_addons.logger.info(
            "{0} COMPLETED {0}".format("*" * 20))

    def _plugin_stage_processor(
            self, plugins_stage: Any,
            payloads: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the analysis stage for each payload object in a separate
        thread.
        """
        for payload_name, payload in payloads.items():
            self.thread_pool.add_task(
                self._plugins_stage_thread,
                [plugins_stage, payload], {})
        self.thread_pool.wait_completion()
        return payloads

    def _plugins_stage_thread(self, stage: Any,
                              payload: Payload) -> None:
        payload.source_addons.logger.info("{0} PLUGIN STAGE STAGE {0}".format(
            "*" * 20))
        start_time = time.time()
        stage.apply_plugins(payload)
        payload.source_addons.stats.plugin_application_time_sec = \
            time.time() - start_time
        payload.source_addons.logger.info("Runtime {} seconds".format(
            payload.source_addons.stats.plugin_application_time_sec))
        payload.source_addons.logger.info("{0} COMPLETED {0}".format(
            "*" * 20))

    def _output_stage_processor(self,
                                output_stage: Any,
                                payloads: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the output stage for each payload object in a separate
        thread.
        """
        for payload_name, payload in payloads.items():
            self.thread_pool.add_task(
                self._output_stage_thread,
                [output_stage, payload], {})
        self.thread_pool.wait_completion()
        return payloads

    def _output_stage_thread(self, stage: Any,
                             payload: Payload) -> None:
        payload.source_addons.logger.info("{0} OUTPUT STAGE {0}".format(
            "*" * 20))
        stage.output(payload)
        payload.source_addons.logger.info(" {0} COMPLETED {0}".format(
            "*" * 10))

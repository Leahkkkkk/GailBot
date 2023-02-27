# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 15:20:28
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 15:40:37

from typing import Dict, Any, List
from gailbot.core.pipeline import Component, ComponentState, ComponentResult
from gailbot.core.engines import Watson
from gailbot.servicesold.organizer.objects import Source, Settings
from gailbot.core.utils.general import (
    get_name
)
import time
from ..objects import Payload, TranscriptionResults, ProcessingStats
from ...engineManager import EngineManager

import logging
logger = logging.getLogger(__name__)


class TranscribeComponent(Component):
    """
    Responsible for transcribing payloads
    """

    def __init__(
        self,
        engine_manager : EngineManager
    ):
        self.engine_manager = engine_manager

    def __repr__(self):
        return str(self)

    # TODO: Add threading ability.
    # TODO: Change things based on the config file structure.
    def __call__(
        self,
        dependency_outputs : Dict[str, Any]
    ) -> ComponentResult:
        """
        Get a source and the associated settings objects and transcribe.
        """
        # NOTE: Each component receives the base input and the dependency inputs

        payloads : List[Payload] = dependency_outputs["base"]
        res = dict()

        process_start_time = time.time()
        for payload in payloads:
            # Parse payload

            # Transcribe
            start_time = time.time()
            utt_map = self._transcribe_payload(payload)
            end_time = time.time()

            stats = ProcessingStats(
                start_time=start_time,
                end_time = end_time,
                elapsed_time_sec= end_time - start_time
            )

            # Store results
            payload.transcription_res.utterances = utt_map
            payload.transcription_res.stats = stats

        return ComponentResult(
            state=ComponentState.SUCCESS,
            result=payloads,
            runtime=time.time() - process_start_time
        )

    def _transcribe_payload(self, payload : Payload) -> None:

        # Parse the payload
        settings = payload.source.settings_profile
        outdir = payload.source.workspace
        data_files = payload.source.data_files

        # Parse the settings
        engine_name = settings.data.engine
        engine_init_kwargs = settings.data[engine_name].watson.initialize
        engine_transcribe_kwargs = settings.data[engine_name].watson.transcribe

        # Transcribe behavior is different based on the type of the input
        # For example, if source contains video files, they should first be
        # extracted into audio files here.
        # If the source is being re-transcribed, then that should be parsed here.

        # Init engine
        if not self.engine_manager.is_engine(engine_name):
            raise Exception(f"Not an engine: {engine_name}")
        engine = self.engine_manager.init_engine(
            engine_name, **engine_init_kwargs)

        # Transcribe all of the data files
        utt_map = dict()
        for data_file in data_files:
            path = data_file.path
            # Transcribe
            engine_transcribe_kwargs.update({
                "audio_path" : path,
                "outdir" : outdir
            })
            utterances = engine.transcribe(**engine_transcribe_kwargs)
            utt_map[get_name(path)] = utterances

        return utt_map










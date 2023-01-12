# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 15:20:28
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-12 14:37:29

from typing import Dict, Any, List
from gailbot.core.pipeline import Component, ComponentState, ComponentResult
from gailbot.core.engines import Watson
from gailbot.services.organizer.objects import Source, Settings
from gailbot.core.utils.general import (
    get_name
)
from ..objects import Payload, TranscriptionResults
from ...engineManager import EngineManager


class TranscribeComponent(Component):

    def __init__(
        self,
        engine_manager : EngineManager
    ):
        self.engine_manager = engine_manager

    def __repr__(self):
        raise NotImplementedError()

    # TODO: Add threading ability.
    # TODO: Change things based on the config file structure.
    def __call__(
        self,
        dependency_outputs : Dict[str, Any]
    ) -> ComponentResult:
        # NOTE: Each component receives the base input and the dependency inputs
        """Get a source and the associated settings objects and transcribe"""
        payloads : List[Payload] = dependency_outputs["base"]
        res = dict()
        for payload in payloads:
            # Parse the settings object
            settings : Settings = payload.source.settings_profile
            engine_name = settings.data.engine
            engine_init = settings.data.engine_name.watson.initialize
            engine_configs = settings.data.engine_name.watson.transcribe
            outdir = payload.source.workspace
            # TODO: Add ability to re-transcribe - need to add access to configs
            if not self.engine_manager.is_engine(engine_name):
                raise Exception(
                    f"Not an engine: {engine_name}"
                )
            engine = self.engine_manager.init_engine(engine_name)


            utt_map = dict()
            for data_file in payload.source.data_files:
                # TODO: Extract audio from the data files as required.
                path = data_file.path
                # Transcribe
                utterances = engine.transcribe(
                    audio_path=path,
                    out_dir=outdir,
                    **engine_configs
                )
                utt_map[get_name(path)] = utterances

            res[payload.transcription_res.utterances] = utt_map

        return ComponentResult(
            state=ComponentState.SUCCESS,
            result=payloads,
            runtime=0
        )








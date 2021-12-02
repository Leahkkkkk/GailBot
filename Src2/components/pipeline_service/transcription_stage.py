# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-11-05 21:08:35
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-02 16:10:37
# Standard imports
from typing import Dict, Tuple, List

from Src2.components.shared_models import utt

# Local imports
from ..utils.threads import ThreadPool
from ..engines import Engines, WatsonEngine
from ..io import IO
from .payload import Payload


class TranscriptionStage:
    SUPPORTED_ENGINES = ["watson", "google"]
    NUM_THREADS = 4

    def __init__(self) -> None:
        self.engines = Engines(IO())
        self.io = IO()
        self.thread_pool = ThreadPool(
            self.NUM_THREADS)
        self.thread_pool.spawn_threads()

    def generate_utterances(self, payload: Payload) -> None:
        print("generating utterances", payload.source)
        try:
            # Transcribe from the temp. dir
            payload.status = self._transcribe(payload)
        except Exception as e:
            print(e)

    def get_supported_engines(self) -> List[str]:
        return self.SUPPORTED_ENGINES

    ######################## PRIVATE METHODS ##################################

    def _transcribe(self, payload: Payload):
        utterances_map = dict()
        source_status_map = dict()
        self._execute_transcription_threads(
            payload, utterances_map, source_status_map)
        # Check status
        if all(list(source_status_map.values())):
            print("Transcribed")
            payload.utterances_map = utterances_map
            # return ProcessStatus.TRANSCRIBED
        else:
            print("Not transcribed")
            # return ProcessStatus.FAILED
    # --- Helpers

    def _execute_transcription_threads(
            self, payload: Payload, utterances_map: Dict,
            source_status_map: Dict) -> None:
        for data_file in payload.source.conversation.data_files:
            self.thread_pool.add_task(
                self._transcribe_watson_thread,
                [data_file.audio_path,
                 payload.source.hook.get_temp_directory_path(),
                 utterances_map, source_status_map], {})

        self.thread_pool.wait_completion()

    def _transcribe_watson_thread(
            self, audio_path, temp_dir_path, utterances_map: Dict[str, List],
            source_status_map: Dict[str, bool]) -> None:
        try:
            engine: WatsonEngine = self.engines.engine("watson")
            engine.configure(
                "MSgOPTS9CvbADe49nEg4wm8_gxeRuf4FGUmlHS9QqAw3",
                "dallas",
                audio_path,
                "en-US_BroadbandModel",
                temp_dir_path,
            )
            utterances = engine.transcribe()
            utterances_map[audio_path] = utterances
            source_status_map[audio_path] = engine.was_transcription_successful(
            )
        except Exception as e:
            print(e)

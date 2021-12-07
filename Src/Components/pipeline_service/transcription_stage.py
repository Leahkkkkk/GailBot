# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-11-05 21:08:35
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-07 12:49:57
# Standard imports
from typing import Dict, Tuple, List

# Local imports
from ..utils.threads import ThreadPool
from ..engines import Engines, WatsonEngine
from ..io import IO
from .payload import Payload
from ..shared_models import DataFile, Utt, GailBotSettings


class TranscriptionStage:
    SUPPORTED_ENGINES = ["watson", "google"]
    NUM_THREADS = 10

    def __init__(self) -> None:
        self.engines = Engines(IO())
        self.io = IO()
        self.thread_pool = ThreadPool(
            self.NUM_THREADS)
        self.thread_pool.spawn_threads()

    def generate_utterances(self, payload: Payload) -> None:
        try:
            payload.status = self._transcribe(payload)
        except Exception as e:
            print(e)

    def get_supported_engines(self) -> List[str]:
        return self.SUPPORTED_ENGINES

    ######################## PRIVATE METHODS ##################################

    def _transcribe(self, payload: Payload):
        self._execute_transcription_threads(payload)

    # --- Helpers

    def _execute_transcription_threads(self, payload: Payload) -> None:
        for data_file in payload.source.conversation.data_files:
            if self.io.get_file_extension(data_file.path) == "gb":
                self._load_from_raw_file(payload, data_file)
            else:
                self.thread_pool.add_task(
                    self._transcribe_watson_thread,
                    [payload, data_file], {})
        self.thread_pool.wait_completion()

    def _transcribe_watson_thread(
            self, payload: Payload, data_file: DataFile) -> None:
        try:
            print("transcribing", data_file.identifier)
            engine: WatsonEngine = self.engines.engine("watson")
            settings: GailBotSettings = payload.source.settings_profile.settings
            engine.configure(
                settings.engines.watson_engine.watson_api_key,
                settings.engines.watson_engine.watson_region,
                data_file.audio_path,
                settings.engines.watson_engine.watson_base_language_model,
                payload.source.hook.get_temp_directory_path()
            )
            utterances = engine.transcribe()
            print("utterances", len(utterances))
            payload.source_addons.utterances_map[data_file.identifier] =\
                utterances
            print("transcribed!", data_file.identifier)
        except Exception as e:
            print(e)

    def _load_from_raw_file(self, payload: Payload, data_file: DataFile):
        _, data = self.io.read(data_file.path)
        data = data.split('\n')
        utts = list()
        for line in data:
            label, text, start_time, end_time = line.split(',')
            utt = Utt(label, float(start_time), float(end_time), text)
            utts.append(utt)
        payload.source_addons.utterances_map[data_file.identifier] = utts

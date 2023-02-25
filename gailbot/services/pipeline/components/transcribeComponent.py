from gailbot.core.engines.engineManager import EngineManager
from typing import Any, List, Dict
from gailbot.core.pipeline import Component, ComponentState, ComponentResult
from gailbot.core.utils.general import (
    get_name
)
from gailbot.core.utils.logger import makelogger
import time
from ...converter.result import  ProcessingStats
from ...converter.payload import PayLoadObject
logger = makelogger("transcribeComponent")

""" TODO by Feb 24:
1. connect with engine and pipeline and test transcription
2. test functions to skip trancription for transcribedpayload
3. error handling mechanism - logging and return failed
"""
class TranscribeComponent(Component):
    def __init__(self):
        self.engine_manager = EngineManager()
    
    def __call__(self, dependency_output: Dict[str, str]) -> Any:
        payloads : List[PayLoadObject] = dependency_output["base"]

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
            payload.set_transcription_result(utt_map)
            payload.set_transcription_process_stats(stats)
            
        return ComponentResult(
            state=ComponentState.SUCCESS,
            result=payloads,
            runtime=time.time() - process_start_time
        )
        
      
    def _transcribe_payload(self, payload : PayLoadObject) -> None:
        # Parse the payload
        settings = payload.setting
        outdir = payload.workspace.transcribe_ws
        data_files = payload.data_files

        # Parse the settings
        engine_name = settings.engine_setting.engine
        engine_init_kwargs = settings.engine_setting.get_init_kwargs()
        engine_transcribe_kwargs = settings.engine_setting.get_transcribe_kwargs()
        # Transcribe behavior is different based on the type of the input
        # For example, if source contains video files, they should first be
        # extracted into audio files here.
        # If the source is being re-transcribed, then that should be parsed here.

        # Init engine
        if not self.engine_manager.is_engine(engine_name):
            raise Exception(f"Not an engine: {engine_name}")
        engine_init_kwargs.update({
            "workspace_dir": outdir
        })
        engine = self.engine_manager.init_engine(
            engine_name, **engine_init_kwargs)

        # Transcribe all of the data files
        utt_map = dict()
        for data_file in data_files:
            engine_transcribe_kwargs.update({
                "audio_path" : data_file,
            })
            utterances = engine.transcribe(**engine_transcribe_kwargs)
            utt_map[get_name(data_file)] = utterances

        return utt_map









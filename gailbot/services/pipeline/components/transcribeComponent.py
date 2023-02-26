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
    """ responsible for running the transcription process
    """
    def __init__(self):
        self.engine_manager = EngineManager()
    
    def __call__(self, dependency_output: Dict[str, str]) -> Any:
        """ extract the payload objects from the dependency_output,and 
            transcribe the datafiles in the payload object

        Args:
            dependency_output (Dict[str, str]): dependency output contains the
            result of the component and payload data
            
        Returns:
            Any: component result that stores the result state of transcription 
            and payloads data
        """
        logger.info(dependency_output)
        # TODO: improve the way of getting the dependency result
        payloads : List[PayLoadObject] = dependency_output["base"]
        process_start_time = time.time()
        for payload in payloads:
            # Parse payload
            if not payload.transcribed:
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
                payload.set_transcribed()
            
        return ComponentResult(
            state=ComponentState.SUCCESS,
            result=payloads,
            runtime=time.time() - process_start_time
        )
        
      
    def _transcribe_payload(self, payload : PayLoadObject) -> None:
        # Parse the payload
        transcribe_ws = payload.workspace.transcribe_ws
        data_files = payload.data_files

        # Parse the settings
        engine_name = payload.get_engine()
        engine_init_kwargs = payload.get_engine_init_setting()
        engine_transcribe_kwargs = payload.get_engine_transcribe_setting()
        
        # Transcribe behavior is different based on the type of the input
        # For example, if source contains video files, they should first be
        # extracted into audio files here.
        # If the source is being re-transcribed, then that should be parsed here.

        # Init engine
        if not self.engine_manager.is_engine(engine_name):
            raise Exception(f"Not an engine: {engine_name}")
        engine_init_kwargs.update({
            "workspace_dir": transcribe_ws
        })
        
        engine = self.engine_manager.init_engine(
            engine_name, **engine_init_kwargs)
        
        logger.info(engine)

        # Transcribe all of the data files
        utt_map = dict()
        for data_file in data_files:
            engine_transcribe_kwargs.update({
                "audio_path" : data_file,
            })
            utterances = engine.transcribe(**engine_transcribe_kwargs)
            utt_map[get_name(data_file)] = utterances

        return utt_map

    def __repr__(self):
        return "Transcription Component"






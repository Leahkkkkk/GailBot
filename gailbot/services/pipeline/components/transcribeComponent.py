from gailbot.core.engines.engineManager import EngineManager
from typing import Any, List, Dict
from gailbot.core.pipeline import Component, ComponentState, ComponentResult
from gailbot.core.utils.general import (
    get_name
)
from gailbot.core.utils.threads import ThreadPool
from gailbot.core.utils.logger import makelogger
import time
from ...converter.result import  ProcessingStats
from ...converter.payload import PayLoadObject
logger = makelogger("transcribeComponent")

class InvalidEngineError(Exception):
    def __init__(self, engine: str, *args) -> None:
        super().__init__(*args)
        self.engine = engine 
    def __repr__(self) -> str:
        return self.engine + "is not a valid engine"

""" TODO by Feb 24:
2. test functions to skip trancription for transcribedpayload
3. error handling mechanism - logging and return failed
"""
class TranscribeComponent(Component):
    """ responsible for running the transcription process
    """
    def __init__(self, num_thread : int = 5):
        self.engine_manager = EngineManager()
        self.num_thread = num_thread
    
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
        try:
            threadpool = ThreadPool(self.num_thread)
            tasks : Dict[int, PayLoadObject] = dict()
            logger.info(dependency_output)
            dep: ComponentResult = dependency_output["base"]
            payloads : List[PayLoadObject] = dep.result
            process_start_time = time.time()
        
            for payload in payloads:
                if not payload.transcribed:
                    # add the payload to the threadpool
                    key = threadpool.add_task(
                        fun=self._transcribe_payload, args=[payload])
                    tasks[key] = payload
                    logger.info(f"key: {key}")
            threadpool.wait_for_all_completion() 
            for key, payload in tasks.items():
                utt_map, stats = threadpool.get_task_result(key)
                payload.set_transcription_result(utt_map)
                payload.set_transcription_process_stats(stats)
                payload.set_transcribed()
        except Exception as e:
            logger.error(e)
            return ComponentResult(
                state=ComponentState.FAILED,
                result=payloads,
                runtime=time.time() - process_start_time
            )
        else:     
            return ComponentResult(
                state=ComponentState.SUCCESS,
                result=payloads,
                runtime=time.time() - process_start_time
            )
        
    def _transcribe_payload(self, payload : PayLoadObject) -> None:
        """ private function that transcribe each individual payload

        Args:
            payload (PayLoadObject): payload object that stores the datafiles 

        Raises:
            InvalidEngineError: 
            raised when the engine setting uses an invalid engine
            
        Returns:
            : return the transcribe result stored in a dictionary and the 
              process data
        """
        logger.info(f"Payload {payload} being transcribed")
        # Parse the payload
        start_time = time.time()
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
            raise InvalidEngineError(engine)
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

        end_time = time.time()
        stats = ProcessingStats(
            start_time=start_time,
            end_time = end_time,
            elapsed_time_sec= end_time - start_time
        )
        return utt_map, stats

    def __repr__(self):
        return "Transcription Component"






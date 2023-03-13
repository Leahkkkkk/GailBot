from gailbot.core.engines.engineManager import EngineManager
from typing import Any, List, Dict
from gailbot.core.pipeline import Component, ComponentState, ComponentResult
from gailbot.core.utils.general import get_name
from gailbot.core.utils.threads import ThreadPool
from gailbot.core.utils.logger import makelogger
import copy
import time
from ...converter.result import  ProcessingStats
from ...converter.payload import PayLoadObject
logger = makelogger("transcribeComponent")
""" TODO: Add to toml"""
NUM_THREAD = 5

class InvalidEngineError(Exception):
    def __init__(self, engine: str, *args) -> None:
        super().__init__(*args)
        self.engine = engine 
    def __repr__(self) -> str:
        return self.engine + "is not a valid engine"

class TranscribeComponent(Component):
    """ 
    Responsible for running the transcription process
    """
    def __init__(self, num_thread : int = 5):
        self.engine_manager = EngineManager()
        self.num_thread = num_thread
    
    def __call__(self, dependency_output: Dict[str, str]) -> Any:
        """ 
        Extracts the payload objects from the dependency_output and 
            transcribes the datafiles in the payload object

        Args:
            dependency_output (Dict[str, str]): dependency output contains the
            result of the component and payload data
            
        Returns:
            Any: component result that stores the result state of transcription 
            and payloads data
        """
        try:
            threadpool = ThreadPool(self.num_thread)
            threadkey_to_payload : Dict[int, PayLoadObject] = dict()
            logger.info(dependency_output)
            dep: ComponentResult = dependency_output["base"]
            payloads : List[PayLoadObject] = dep.result
            process_start_time = time.time()
        
            for payload in payloads:
                if not payload.transcribed:
                    # add the payload to the threadpool
                    key = threadpool.add_task(
                        task=self._transcribe_payload, args=[payload])
                    threadkey_to_payload[key] = payload
                    logger.info(f"key: {key}")
            for key, payload in threadkey_to_payload.items():
                assert threadpool.get_task_result(key)
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
        engine_init_kwargs.update({"workspace_dir": transcribe_ws})
        engine_transcribe_kwargs = payload.get_engine_transcribe_setting()
        logger.info(f"get transcribed setting engine_name: {engine_name} \
                      engine initialization setting {engine_init_kwargs} \
                      engine transcription setting {engine_transcribe_kwargs}")
       

        # Transcribe behavior is different based on the type of the input
        # For example, if source contains video files, they should first be
        # extracted into audio files here.
        # If the source is being re-transcribed, then that should be parsed here.

        # Init engine
        if not self.engine_manager.is_engine(engine_name):
            raise InvalidEngineError(engine_name)
        engine = self.engine_manager.init_engine(engine_name, **engine_init_kwargs)
                
        utt_map = dict()
        name_to_threadkey : Dict[str, int] = dict()
        threadpool = ThreadPool(NUM_THREAD)
        
        for file in data_files:
            transcribe_kwargs = copy.deepcopy(engine_transcribe_kwargs)
            transcribe_kwargs.update({"audio_path": file})
            name_to_threadkey[file] = threadpool.add_task(
                task = engine.transcribe, kwargs = transcribe_kwargs) 
        try:
            for file in data_files:
                utt_map[get_name(file)] = \
                    threadpool.get_task_result(name_to_threadkey[file])
        except Exception as e:
            logger.error(f"Failed to transcribed {len(data_files)} file in parallel due to the error {e}")
            return False
    
    
        # logger.info(engine)

        # # Transcribe all of the data files
        # utt_map = dict()
        # for data_file in data_files:
        #     engine_transcribe_kwargs.update({
        #         "audio_path" : data_file,
        #     })
        #     utterances = engine.transcribe(**engine_transcribe_kwargs)
        #     utt_map[get_name(data_file)] = utterances

        end_time = time.time()
        stats = ProcessingStats(
            start_time=start_time,
            end_time = end_time,
            elapsed_time_sec= end_time - start_time
        )
        payload.set_transcription_result(utt_map)
        payload.set_format_process_stats(stats)
        return True
    
    
    def transcribe_single_file(self, engine, init_kwargs, transcribe_kwargs):
        """
        Transcribes a file with the given engine

        Args:
            engine: engine to perform the transcription
            init_kwargs: arguments with which to initialize the engine
            transcribe_kwargs: arguments with which to initialize the transcription
        """
        engine = self.engine_manager.init_engine(engine, **init_kwargs)
        utterances = engine.transcribe(**transcribe_kwargs)
        return utterances
        
        
    def __repr__(self):
        return "Transcription Component"






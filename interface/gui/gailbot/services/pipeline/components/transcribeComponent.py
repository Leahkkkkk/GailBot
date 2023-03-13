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
from gailbot.configs import service_config_loader
logger = makelogger("transcribeComponent")
""" TODO: Add to toml"""
DEFULT_NUM_THREAD = service_config_loader().thread.transcriber_num_threads

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
    def __init__(self, num_thread : int = DEFULT_NUM_THREAD):
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
        init_kwargs = payload.get_engine_init_setting()
        init_kwargs.update({"workspace_dir": transcribe_ws})
        transcribe_kwargs = payload.get_engine_transcribe_setting()
        logger.info(f"get transcribed setting engine_name: {engine_name} \
                      engine initialization setting {init_kwargs} \
                      engine transcription setting {transcribe_kwargs}")
        
        # Init engine
        if not self.engine_manager.is_engine(engine_name):
            raise InvalidEngineError(engine_name)
                
        utt_map = dict()
        threadpool = ThreadPool(DEFULT_NUM_THREAD)
        
        for file in data_files:
            transcribe_kwargs = copy.deepcopy(transcribe_kwargs)
            transcribe_kwargs.update({"audio_path": file})
            filename = threadpool.add_task( 
                                            self.transcribe_single_file, 
                                            kwargs= {"engine_name" : engine_name,
                                                    "init_kwargs" : init_kwargs, 
                                                    "transcribe_kwargs": transcribe_kwargs},
                                            key = get_name(file)) 
            assert filename == get_name(file)
        try:
            for file in data_files:
                utt_map[get_name(file)] = \
                    threadpool.get_task_result(get_name(file))
                    
        except Exception as e:
            logger.error(f"Failed to transcribed {len(data_files)} file in parallel due to the error {e}")
            return False

        end_time = time.time()
        stats = ProcessingStats(
            start_time=start_time,
            end_time = end_time,
            elapsed_time_sec= end_time - start_time
        )
        payload.set_transcription_result(utt_map)
        payload.set_format_process_stats(stats)
        return True
    
    
    def transcribe_single_file(self, engine_name, init_kwargs, transcribe_kwargs):
        """
        Transcribes a file with the given engine

        Args:
            engine: engine to perform the transcription
            init_kwargs: arguments with which to initialize the engine
            transcribe_kwargs: arguments with which to initialize the transcription
        """
        engine = self.engine_manager.init_engine(engine_name, **init_kwargs)
        utterances = engine.transcribe(**transcribe_kwargs)
        return utterances
        
        
    def __repr__(self):
        return "Transcription Component"






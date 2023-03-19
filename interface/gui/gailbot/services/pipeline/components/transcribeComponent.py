# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-03-15 10:31:49
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-03-15 12:22:53
from gailbot.core.engines.engineManager import EngineManager
from dataclasses import dataclass
from typing import Any, List, Dict
from gailbot.core.pipeline import Component, ComponentState, ComponentResult
from gailbot.core.utils.general import get_name
from gailbot.core.utils.threads import ThreadPool
from gailbot.core.utils.logger import makelogger

import copy
import time
from ...converter.result import  ProcessingStats
from ...converter.payload import PayLoadObject
from ..components.progress import ProgressMessage
from gailbot.configs import service_config_loader
logger = makelogger("transcribeComponent")

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
        self.engine_manager = EngineManager() # a wrapper class for managing
                                              # and transcribing payload using engine
        self.num_thread = num_thread

    def __call__(self, dependency_output: Dict[str, ComponentResult]) -> Any:
        """
            Extracts the payload objects from the dependency_output and
            transcribes the datafiles in the payload object

        Args:
            dependency_output (Dict[str, ComponentResult]): dependency output contains the
            result of the component and payload data

        Returns:
            Any: component result that stores the result state of transcription
            and payloads data
        """
        try:
            threadpool = ThreadPool(self.num_thread)
            logger.info(dependency_output)
            dep: ComponentResult = dependency_output["base"]
            # get the list of payloads from dependency_output
            payloads : List[PayLoadObject] = dep.result
            process_start_time = time.time()
            
            for payload in payloads:
                self.emit_progress(payload, ProgressMessage.Waiting)
                if not payload.transcribed:
                    # add the payload to the threadpool
                    key = threadpool.add_task(
                        task = self._transcribe_one_payload,
                        args = [payload],
                        key  = payload.name)
                    assert key == payload.name
                    logger.info(f"payload {payload.name} is added to the threadpool, the key is {key}")
                else:
                    self.emit_progress(payload, ProgressMessage.Finished)
           
           
            # get the result from the thread pool
            for payload in payloads:
                if not payload.transcribed:
                    if not threadpool.get_task_result(payload.name):
                        payload.set_failure()
                    else:
                        payload.set_transcribed()
        
        except Exception as e:
            logger.error(f"Transcription failure {e}", exc_info=e)
            threadpool.shutdown(wait=True)
            return ComponentResult(
                state=ComponentState.FAILED,
                result=payloads,
                runtime=time.time() - process_start_time
            )
        else:
            threadpool.shutdown(cancel_futures=True)
            return ComponentResult(
                state=ComponentState.SUCCESS,
                result=payloads,
                runtime=time.time() - process_start_time
            )

    def _transcribe_one_payload(self, payload : PayLoadObject) -> bool:
        """ private function that transcribe each individual payload

        Args:
            payload (PayLoadObject): payload object that stores the datafiles

        Raises:
            InvalidEngineError:
            raised when the engine setting uses an invalid engine

        Returns:
            : return True if the payload is transcribed successfully , false
              otherwise
        """
        try:
            logger.info(f"Payload {payload} being transcribed")
            self.emit_progress(payload, "Start transcribing")
            
            # Parse the payload
            start_time = time.time()
            transcribe_ws = payload.workspace.transcribe_ws
            data_files = payload.data_files
            num_file = len(data_files)
            
            # Parse the settings
            engine_name = payload.get_engine()
            init_kwargs = payload.get_engine_init_setting()
            transcribe_kwargs = payload.get_engine_transcribe_setting()
            logger.info(f"get transcribed setting engine_name: {engine_name} \
                          engine initialization setting {init_kwargs} \
                          engine transcription setting {transcribe_kwargs}")

            # check for valid engine engine
            if not self.engine_manager.is_engine(engine_name):
                raise InvalidEngineError(engine_name)
            
            # start to use engine to transcribe files in the payload
            utt_map = dict()
            threadpool = ThreadPool(DEFULT_NUM_THREAD)
            
            # adding the task to transcribe individual file to the thread
            self.emit_progress(payload, "Adding Task")
            for idx, file in enumerate(data_files):
                transcribe_kwargs = copy.deepcopy(transcribe_kwargs)
                transcribe_kwargs.update({"audio_path": file, "payload_workspace": transcribe_ws})
                filename = threadpool.add_task(
                    self.transcribe_single_file,
                    kwargs= {"engine_name" : engine_name,
                            "init_kwargs" : init_kwargs,
                            "transcribe_kwargs": transcribe_kwargs},
                    key = get_name(file))
                assert filename == get_name(file)
       
            # start getting the result of the file
            self.emit_progress(payload, ProgressMessage.Transcribing)
            """ TODO: consider adding a while loop to watch for progress 
                     instead of a for loop, if we want better message """
            for idx, file in enumerate (data_files):
                utt_map[get_name(file)] = \
                    threadpool.get_task_result(get_name(file))
                self.emit_progress(payload, f"{idx + 1}/{num_file} files transcribed")
           
            time.sleep(1)
            
            # if the transcription result is returned successfully
            end_time = time.time()
            stats = ProcessingStats(
                start_time=start_time,
                end_time = end_time,
                elapsed_time_sec= end_time - start_time
            )
            
            assert payload.set_transcription_result(utt_map)
            assert payload.set_transcription_process_stats(stats)      
            self.emit_progress(payload, ProgressMessage.Transcribed)
             
        except Exception as e:
            payload.progress_display(payload, ProgressMessage.Error)
            logger.error(f"Failed to transcribed {len(data_files)} file in parallel due to the error {e}", exc_info=e)
            return False
        
        else: 
            return True


    def transcribe_single_file(self, engine_name, init_kwargs, transcribe_kwargs)  -> List[Dict[str, str]]:
        """
        Transcribes a file with the given engine

        Args:
            engine: engine to perform the transcription
            init_kwargs: arguments with which to initialize the engine
            transcribe_kwargs: arguments with which to initialize the transcription

        Return:
            the utterances result
        """
        engine = self.engine_manager.init_engine(engine_name, **init_kwargs)
        utterances = engine.transcribe(**transcribe_kwargs)
        return utterances

    def __repr__(self):
        return "Transcription Component"

    def emit_progress(self, payload: PayLoadObject, msg: str):
        if payload.progress_display:
            payload.progress_display(msg)



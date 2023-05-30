# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:13:08
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 11:53:04
# Standard imports
from typing import Callable, Any, List, Dict
import sys
# Local imports
# Third party imports
from copy import deepcopy
from ibm_watson.websocket import RecognizeCallback
from gailbot.core.utils.logger import makelogger

logger = makelogger("callback")

class WatsonException(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)
        self.msg = msg 
    
class CustomWatsonCallbacks(RecognizeCallback):
    """
    Extends the watson callback class to allow custom callbacks to be executed
    when an event occurs through the lifecycle of the websocket connection.

    Inherits:
        (RecognizeCallback)
    """
    def __init__(self) -> None:
        """
        Args:
            closure (List):
                User object that is passed as the first parameter of every
                callback during the lifecycle of the websocket connection.
        """
        self.closure = self._init_closure()

    def reset(self) -> None:
        logger.info("reset recognize callback")
        self.closure = self._init_closure()

    def get_results(self) -> Dict:
        logger.info("on get result")
        return deepcopy(self.closure)

    def on_transcription(self, transcript: List) -> None:
        """
        Called after the service returns the final result for the transcription.
        """
        logger.info("on transcription")
        try:
            closure = self.closure
            closure["callback_status"]["on_transcription"] = True
            closure["results"]["transcript"].append(transcript)
        except Exception as e:
            logger.error(e, exc_info=e)

    def on_connected(self) -> None:
        """
        Called when a Websocket connection was made
        """
        logger.info("connected to watson")
        try:
            closure = self.closure
            closure["callback_status"]["on_connected"] = True
        except Exception as e:            
           logger.error(e, exc_info=e) 
    
    def on_error(self, error: str) -> None:
        """
        Called when there is an error in the Websocket connection.
        """
        logger.error(f"get error {error}", exc_info=error)

        closure = self.closure
        closure["callback_status"]["on_error"] = True
        closure["results"]["error"] = error
        raise WatsonException(error)

    def on_inactivity_timeout(self, error: str) -> None:
        """
        Called when there is an inactivity timeout.
        """      
        logger.info("inactivity time out") 
        try:
            closure = self.closure
            closure["callback_status"]["on_inactivity_timeout"] = True
            closure["results"]["error"] = error
        except Exception as e:
            logger.error(f"timeout error {e}", exc_info=e)

    def on_listening(self) -> None:
        """
        Called when the service is listening for audio.
        """   
        logger.info("watson is listening")   
        try:
            closure = self.closure
            closure["callback_status"]["on_listening"] = True
        except Exception as e:
            logger.error(f"on listening error {e}", exc_info=e)

    def on_hypothesis(self, hypothesis: str) -> None:
        """
        Called when an interim result is received.
        """
        logger.info(f"on hypothesis {hypothesis}")
        try:
            closure = self.closure
            closure["callback_status"]["on_hypothesis"] = True
        except Exception as e:
            logger.error(f"on hypothesis error {e}", exc_info=e)

    def on_data(self, data: Dict) -> None:
        """
        Called when the service returns results. The data is returned unparsed.
        """
        logger.info(f"watson returned the results")
        try:
            closure = self.closure
            closure["callback_status"]["on_data"] = True
            closure["results"]["data"].append(data)
        except Exception as e:
            logger.error(f"on data error {e}", exc_info=e)

    def on_close(self) -> None:
        """
        Called when the Websocket connection is closed
        """
        logger.info("on close")
        try:
            closure = self.closure
            closure["callback_status"]["on_close"] = True
        except Exception as e:
            logger.error(f"on close error {e}", exc_info=e)

    def _init_closure(self) -> Dict:      
        return  {
                "callback_status": {
                    "on_transcription": False,
                    "on_connected": False,
                    "on_error": False,
                    "on_inactivity_timeout": False,
                    "on_listening": False,
                    "on_hypothesis": False,
                    "on_data": False,
                    "on_close": False
                },
                "results": {
                    "error": None,
                    "transcript": list(),
                    "hypothesis": list(),
                    "data": list()
                }
            }

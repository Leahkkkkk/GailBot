# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:13:08
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 11:53:04
# Standard imports
from typing import Callable, Any, List, Dict
# Local imports
# Third party imports
from copy import deepcopy
from ibm_watson.websocket import RecognizeCallback


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
        self.callback_closure = self._init_closure()

    def reset(self) -> None:
        self.callback_closure = self._init_closure()

    def get_results(self) -> Dict:
        return deepcopy(self.callback_closure)

    def on_transcription(self, transcript: List) -> None:
        """
        Called after the service returns the final result for the transcription.
        """
        try:
            closure = self.closure
            closure[0]["callback_status"]["on_transcription"] = True
            closure[0]["results"]["transcript"].append(transcript)
        except:
            pass

    def on_connected(self) -> None:
        """
        Called when a Websocket connection was made
        """
        try:
            closure = self.closure
            closure[0]["callback_status"]["on_connected"] = True
        except:
            pass

    def on_error(self, error: str) -> None:
        """
        Called when there is an error in the Websocket connection.
        """
        try:
            closure = self.closure
            closure[0]["callback_status"]["on_error"] = True
            closure[0]["results"]["error"] = error
        except:
            pass

    def on_inactivity_timeout(self, error: str) -> None:
        """
        Called when there is an inactivity timeout.
        """
        try:
            closure = self.closure
            closure[0]["callback_status"]["on_inactivity_timeout"] = True
            closure[0]["results"]["error"] = error
        except:
            pass

    def on_listening(self) -> None:
        """
        Called when the service is listening for audio.
        """
        try:
            closure = self.closure
            closure[0]["callback_status"]["on_listening"] = True
        except:
            pass

    def on_hypothesis(self, hypothesis: str) -> None:
        """
        Called when an interim result is received.
        """
        try:
            closure = self.closure
            closure[0]["callback_status"]["on_hypothesis"] = True
        except:
            pass

    def on_data(self, data: Dict) -> None:
        """
        Called when the service returns results. The data is returned unparsed.
        """
        try:
            closure = self.closure
            closure[0]["callback_status"]["on_data"] = True
            closure[0]["results"]["data"].append(data)
        except:
            pass

    def on_close(self) -> None:
        """
        Called when the Websocket connection is closed
        """
        try:
            closure = self.closure
            closure[0]["callback_status"]["on_close"] = True
        except:
            pass

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

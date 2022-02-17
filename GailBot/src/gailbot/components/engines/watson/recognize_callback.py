# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:13:08
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-05 17:21:20
# Standard imports
from typing import Callable, Any, List, Dict
# Local imports
# Third party imports
from ibm_watson.websocket import RecognizeCallback


class customWatsonCallbacks(RecognizeCallback):
    """
    Extends the watson callback class to allow custom callbacks to be executed
    when an event occurs through the lifecycle of the websocket connection.

    Inherits:
        (RecognizeCallback)
    """

    def __init__(self, closure: List) -> None:
        """
        Args:
            closure (List):
                User object that is passed as the first parameter of every
                callback during the lifecycle of the websocket connection.
        """
        self.closure = closure
        self.on_transcription_callback = lambda *args: None
        self.on_connected_callback = lambda *args: None
        self.on_error_callback = lambda *args: None
        self.on_inactivity_timeout_callback = lambda *args: None
        self.on_listening_callback = lambda *args: None
        self.on_hypothesis_callback = lambda *args: None
        self.on_data_callback = lambda *args: None
        self.on_close_callback = lambda *args: None

    # SETTERS

    def set_on_transcription_callback(self,
                                      callback: Callable[[List[Any], List], None]) -> None:
        """
        Called after the service returns the final result for the transcription.

        Args:
            (Callable[[List[Any], List],None]):
                The first argument is the closure while the second is the
                transcript returned by the service.
        """
        self.on_transcription_callback = callback

    def set_on_connected_callback(self,
                                  callback: Callable[[List[Any]], None]) -> None:
        """
        Called when a Websocket connection was made

        Args:
            (Callable[[List[Any]],None]): The first argument is the closure.
        """
        self.on_connected_callback = callback

    def set_on_error_callback(self,
                              callback: Callable[[List[Any], str], None]) -> None:
        """
        Called when there is an error in the Websocket connection.

        Args:
            (Callable[[List[Any],str], None]):
                The first argument is the closure while the second is the error.
        """
        self.on_error_callback = callback

    def set_on_inactivity_timeout(self,
                                  callback: Callable[[List[Any], str], None]) -> None:
        """
        Called when there is an inactivity timeout.

        Args:
            (Callable[[List[Any],str], None]):
                The first argument is the closure while the second is the error.
        """
        self.on_inactivity_timeout_callback = callback

    def set_on_listening_callback(self,
                                  callback: Callable[[List[Any]], None]) -> None:
        """
        Called when the service is listening for audio.

        Args:
            (Callable[[List[Any]], None]): The first argument is the closure.
        """
        self.on_listening_callback = callback

    def set_on_hypothesis_callback(self,
                                   callback: Callable[[List[Any], str], None]) -> None:
        """
        Called when an interim result is received.

        Args:
            (Callable[[List[Any], str], None]):
                The first argument is the closure while the second is the
                hypothesis.
        """
        self.on_hypothesis_callback = callback

    def set_on_data_callback(self,
                             callback: Callable[[List[Any], Dict], None]) -> None:
        """
        Called when the service returns results. The data is returned unparsed.

        Args:
            (Callable[[List[Any], Dict], None]):
                The first argument is the closure while the second is the
                data dictionary.
        """
        self.on_data_callback = callback

    def set_on_close_callback(self,
                              callback: Callable[[List[Any]], None]) -> None:
        """
        Called when the Websocket connection is closed

        Args:
            (Callable[[List[Any]], None]): The first argument is the closure.
        """
        self.on_close_callback = callback

    # Others

    def on_transcription(self, transcript: List) -> None:
        """
        Called after the service returns the final result for the transcription.
        """
        try:
            self.on_transcription_callback(self.closure, transcript)
        except:
            pass

    def on_connected(self) -> None:
        """
        Called when a Websocket connection was made
        """
        try:
            self.on_connected_callback(self.closure)
        except:
            pass

    def on_error(self, error: str) -> None:
        """
        Called when there is an error in the Websocket connection.
        """
        try:
            self.on_error_callback(self.closure, error)
        except:
            pass

    def on_inactivity_timeout(self, error: str) -> None:
        """
        Called when there is an inactivity timeout.
        """
        try:
            self.on_inactivity_timeout_callback(self.closure, error)
        except:
            pass

    def on_listening(self) -> None:
        """
        Called when the service is listening for audio.
        """
        try:
            self.on_listening_callback()
        except:
            pass

    def on_hypothesis(self, hypothesis: str) -> None:
        """
        Called when an interim result is received.
        """
        try:
            self.on_hypothesis_callback(self.closure, hypothesis)
        except:
            pass

    def on_data(self, data: Dict) -> None:
        """
        Called when the service returns results. The data is returned unparsed.
        """
        try:
            self.on_data_callback(self.closure, data)
        except:
            pass

    def on_close(self) -> None:
        """
        Called when the Websocket connection is closed
        """
        try:
            self.on_close_callback(self.closure)
        except:
            pass

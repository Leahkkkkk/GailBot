# Standard library imports
from typing import Any, Dict, Tuple, Union
from queue import Queue, Empty

from autobahn import websocket

# Local imports
from .WS_models import WebsocketProtocolModel, WSProtocolAttributes
# Third party imports
from typing import Callable
from autobahn.twisted.websocket import WebSocketClientProtocol


class WSInterfaceProtocol(WebSocketClientProtocol):
    """
    Client protocol that establishes how to communicate with a server at
    different states of a websocket connection.

    Inherits:
        (WebSockerClientProtocol)
    """
    # Codes that can be sent with a send_close function call.
    CLOSE_CODES = ("1000", "1001", "1002", "1003",
                   "1007", "1008", "1009", "1010")

    def __init__(self):
        """
        Params:
            factory (WSInterfaceFactory): Factory that this protocol is being
                                        used by.
            data_queue (Queue): Queue containing data associated with each task.
            task_data (Any): The data associated with this particular task.
            callbacks (Dict): Mapping of str to callbacks for the protocol.
                        Must contain the keys:
                            1. on_connect
                            2. on_connecting
                            3. on_open
                            4. on_message
                            5. on_close
        """
        super().__init__()
        # Params
        self.factory = None
        self.data_queue = None
        self.task_data = None
        self.callbacks = {
            "on_connect": lambda *args, **kwargs: None,
            "on_connecting": lambda *args, **kwargs: None,
            "on_open": lambda *args, **kwargs: None,
            "on_message": lambda *args, **kwargs: None,
            "on_close": lambda *args, **kwargs: None}

    ########################### PUBLIC METHODS ################################

    def set_callback(self, callback_type: str,
                     callback: Callable[[WebsocketProtocolModel], None]) -> bool:
        """
        Set a callback required by this protocol.

        Args:
            callback_type (str): Name of the callback. Must be one of:
                            1. on_connect
                            2. on_connecting
                            3. on_open
                            4. on_message
                            5. on_close
            callback (Callable[[WebsocketProtocolModel], None])

        Returns:
            (bool): True if set successfully. False otherwise.
        """
        # Must be a type of callback
        if not callback_type in self.callbacks.keys():
            return False
        self.callbacks[callback_type] = callback
        return True

    def set_data_queue(self, data_queue: Queue) -> bool:
        """
        Set the data queue associated with the task for this protocol.
        This is mainly used to mark the task as completed.

        Args:
            data_queue (Queue): Queue this task is a part of.

        Returns:
             (bool): True if set successfully. False otherwise.
        """
        self.data_queue = data_queue
        return True

    def set_task_data(self, task_data: Any) -> bool:
        """
        Set the task associated with this task.

        Args:
            task_data (Any): Data associated with this task.

        Returns:
             (bool): True if set successfully. False otherwise.
        """
        self.task_data = task_data
        return True

    def set_factory_reference(self, factory: Any) -> bool:
        """
        Set a reference to the factory that this protocol is being used by.

        Args:
            factory (Any): Pointer to factory this protocol is being used by.

        Returns:
             (bool): True if set successfully. False otherwise.
        """
        self.factory = factory
        return True

    ########################### PRIVATE METHODS ################################

    # Callbacks
    def onConnect(self, response: Union[websocket.ConnectionRequest,
                                        websocket.ConnectionResponse]) -> None:
        """
        Called when first connected to the server.
        Sends close if the callback throws an uncaught exception.

        Args:
            response (Union[websocket.ConnectionRequest, websocket.ConnectionResponse]):
                    Response returned by the server.
        """
        success, _ = self._execute_callback(self.callbacks["on_connect"],
                                            self._create_protocol_model({"response": response}))
        # Close the connection if unsuccessful.
        if not success:
            self._send_close("1000")

    def onConnecting(self, response: websocket.types.TransportDetails) -> None:
        """
        Called when first connecting to the server.
        Sends close if the callback throws an uncaught exception.

        Args:
            response (Any): Response returned by the server.
        """
        success, _ = self._execute_callback(self.callbacks["on_connecting"],
                                            self._create_protocol_model({"response": response}))
        # Close the connection if unsuccessful.
        if not success:
            self._send_close("1000")

    def onOpen(self) -> None:
        """
        Called when the connection is first opened with the server.
        """
        success, _ = self._execute_callback(self.callbacks["on_open"],
                                            self._create_protocol_model({}))
        # Close the connection if unsuccessful.
        if not success:
            self._send_close("1000")

    def onMessage(self,  payload: bytes, is_binary: bool) -> None:
        """
        Called when a message is received by the server.
        Sends close if the callback throws an uncaught exception.

        Args:
            payload (bytes): Data returned by the server.
            is_binary (bool) : True if the data returned is in binary form.
                                False otherwise.
        """
        success, _ = self._execute_callback(self.callbacks["on_message"],
                                            self._create_protocol_model({
                                                "payload": payload, "is_binary": is_binary}))
        # Close the connection if unsuccessful.
        if not success:
            self._send_close("1000")

    def onClose(self, was_clean: bool, code: int, reason: str) -> None:
        """
        Called when the connection with the server is closed.
        Marks the task as completed.

        Args:
            was_clean (bool): True if the connection was cleanly closed.
                            False otherwise.
            code (int): Closing code returned by the server.
            reason (str): Reason the server was closes
        """
        self._execute_callback(self.callbacks["on_close"],
                               self._create_protocol_model({
                                   "was_clean": was_clean, "code": code, "reason": reason}))
        # Marking task as completed
        self.data_queue.task_done()
        # Restarting the factory if the queue is not fully processed.
        if not self.data_queue.empty():
            self.factory.restart_factory()

    # Wrappers for sending messages

    # Protocol Model methods
    def _send_close(self, code: str, reason: str = None) -> bool:
        """
        Method provided with callbacks as part of WebsocketProtocolModel.
        Allows the connection with the server to close with the given code.

        Args:
            code (str): Code with which the connection with the server is closed.
                    Available codes are:
                    ("1000", "1001","1002","1003","1007","1008","1009","1010")
            reason (str): Reason for sending close.

        Returns:
            (bool): True if successfully sent. False otherwise.
        """
        if code not in self.CLOSE_CODES:
            return False
        self.sendClose(int(code), reason)
        return True

    def _send_message(self, payload: bytes, is_binary: bool) -> bool:
        """
        Method provided with callbacks as part of WebsocketProtocolModel.
        Allows a message to be sent to the server.

        Args:
            payload (bytes): Data being sent as part of the message.
            is_binary (bool): True if the data is in binary form. False otherwise.

        Returns:
            (bool): True if successfully sent. False otherwise.
        """
        # Encode the payload appropriately
        try:
            if type(payload) == str:
                payload = payload.encode("utf-8")
            self.sendMessage(payload)
            return True
        except:
            return False

    def _send_ping(self, payload: bytes) -> bool:
        """
        Method provided with callbacks as part of WebsocketProtocolModel.
        Send a websocket ping to the peer.

        Args:
            payload (bytes): Data to be sent with the ping.

        Returns:
            (bool): True if successfully sent. False otherwise.
        """
        try:
            if type(payload) == str:
                payload = payload.encode("utf-8")
            self.sendPing(payload)
            return True
        except:
            return False

    def _send_pong(self, payload:  bytes) -> bool:
        """
        Method provided with callbacks as part of WebsocketProtocolModel.
        Send a websocket pong to the peer.

        Args:
            payload (bytes): Data to be sent with the pong.

        Returns:
            (bool): True if successfully sent. False otherwise.
        """
        try:
            if type(payload) == str:
                payload = payload.encode("utf-8")
            self.sendPong(payload)
            return True
        except:
            return False

    # Others

    def _execute_callback(self, callback: Callable, data: Dict)\
            -> Tuple[bool, Any]:
        """
        Executes the given callback safely.

        Args:
            callback (Callable): Method to execute.
            data (Dict): Data to be passed as part of the method.

        Returns:
            (Tuple[bool,Any]): True + data returned by callback. if successful.
                                False + None if unsuccessful.
        """
        try:
            return (True, callback(data))
        except:
            return (False, None)

    def _create_protocol_model(self, callback_data: Dict) \
            -> WebsocketProtocolModel:
        """
        Uses the data returned by the callback to create an instance of
        WebsocketProtocolModel

        Args:
            callback_data (Dict): Data returned by a callback.

        Returns:
            (WebsocketProtocolModel)
        """
        protocol_model = WebsocketProtocolModel()
        protocol_model.set(
            WSProtocolAttributes.send_close_callback, self._send_close)
        protocol_model.set(
            WSProtocolAttributes.send_message_callback, self._send_message)
        protocol_model.set(
            WSProtocolAttributes.send_ping_callback, self._send_ping)
        protocol_model.set(
            WSProtocolAttributes.send_pong_callback, self._send_pong)
        protocol_model.set(
            WSProtocolAttributes.callback_return_data, callback_data)
        protocol_model.set(
            WSProtocolAttributes.callback_data_parameter, self.task_data)
        return protocol_model

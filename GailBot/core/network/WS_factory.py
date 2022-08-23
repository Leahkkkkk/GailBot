# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-23 10:02:56
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-23 10:39:34
# Standard library imports
from typing import Dict, Callable, Any
from queue import Queue, Empty
# Local imports
from .WS_protocol import WSInterfaceProtocol
from .WS_models import WebsocketProtocolModel
# Third party imports
from autobahn.twisted.websocket import WebSocketClientFactory, connectWS
from twisted.internet import ssl, reactor
import validators


class WSInterfaceFactory(WebSocketClientFactory):
    """
    Factory responsible for spawning instancedata_parameters of a websocket client protocol
    to connect to the specified url using a Websocket connection, and processing
    all items in the data queue through the connection.

    Inheritance:
        (WebSocketClientFactory)
    """

    def __init__(self, url: str, headers: Dict) -> None:
        """
        Args:
            url (str): Url of the server with which to establish the connection.
            headers (Dict): Header data to be passed to the server.

        Params:
            url (str): Url of the server with which to establish the connection.
            headers (Dict): Header data to be passed to the server.
            protocol (WSInterfaceProtocol): Protcol used to define interaction.
            data_queue (Queue): Queue containing the data associated with
                                each task.
            context_factory (ssl.ClientContextFactory)
            protocol_callbacks (Dict): Mapping of callback types to method.
        """
        super().__init__(url=url, headers=headers)
        # Factory params
        self.url = url
        self.headers = headers
        self.protocol = None
        self.data_queue = Queue(0)
        self.context_factory = None
        self.protocol_callbacks = {
            "on_connect": lambda *args, **kwargs: None,
            "on_connecting": lambda *args, **kwargs: None,
            "on_open": lambda *args, **kwargs: None,
            "on_message": lambda *args, **kwargs: None,
            "on_close": lambda *args, **kwargs: None}
        # Setting protocol options
        self.setProtocolOptions(
            utf8validateIncoming=True,
            applyMask=True,
            maxFramePayloadSize=0,
            maxMessagePayloadSize=0,
            autoFragmentSize=0,
            failByDrop=True,
            echoCloseCodeReason=False,
            openHandshakeTimeout=10,
            closeHandshakeTimeout=10,
            tcpNoDelay=True,
            autoPingInterval=5,
            autoPingTimeout=5,
            autoPingSize=4,
            version=18,
            acceptMaskedServerFrames=False,
            maskClientFrames=True,
            serverConnectionDropTimeout=1)

    ################################# SETTERS ###############################

    def set_protocol(self, protocol: WSInterfaceProtocol) -> bool:
        """
        Sets the protocol for this factory. The protocol defines how the
        interaction occurs when a connection with the server is established.

        Args:
            protocol (WSInterfaceProtocol)

        Returns:
            (bool): True if set successfully. False otherwise.
        """
        self.protocol = protocol
        return True

    def set_data_queue(self, data_queue: Queue) -> bool:
        """
        Sets the data queue that contains data associated with each task.

        Args:
            data_queue (Queue): Queue containing the data associated with
                                each task.

        Returns:
            (bool): True if set successfully. False otherwise.
        """
        self.data_queue = data_queue
        return True

    def set_context_factory(self, context_factory: ssl.ClientContextFactory) \
            -> bool:
        """
        Sets the client context factory for the secure socket layer.

        Args:
            context_factory (ssl.ClientContextFactory)

        Returns:
            (bool): True if set successfully. False otherwise.
        """
        self.context_factory = context_factory
        return True

    def set_protocol_callback(self, callback_type: str,
                              callback: Callable[[WebsocketProtocolModel], None]) -> bool:
        """
        Set a callback associated with the protocol.

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
        # Must be a valid callback.
        if not callback_type in self.protocol_callbacks.keys():
            return False
        self.protocol_callbacks[callback_type] = callback
        return True

    ################################# GETTERS ################################

    def get_factory_configurations(self) -> Dict:
        """
        Get the different configurations associated with the server.

        Returns:
            (Dict): Dictionary containing the factory configurations.
        """
        return {
            "is_secure": self.isSecure,
            "url": self.url,
            "context_factory": self.context_factory,
            "data_queue": self.data_queue
        }

    def is_ready(self) -> bool:
        """
        Check whether the server is ready to connect.

        Returns:
            (bool): True if the factory is ready. False otherwise.
        """
        return self._is_ready_for_connection()

    ########################## PUBLIC METHODS ################################

    def restart_factory(self) -> bool:
        """
        Restart the factory if the data queue has not been fully processed.

        Returns:
            (bool): True if successfully restarted. False otherwise.
        """
        try:
            connectWS(self, self.context_factory)
            return True
        except:
            return False

    ######################### PRIVATE METHODS ###############################

    def buildProtocol(self, addr: Any) -> Any:
        try:
            data = self.data_queue.get_nowait()
            protocol = self.protocol()
            protocol.set_data_queue(self.data_queue)
            protocol.set_task_data(data)
            protocol.set_factory_reference(self)
            for name, callback in self.protocol_callbacks.items():
                protocol.set_callback(name, callback)
            return protocol
        except Empty:
            return

    def _is_ready_for_connection(self) -> bool:
        """
        Checks whether the factory is ready to connect.
        Checks for valid url, non empty data queue, and a defined protocol.

        Returns:
            (bool): True if ready to connect. False otherwise.
        """
        return self._is_valid_url(self.url) and \
            not self.data_queue.empty() and  \
            self.protocol

    def _is_valid_url(self, url: str) -> bool:
        """
        Checks if the url is valid.

        Args:
            url (str):

        Returns:
            (bool): True if the url is in the correct format. False otherwise.
        """
        # TODO: Validation function is not working for certain urls (wss:)
        # Need to change this later. Validators does not check for wss url's.
        # return validators.url(url)
        return url != ""

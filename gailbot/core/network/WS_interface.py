# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-23 10:02:56
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-23 10:40:00
# Standard library imports
from threading import Thread
from typing import Callable, Dict, List
# Third party imports
from queue import Queue
from autobahn.twisted.websocket import connectWS
from twisted.internet import reactor, ssl
# Local imports
from .WS_protocol import WSInterfaceProtocol
from .WS_models import WebsocketProtocolModel
from .WS_factory import WSInterfaceFactory
from gailbot.utils.threads import ThreadPool

class WSInterface:
    """
    Responsible for establishing and managing Websocket client connections
    with the given url using a WebSocket client factory and a
    websocket client protocol
    """

    def __init__(self, url: str, headers: Dict) -> None:
        """
        Args:
            url (str): Url of the server with which to establish the connection.
            headers (Dict): Header data to be passed to the server.

        Params:
            protocol (WSInterfaceProtocol): Protcol used to define interaction.
            factory (WSInterfaceFactory): Factory used for establishing connections.
            factory_num_threads (int): Number of threads to be used by factory.
            max_factory_threads (int): Max. allowed threads.
        """
        # Params
        self.protocol = WSInterfaceProtocol
        self.factory = WSInterfaceFactory(url, headers)
        self.factory.set_protocol(self.protocol)
        self.factory_num_threads = 1
        self.max_factory_threads = 1000

    ############################ SETTERS #####################################

    def set_num_threads(self, num_theads: int) -> bool:
        """
        Set the number of threads to be used to process tasks with the server.

        Args:
            num_threads (int): No. of threads

        Returns:
            (bool): True if set successfully. False otherwise.
        """
        if num_theads > 0 and num_theads <= self.max_factory_threads:
            self.factory_num_threads = num_theads
            return True
        return False

    def set_callbacks(self,
                      callbacks: Dict[str, Callable[[WebsocketProtocolModel], None]]) \
            -> bool:
        """
        Set the callbacks associated with the websocket connection.

        Args:
            callbacks (Dict[str, Callable[[WebsocketProtocolModel], None]]):
                Mapping of callback names and methods/
                Must have keys:
                    1. on_connect
                    2. on_connecting
                    3. on_open
                    4. on_message
                    5. on_close
        Returns:
            (bool): True if set successfully. False otherwise.
        """
        # Ensure that dictionary is non-empty
        if len(callbacks) == 0:
            return False
        for callback_type, callback in callbacks.items():
            is_set = self.factory.set_protocol_callback(
                callback_type, callback)
            if not is_set:
                return False
        return True

    def set_data_queue(self, data_queue: Queue) -> bool:
        """
        Set the queue containing data associated with each task to be completed
        over the websocket connection.

        Args:
            data_queue (Queue): Contains tasks.

        Returns:
            (bool): True if set successfully. False otherwise.
        """
        return self.factory.set_data_queue(data_queue)

    ############################ GETTERS ######################################

    def get_configurations(self) -> Dict:
        """
        Returns configurations associated with the WSInterface instance.
        Contains useful information regarding the callbacks, Websocket factory,
        and Websocket protocol being used.

        Returns:
            (Dict): WSInterface instance configurations.
        """
        return {
            "factory_threads": self.factory_num_threads,
            "max_allowed_threads": self.max_factory_threads,
            "factory_configurations": self.factory.get_factory_configurations()
        }

    ########################### PUBLIC METHODS ################################

    def open_connection_until_complete(self, daemon: bool) -> bool:
        """
        Establish a websocket connection with the url and start processing
        tasks in the data queue. Continue until all tasks are processed.

        Args:
            daemon (bool): True to start as a daemon. False otherwise.
        """
        # The factory must be ready to connect.
        if not self.factory.is_ready():
            return False
        factory_configurations = self.factory.get_factory_configurations()
        factory_queue_size = factory_configurations["data_queue"].qsize()
        for _ in range(min(self.factory_num_threads, factory_queue_size)):
            context_factory = self._get_context_factory(
                factory_configurations["is_secure"])
            self.factory.set_context_factory(context_factory)
            connectWS(self.factory, context_factory)
        if daemon:
            self._reactor_thread_pool([self._start_reactor, self._end_reactor])
        else:
            self._reactor_thread_pool([self._end_reactor])
            self._start_reactor()
        return True

    ########################## PRIVATE METHODS ################################

    def _get_context_factory(self, is_secure: bool) -> ssl.ClientContextFactory:
        """
        Obtain the context factory if it is secure.

        Args:
            is_secure (bool)

        Returns:
            (ssl.ClientContextFactory)
        """
        if is_secure:
            return ssl.ClientContextFactory()

    def _reactor_thread_pool(self, tasks: List[Callable]) -> None:
        """
        Starts a thread pool to processes the given tasks as separate threads.

        Args:
            tasks (List[Callable]): Methods called in individual threads.
        """
        reactor_thread_pool = ThreadPool(1)
        reactor_thread_pool.spawn_threads()
        for task in tasks:
            reactor_thread_pool.add_task(task, [], {})

    def _start_reactor(self) -> None:
        """
        Start the reactor to establish websocket connection.
        """
        reactor.run()

    def _end_reactor(self) -> None:
        """
        Stop the reactor, which closes the websocket connection.
        """
        self.factory.get_factory_configurations()["data_queue"].join()
        reactor.stop()

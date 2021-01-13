# Standard library imports 
from typing import Callable, Dict, List
# Local imports 
from .WS_protocol import WebsocketProtocolModel, WSInterfaceProtocol
from .WS_factory import WSInterfaceFactory
# Third party imports 
from queue import Queue
from autobahn.twisted.websocket import connectWS
from twisted.internet import reactor, ssl


class WSInterface:

    def __init__(self, url : str, headers : Dict) -> None:
        # Params
        self.protocol = WSInterfaceProtocol
        self.factory = WSInterfaceFactory(url, headers)
        self.factory.set_protocol(self.protocol)
        self.factory_num_threads = 1
        self.max_factory_threads = 1000

    ############################ SETTERS #####################################

    def set_num_threads(self, num_theads : int) -> bool:
        if num_theads > 0 and num_theads <= self.max_factory_threads:
            self.factory_num_threads = num_theads
            return True 
        return False 

    def set_callbacks(self, 
            callbacks : Dict[[str,Callable[[WebsocketProtocolModel]]]]) -> bool:

        for callback_type, callback in callbacks:
            is_set = self.factory.set_protocol_callback(callback_type, callback)
            if not is_set:
                return False 
        return True 


    def set_data_queue(self, data_queue : Queue) -> bool:
        return self.factory.set_data_queue(data_queue)

    ########################### PUBLIC METHODS ################################

    def open_connection_until_complete(self, daemon : bool) -> bool:
        # The factory must be ready to connect.
        if not self.factory.is_ready():
            return 
        
        factory_configurations = self.factory.get_factory_configurations()
        factory_queue_size = factory_configurations["data_queue"].qsize()

        for _ in range(min(self.factory_num_threads, factory_queue_size)):
            context_factory = self._get_context_factory(
                factory_configurations["is_secure"])
            self.factory.set_context_factory(context_factory)
            connectWS(self.factory,context_factory)

        # TODO: ADD CONDITIONS FOR DAEMON.
        # TODO: NEED TO IMPLEMENT THREAD CLASS FIRST.
        if daemon:
            tasks = [self._start_reactor,self._end_reactor]
            self._reactor_thread_pool(tasks)
        else:
            tasks = [self._end_reactor]
            self._reactor_thread_pool(tasks)
            self._start_reactor()
         

    ########################## PRIVATE METHODS ################################

    def _get_context_factory(self, is_secure : bool) -> None:
        if is_secure:
            return ssl.ClientContextFactory()

    # TODO: Implement this after implementing the thread class.
    def _reactor_thread_pool(self, tasks : List[Callable]) -> None:
        pass 

    def _start_reactor(self) -> None:
        reactor.run()

    def _end_reactor(self) -> None:
        reactor.stop()


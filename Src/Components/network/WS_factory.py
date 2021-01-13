# Standard library imports 
from typing import Dict, Callable, Any
from queue import Queue, Empty
# Local imports 
from .WS_protocol import WebSocketClientProtocol, WebsocketProtocolModel
# Third party imports 
from autobahn.twisted.websocket import WebSocketClientFactory, connectWS
from twisted.internet import ssl, reactor
import validators

class WSInterfaceFactory(WebSocketClientFactory):

    def __init__(self, url : str, headers : Dict) -> None:
        # Factory params 
        self.url = url
        self.headers = headers 
        self.protocol = None 
        self.data_queue = Queue(0)
        self.context_factory = None 
        self.protocol_callbacks = {
            "on_connect" : lambda *args, **kwargs: None,
            "on_connecting" : lambda *args, **kwargs: None,
            "on_open" : lambda *args, **kwargs: None,
            "on_message" : lambda *args, **kwargs: None,
            "on_close" : lambda *args, **kwargs: None}
        # Setting protocol options 
        self.setProtocolOptions(
            utf8validateIncoming = True,
            applyMask = True,
            maxFramePayloadSize = 0,
            maxMessagePayloadSize = 0,
            autoFragmentSize = 0,
            failByDrop = True,
            echoCloseCodeReason = False,
            openHandshakeTimeout= 10, 
            closeHandshakeTimeout = 10,
            tcpNoDelay = True,
            autoPingInterval = 5,
            autoPingTimeout= 5,
            autoPingSize = 4,
            version = 18,
            acceptMaskedServerFrames = False, 
            maskClientFrames = True,
            serverConnectionDropTimeout = 1)
     

    ################################# SETTERS ###############################

    def set_protocol(self, protocol : WebSocketClientProtocol) -> bool:
        self.protocol = protocol
        return True  

    def set_data_queue(self, data_queue : Queue) -> bool:
        self.data_queue = data_queue 
        return True 

    def set_context_factory(self, context_factory : ssl.ClientContextFactory ) \
            -> bool:
        self.context_factory = context_factory
        return True   

    def set_protocol_callback(self, callback_type : str, 
            callback : Callable[[WebsocketProtocolModel]]) -> bool:
        # Must be a valid callback.
        if not callback_type in self.protocol_callbacks.keys():
            return False
        self.protocol_callbacks[callback_type] = callback
        return True 
          
    ################################# GETTERS ################################

    def get_factory_configurations(self) -> Dict: 
        return {
            "is_secure" : self.isSecure,
            "url" : self.url,
            "context_factory" : self.context_factory,
            "data_queue" : self.data_queue
        }

    def is_ready(self) -> bool:
        return self._is_ready_for_connection() 

    ########################## PUBLIC METHODS ################################

    def restart_factory(self) -> bool:
        try:
            connectWS(self,self.context_factory) 
            return True 
        except:
            return False 
    
    ######################### PRIVATE METHODS ###############################
    
    # TODO: Research and fix input and return types.
    def buildProtocol(self, addr) -> Any:
        try: 
            data = self.data_queue.get_nowait()
            protocol = self.protocol()
            protocol.set_data_queue(self.data_queue)
            protocol.set_task_data(data)
            protocol.set_factory_reference(self)
            for name, callback in self.protocol_callbacks:
                protocol.set_callback(name, callback)
            return protocol
        except Empty:
            return 

    def _is_ready_for_connection(self) -> bool:
        return self._is_valid_url(self.url) and \
                not self.data_queue.empty() and  \
                self.protocol

    def _is_valid_url(self, url : str) -> bool:
        return validators.url(url) 


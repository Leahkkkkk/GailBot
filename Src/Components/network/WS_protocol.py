# Standard library imports 
from Src.Components.network.WS_factory import WSInterfaceFactory
from typing import Any, Dict, Tuple
from queue import Queue, Empty
# Local imports 

# Third party imports
from enum import Enum
from typing import Callable
from autobahn.twisted.websocket import WebSocketClientProtocol


class WSProtocolAttributes(Enum):
    send_close_callback = "send_close_callback"
    send_message_callback = "send_message_callback"
    callback_return_data = "return_data"
    data_parameter = "data_parameter"

class WebsocketProtocolModel:
    def __init__(self):
        self.items = {
            "send_close_callback" : None,
            "send_message_callback" : None,
            "return_data" : None, 
            "data_parameter" : None
        }
    
    def get(self, attr : str) -> Any:
        return self.items[attr]

    def set(self, attr : str, data : Any) -> bool:
        if attr in self.items:
            self.items[attr] = data  
            return True 
        return False  

    def count(self) -> int:
        return len(self.items.keys())


class WSInterfaceProtocol(WebSocketClientProtocol):
    """
    Client protocol that establishes how to communicate with a server at 
    different states of a websocket connection. 

    Inherits:
        (WebSockerClientProtocol)
    """

    CLOSE_CODES = ("1000", "1001","1002","1003","1007","1008","1009","1010")

    def __init__(self):
        # Params 
        self.factory = None
        self.data_queue = None 
        self.task_data = None 
        self.callbacks = {
            "on_connect" : lambda *args, **kwargs: None,
            "on_connecting" : lambda *args, **kwargs: None,
            "on_open" : lambda *args, **kwargs: None,
            "on_message" : lambda *args, **kwargs: None,
            "on_close" : lambda *args, **kwargs: None} 

    ########################### PUBLIC METHODS ################################

    def set_callback(self, callback_type : str, 
            callback : Callable[[WebsocketProtocolModel]]) -> bool:
        # Must be a type of callback
        if not callback_type in self.callbacks.keys():
            return False 
        self.callbacks[callback_type] = callback 
        return True 

    def set_data_queue(self, data_queue : Queue) -> bool:
        self.data_queue = data_queue  

    def set_task_data(self, task_data : Any) -> bool:
        self.task_data = task_data

    def set_factory_reference(self, factory : WSInterfaceFactory) -> bool:
        self.factory = factory 
    

    ########################### PRIVATE METHODS ################################

    #### Callbacks 
    def onConnect(self, response : Any) -> None:
        self._execute_callback(self.callbacks["on_connect"],
            self._create_protocol_model({"response" : response}))


    def onConnecting(self, response : Any) -> None:
        self._execute_callback(self.callbacks["on_connecting"],
            self._create_protocol_model({"response" : response}))

    def onOpen(self) -> None:
        self._execute_callback(self.callbacks["on_open"],
            self._create_protocol_model({}))

    def onMessage(self,  payload : Any ,is_binary : bool) -> None:
        self._execute_callback(self.callbacks["on_message"],
            self._create_protocol_model({
                "payload" : payload, "is_binary" : is_binary}))

    def onClose(self, was_clean : bool, code : int, reason : Any) -> None:
        self._execute_callback( self.callbacks["on_close"],
            self._create_protocol_model({
                "was_clean" : was_clean, "code" : code, "reason" : reason}))
        # Marking task as completed
        self.data_queue.task_done()
        # Restarting the factory if the queue is not fully processed.
        if not self.data_queue.empty():
            self.factory.restart_factory() 

    #### Wrappers for sending messages 

    #### Protocol Model methods 
    def _send_close(self, code : str) -> bool:
        if code not in self.CLOSE_CODES:
            return False 
        self.sendClose(int(code))
        return True 

    def _send_message(self, payload : Any, is_binary : bool) -> bool:
        # Encode the payload appropriately
        try:
            if type(payload) == str:
                payload = payload.encode("utf-8")
            self.sendMessage(payload) 
            return True
        except:
            return False 

    #### Others 

    def _execute_callback(self, callback : Callable, data : Dict)\
             -> Tuple[bool,Any]:
        try:
            return (True,callback(data))
        except:
            return (False, None)
   
    def _create_protocol_model(self, callback_data : Dict) \
            -> WebsocketProtocolModel:
        protocol_model = WebsocketProtocolModel()
        protocol_model.set(
            WSProtocolAttributes.send_close_callback,self._send_close)
        protocol_model.set(
            WSProtocolAttributes.send_message_callback,self._send_message)
        protocol_model.set(
            WSProtocolAttributes.callback_return_data, callback_data)
        protocol_model.set(
            WSProtocolAttributes.data_parameter, self.task_data)
        return protocol_model


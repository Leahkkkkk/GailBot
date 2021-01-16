# Standard library imports 
from typing import Any, Tuple
# Third party imports
from enum import Enum

class WSProtocolAttributes(Enum):
    """
    Defines the attributes of the WebsockerProtocolModel

    Params:
        send_close_callback (Callable[[str,str],None])
        send_message_callback (Callable[[bytes,bool], None])
        send_ping_callback (Callable[[bytes],None])
        send_pong_callback (Callable[[bytes],None])
        callback_data_paramer (Any)
        callback_return_data (Tuple[bool,Dict])
    """
    send_close_callback = "send_close_callback" 
    send_message_callback = "send_message_callback"
    send_ping_callback = "send_ping_callback"
    send_pong_callback = "send_pong_callback"
    callback_data_parameter = "data_parameter"
    callback_return_data = "return_data"

class WebsocketProtocolModel:
    """
    This model class contains information that can be passed to callbacks during 
    different stages of a websocket connection.
    """
    def __init__(self):
        """
        Params:
            items (Dict): Contains mapping of WSProtocolAttributes to their 
                            values.
        """
        self.items = {
            WSProtocolAttributes.send_close_callback : None,
            WSProtocolAttributes.send_message_callback : None,
            WSProtocolAttributes.send_ping_callback : None, 
            WSProtocolAttributes.send_pong_callback : None,
            WSProtocolAttributes.callback_return_data : None, 
            WSProtocolAttributes.callback_data_parameter : None
        }
    
    def get(self, attr : str) -> Tuple[bool,Any]:
        """
        Returns the value associated with the attribute if that attribute exists
        in WSProtocolAttributes.

        Args:
            attr (WSProtocolAttributes)
        
        Returns:
            (Tuple[bool,Any]): True + data is attribute exists.
                            False + None if the attribute is invalid.
        """
        try:
            return (True,self.items[attr])
        except:
            return (False, None) 

    def set(self, attr : str, data : Any) -> bool:
        """
        Sets the given attribute to the data if it exists in WSProtocolAttributes.

        Args:
            attr (WSProtocolAttributes)
            data (Any): Data associated with the attribute.
        
        Returns:
            (bool): true if successful. False otherwise.
        """
        if attr in self.items.keys():
            self.items[attr] = data  
            return True 
        return False  

    def count(self) -> int:
        return len(self.items.keys())


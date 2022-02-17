# Standard library imports
from typing import Any, Tuple
# Local imports
from ..utils.models import IDictModel
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


class WebsocketProtocolModel(IDictModel):
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
        super().__init__()
        self.items = {
            WSProtocolAttributes.send_close_callback: None,
            WSProtocolAttributes.send_message_callback: None,
            WSProtocolAttributes.send_ping_callback: None,
            WSProtocolAttributes.send_pong_callback: None,
            WSProtocolAttributes.callback_return_data: None,
            WSProtocolAttributes.callback_data_parameter: None}

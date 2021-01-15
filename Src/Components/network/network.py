# Standard library imports 
from typing import Dict, Callable, List, Any, Tuple
from queue import Queue
# Local imports 
from .WS_interface import WSInterface 
from .request import Request
from .WS_models import WebsocketProtocolModel

# Third party imports


class Network:

    # TODO: This might potentially want to get the blackboard to  
    # configure the different networks.
    def __init__(self) -> None:
        pass
 
    ################################ PUBLIC METHODS ##########################

    def websocket_connect(self, url : str, headers : Dict, num_threads : int, 
            tasks_data : List[Any], is_daemon : bool,
            callbacks : Dict[[str,Callable[[WebsocketProtocolModel], None]]]) \
                -> bool:
        # Creating WSInterface object to manage connection.
        websocket = WSInterface(url, headers)
        # Creating the data queue.
        data_queue = Queue()
        for task_data in tasks_data:
            data_queue.put((task_data))
        # Ensuring all params are set successfully. 
        if websocket.set_num_threads(num_threads) and \
                websocket.set_callbacks(callbacks) and \
                websocket.set_data_queue(data_queue):
            websocket.open_connection_until_complete(is_daemon)
            return True 
        return False 

    def send_http_request(self,request_type : str, url : str, data : Dict, 
            timeout : int, allow_redirects : bool, verify : bool) \
            -> Tuple[bool, Dict]:
        request = Request(timeout, allow_redirects, verify)
        return request.send_request(request_type,url,data)











    


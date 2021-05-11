# Standard library imports
from typing import Dict, Callable, List, Any, Tuple
from queue import Queue
# Local imports
from .WS_interface import WSInterface
from .request import Request
from .WS_models import WebsocketProtocolModel

# Third party imports

class Network:
    """
    Convenience class that provides methods to hide complexities involved
    in establishing a websocket connection or sending requests.

    """
    def __init__(self) -> None:
        pass

    ################################ PUBLIC METHODS ##########################

    def websocket_connect(self, url : str, headers : Dict, num_threads : int,
            tasks_data : List[Any], is_daemon : bool,
            callbacks : Dict[str, Callable[[WebsocketProtocolModel], None]]) \
                -> bool:
        """
        Establish a websocket connection with the given url.

        Args:
            url (str): Url of the server with which to establish the connection.
            headers (Dict): Header data to be passed to the server.
            num_threads (int): No. of threads used to process all tasks.
            tasks_data (List[Any]): Data associated with each task that is
                                passed to the callbacks for these tasks.
            is_daemon (bool): True to run as a separate process. False otherwise.
            callbacks (Dict[str, Callable[[WebsocketProtocolModel], None]]):
                Mapping of callback names and methods.
                Must have keys:
                    1. on_connect
                    2. on_connecting
                    3. on_open
                    4. on_message
                    5. on_close
                Every callback must take a WebsocketProtocolModel as an argument.

        Returns:
            (bool): True if the connection was successful and all tasks processed.
                    False otherwise.
        """
        # List to store status
        status = list()
        # Creating the data queue from the given tasks
        data_queue = Queue()
        for task_data in tasks_data:
            data_queue.put(task_data)
        # Creating WSInterface object to manage connection.
        websocket = WSInterface(url,headers)
        # Attempting to set all parameters.
        status.append(websocket.set_num_threads(num_threads))
        status.append(websocket.set_callbacks(callbacks))
        status.append(websocket.set_data_queue(data_queue))
        status.append(websocket.open_connection_until_complete(is_daemon))
        # Successful only if all steps were successful.
        print(status)
        return all(status)

    def send_http_request(self,request_type : str, url : str, data : Dict,
            timeout : int, allow_redirects : bool, verify : bool) \
                -> Tuple[bool, Dict]:
        """
        Send an HTTP request to the url.

        Args:
            request_type (str): Any one of "GET","OPTIONS","HEAD","POST","PUT",
                                "PATCH","DELETE".
            url (str): Valid url the request is being sent to.
            data (Dict):
                Key-value pairs of data being sent with the request.
                Must have any or all of the following mappings:
                    1. params (Dict): Parameters sent with request.
                    2. data (Dict): data sent with request.
                    3. json (Dict): Data sent in json form.
                    4. auth (Tuple): Authentication tuple
                    5. headers (Dict): Headers sent with data
            timeout (int): Time after which request times out. 60 seconds default.
            allow_redirects (bool): True to be redirected by server. False otherwise.
            verify (bool): True to verify server contact. False otherwise.

        Returns:
            (Tuple[bool, Dict]):
                Tuple contains True if request was successfully
                sent or False if it was unsuccessful along with
                the data returned by the request.
                The output dictionary will have the following keys if bool is True:
                    1. "content"
                    2. "apparent_encoding"
                    3. "cookies"
                    4. "time_elapsed"
                    5. "response_encoding"
                    6. "is_redirect"
                    7. "response_ok"
                    8. "reason"
                    9. "status_code"
                    10. "response_url"
        """
        # Creating a request instance to run the request.
        request = Request(timeout, allow_redirects, verify)
        # Sending the appropriate request and returning the data as a dictionary.
        return request.send_request(request_type,url,data)














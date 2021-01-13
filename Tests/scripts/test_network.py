"""
testing script for the network component
"""
# Standard library imports 
# Local imports 
from Src.Components.network import Request
from ..suites import TestSuite, TestSuiteAttributes

############################### GLOBALS #####################################

########################## TEST DEFINITIONS ##################################

#### REQUESTS TESTS

def request_send_request() -> bool:
    """
    Tests the send request method in Request.

    Tests:
        1. Send request to all of "GET","OPTIONS","HEAD","POST","PUT","PATCH",
        "DELETE" with no data and valid url
        2.  Send request to all of "GET","OPTIONS","HEAD","POST","PUT","PATCH",
        "DELETE" with some data and check results and valid url
        3. Sending invalid url.
        4. Send data dictionary with invalid keys but valid url.
        5. Send data dictionary with invalid keys and invalid url.

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    request = Request()
    results = dict()
    # Data dictionaries to pass with request 
    empty_data_dict = {
        "params" : {},
        "data" : {},
        "json" : {},
        "auth" : {},
        "headers" : {}}
    # Using postman urls for testing different request types
    get_url = "https://postman-echo.com/get?foo1=bar1&foo2=bar2"
    options_url = "https://postman-echo.com/get?foo1=bar1&foo2=bar2"
    post_url = "https://postman-echo.com/post"
    put_url = "https://postman-echo.com/put"
    patch_url = "https://postman-echo.com/patch"
    delete_url = "https://postman-echo.com/delete"
    invalid_url = "https://invalid.com"
    # Running requests 
    results["GET"] = request.send_request("GET",get_url,empty_data_dict)
    results["OPTIONS"] = request.send_request(
        "OPTIONS",options_url,empty_data_dict)
    results["POST"] = request.send_request("POST",post_url,empty_data_dict)
    results["PUT"] = request.send_request("PUT",put_url,empty_data_dict)
    results["PATCH"] = request.send_request("PATCH",patch_url,empty_data_dict)
    results["DELETE"] = request.send_request(
        "DELETE",delete_url,empty_data_dict)
    # All requests must return True and have status code 200.
    # Checks Invalid url 
    return all([v[0] for v in results.values()]) and \
        all([v[1]["status_code"] == 200 for v in results.values()]) and \
        not request.send_request("GET",invalid_url, empty_data_dict)[0] and \
        not request.send_request("GET", get_url,{"invalid key" : None })[0] and \
        not request.send_request("GET",invalid_url,{"invalid key" : None })[0]
        
####################### TEST SUITE DEFINITION ################################

def define_network_test_suite() -> TestSuite:
    """
    Creates a test suite for networks and adds tests to the suite.

    Returns:
        (TestSuite): Suite containing network tests
    """
    suite = TestSuite()
    # Request tests 
    suite.add_test("request_send_request", (), True, True, request_send_request)
    return suite



class NetworkInterface:
    """ Responsible for providing the main interface that allows different 
        types of communication over a network """
    
    def __init__(self):
        # Requests variables 
        self.requests = RequestsInterface()
        self.request_url = None 
        self.request_json = None 
        self.request_params = None 
        self.request_data = None 
        self.request_auth = None 
        self.request_headers = None 
        # Websocket variables 
        self.websockets = None 
        self.websockets_url = None 
        self.websockets_queue = None 
        self.websockets_headers = None 
        self.websockets_callbacks = {
            "on_connect" : None,
            "on_connecting" : None,
            "on_open" : None,
            "on_message" : None,
            "on_close" : None}
    
    ################################## SETTERS ##############################
    
    #### Request setters 
    
    def set_request_url(self, request_url : str) -> None:
        """
        Set the url for an http request that is to be made.

        Args:
            request_url (str): url for an http request

        Returns:
            None

        """
        self.request_url = request_url
    
    
    def set_requests_url_params(self,params : Dict) -> None:
        """
        Set the parameters that will be sent with an http request url

        Args:
            params (Dict): Parameters to be sent with url

        Returns:
            None

        """
        self.request_params = params 
    
    
    def set_request_data(self,data : Dict) -> None:
        """
        Set the data dictionary that will be sent with an http request

        Args:
            data (Dict): Data to be sent with http request

        Returns:
            None

        """
        self.request_data = data
        
    
    def set_request_authentication(self, auth : Dict) -> None:
        """
        Set the authentication values that will be sent with an http request

        Args:
            auth (Dict): Authentication values to be sent with request

        Returns:
            None

        """
        self.request_auth = auth 
    
    
    def set_request_headers(self, headers : Dict) -> None:
        """
        Set the headers that will be sent with an http request

        Args:
            headers (Dict): Headers to be sent with request

        Returns:
            None

        """
        self.request_headers = headers
    
    #### Websocket setters 
     
    def set_websocket_url(self, url: str) -> None:
        """
        Set the server url to be used to establish a WebSocket connection with

        Args:
            url (str): url for websocket connection

        Returns:
            None

        """
        self.websockets_url = url
    
    def set_websocket_data_queue(self, queue: Queue) -> None:
        """
        Set the data queue contiaining data items that are to be processed 
        by the websocket server.
        Items in this queue will be processed by sending them to callbacks
        on websocket events.

        Args:
            queue (Queue): Queue containing data items that will be sent to 
                            callbacks on an event.

        Returns:
            None

        """
        self.websockets_queue = queue
        
        
    def set_websocket_headers(self, headers: Dict) -> None:
        """
        Headers that will be sent to server when trying to open an initial
        websocket connection

        Args:
            headers (Dict): Headers to be sent to websocket server

        Returns:
            None
        """
        self.websockets_headers = headers
    
    def set_websocket_on_connect_callback(
            self, func: Callable[[WebsocketProtocolModel], None]) -> None:
        """
        Set callback that will be called when websocket connection opens

        Args:
            func (Callable[[WebsocketProtocolModel],None]):

        Returns:
            None

        """
        self.websockets_callbacks["on_connect"] = func 
    
    
    def set_websocket_on_connecting_callback(
            self, func: Callable[[WebsocketProtocolModel], None]) -> None:
        """
        Set callback that will be called when the websocket is connecting

        Args:
            func (Callable[[WebsocketProtocolModel],None]):

        Returns:
            None
        """
        self.websockets_callbacks["on_connecting"] = func 
    
    def set_websocket_on_open_callback(
            self, func: Callable[[WebsocketProtocolModel], None]) -> None:
        """
        Set callback that will be called when the websocket is opened

        Args:
            func (Callable[[WebsocketProtocolModel],None]):

        Returns:
            None
        """
        self.websockets_callbacks["on_open"] = func
    
    def set_websocket_on_message_callback(
            self, func: Callable[[WebsocketProtocolModel], None]) -> None:
        """
        Set callback that will be called when a message is received from the 
        websocket server.

        Args:
            func (Callable[[WebsocketProtocolModel],None]):

        Returns:
            None
        """
        self.websockets_callbacks["on_message"] = func
    
    def set_websocket_on_close_callback(
            self, func: Callable[[WebsocketProtocolModel], None]) -> None:
        """
        Set callback that is called when the websocket connection is closed.

        Args:
            func (Callable[[WebsocketProtocolModel],None]):

        Returns:
            None
        """
        self.websockets_callbacks["on_close"] = func
    
    ############################## PUBLIC METHODS ###########################
    
    #### HTTP requests 
    def get_request(self) -> RequestModel:
        """
        Send GET HTTP request

        Args:

        Returns:
            RequestModel
        """
        return self._send_http_request("GET") 
    
    def options_request(self) -> RequestModel:
        """
        Send OPTIONS HTTP request

        Args:

        Returns:
            RequestModel
        """
        return self._send_http_request("OPTIONS")
    
    def head_request(self) -> RequestModel:
        """
        Send HEAD HTTP request

        Args:

        Returns:
            RequestModel
        """
        return self._send_http_request("HEAD")
    
    def post_request(self) -> RequestModel:
        """
        Send POST HTTP request

        Args:

        Returns:
            RequestModel
        """
        return self._send_http_request("POST")
    
    def put_request(self) -> RequestModel:
        """
        Send PUT HTTP request

        Args:

        Returns:
            RequestModel
        """
        return self._send_http_request("PUT")
    
    def patch_request(self) -> RequestModel:
        """
        Send PATCH HTTP request

        Args:

        Returns:
            RequestModel
        """
        return self._send_http_request("PATCH")
    
    def delete_request(self) -> RequestModel:
        """
        Send DELETE HTTP request

        Args:
        
        Returns:
            RequestModel
        """
        return self._send_http_request("DELETE")
    
    #### Websockets 
    def websocket_connect(self) -> None:
        """
        Open a websocket connection and process all items in the data queue

        Args:

        Returns:
            None
        """
        self.websockets = WebSocketInterface(
            self.websockets_url,self.websockets_headers) 
        self.websockets.set_data_queue(self.websockets_queue)
        self.websockets.set_thread_count(self.websockets_queue.qsize())
        self.websockets.set_on_connect_callback(
            self.websockets_callbacks["on_connect"])
        self.websockets.set_on_connecting_callback(
            self.websockets_callbacks["on_connecting"])
        self.websockets.set_on_open_callback(
            self.websockets_callbacks["on_open"])
        self.websockets.set_on_message_callback(
            self.websockets_callbacks["on_message"])
        self.websockets.set_on_close_callback(
            self.websockets_callbacks["on_close"])
        self.websockets.open_connection_until_complete()
    
    ############################## PRIVATE METHODS ##########################
    def _send_http_request(self, request_type : str) -> RequestModel:
        """
        Wrapper for sending an HTTP request 
        
        Args:
            request_type (str): Type of HTTP request
            
        Returns:
            None
        """
        return self.requests.send_request(
            request_type, self.request_url, self.request_params, 
            self.request_data, self.request_json, self.request_auth, 
            self.request_headers)
    
    
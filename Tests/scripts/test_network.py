"""
testing script for the network component
"""
# Standard library imports 
from queue import Queue
# Local imports 
from Src.Components.network import Request, WSInterface, WSProtocolAttributes, \
                                WebsocketProtocolModel
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

#### WebsocketProtocolModel test
def websocket_protocol_model_set() -> bool:
    """
    Tests the WebsocketProtocolModel class's set function.

    Tests:
        1. Set an attribute that exists.
        2. Set an attribute that does not exist.
    
    Returns:
        (bool): True if all the tests pass. False otherwise.
    """
    model = WebsocketProtocolModel()
    return model.set(WSProtocolAttributes.send_close_callback, {}) and \
        model.set(WSProtocolAttributes.send_message_callback, {}) and \
        model.set(WSProtocolAttributes.callback_return_data, {}) and \
        model.set(WSProtocolAttributes.data_parameter, {}) and \
        not model.set("Not real", {})

def websocket_protocol_model_get() -> bool:
    """
    Tests the WebsocketProtocolModel get function.

    Tests:
        1. Tests that we can get a valid attribute data.
        2. Test that we cannot get invalid attribute data.

    Returns:
        (bool): True if all the tests pass. False otherwise.
    """
    model = WebsocketProtocolModel()
    return model.get(WSProtocolAttributes.send_close_callback)[0] and \
        model.get(WSProtocolAttributes.send_message_callback)[0] and \
        model.get(WSProtocolAttributes.callback_return_data)[0] and \
        model.get(WSProtocolAttributes.data_parameter)[0] and \
        not model.get("Not real")[0]


#### WEBSOCKETS TEST

def on_connect_callback(model : WebsocketProtocolModel) -> None:
    # response =  model.get(WSProtocolAttributes.callback_return_data)[
    #         "response"]
    # print("OnConnect\nServer connected: {}".format(response.peer))
    # print("Websocket Protocol : {}".format(response.protocol))
    # print("Protocol Version : {}\n".format(response.version))
    try:
        response =  model.get(WSProtocolAttributes.callback_return_data)[
            "response"]
        print("OnConnect\nServer connected: {}".format(response.peer))
        print("Websocket Protocol : {}".format(response.protocol))
        print("Protocol Version : {}\n".format(response.version))
    except: 
        print("On connect failed")
    

def on_connecting_callback(model : WebsocketProtocolModel) -> None:
    # response = model.get(WSProtocolAttributes.callback_return_data)["response"]
    # print("On connecting")
    # print(response) 
    try:
        response = model.get(WSProtocolAttributes.callback_return_data)["response"]
        print("On connecting")
        print(response) 
    except:
        print("On connecting failed")

def on_open_callback(model : WebsocketProtocolModel) -> None:
    # print("Opening API connection")
    # task_data = model.get(WSProtocolAttributes.data_parameter)
    # print("Task data: {}".format(task_data))
    # msg = 'WebSocket rocks!'.encode('utf-8')
    # model.get(WSProtocolAttributes.send_message_callback)(
    #     payload = msg, is_binary = False )
    try:
        print("Opening API connection")
        task_data = model.get(WSProtocolAttributes.data_parameter)
        print("Task data: {}".format(task_data))
        msg = 'WebSocket rocks!'.encode('utf-8')
        model.get(WSProtocolAttributes.send_message_callback)(
            payload = msg, is_binary = False )
    except:
        print("On open failed.")

def on_message_callback(model : WebsocketProtocolModel) -> None:
    # print("On message")
    # data = model.get(WSProtocolAttributes.callback_return_data)
    # payload = data["payload"].decode("utf-8")
    # is_binary = data["is_binary"]
    # print("Getting message: {}".format(payload))
    # print("Is binary: {}".format(is_binary))
    # model.get(WSProtocolAttributes.send_close_callback)("1000")
    try:
        print("On message")
        data = model.get(WSProtocolAttributes.callback_return_data)
        payload = data["payload"].decode("utf-8")
        is_binary = data["is_binary"]
        print("Getting message: {}".format(payload))
        print("Is binary: {}".format(is_binary))
        model.get(WSProtocolAttributes.send_close_callback)("1000")
    except:
        print("On message failed.")

def on_close_callback(model : WebsocketProtocolModel) -> None:
    # data = model.get(WSProtocolAttributes.callback_return_data)
    # print("\nClosing API WebSocket connection")
    # print('Websocket Connection closed:\n\tCode: {0}\n\tReason: {1}\n'
    #     '\twasClean: {2}'.format(data["code"], data["reason"], 
    #                             data["was_clean"]))
    try:
        data = model.get(WSProtocolAttributes.callback_return_data)
        print("\nClosing API WebSocket connection")
        print('Websocket Connection closed:\n\tCode: {0}\n\tReason: {1}\n'
            '\twasClean: {2}'.format(data["code"], data["reason"], 
                                    data["was_clean"]))
    except:
        print("On close failed")

def websocket_interface() -> bool:
    """
    Tests the WSInterface class that uses the WSInterfaceProtocol and 
    WSInterfaceFactory. 

    Tests:
        1. 

    Returns:
        (bool): True if all the tests pass. False otherwise.
    """
    thread_count = 1
    ws_test_url =  "wss://echo.websocket.org"
    ws_test_headers = {}
    callbacks = {
        "on_connect" : on_connect_callback,
        "on_connecting" : on_connecting_callback,
        "on_message" : on_message_callback,
        "on_open" : on_open_callback,
        "on_close" : on_close_callback}
    test_queue = Queue()
    test_queue.put(("Test string 1"))
    test_queue.put(("Test string 2"))
    # Create websocket interface interface instance 
    ws_interface = WSInterface(ws_test_url, ws_test_headers)
    ws_interface.set_num_threads(thread_count)
    ws_interface.set_data_queue(test_queue)
    ws_interface.set_callbacks(callbacks)
    # Starting connection (Daemon not available right now)
    return ws_interface.open_connection_until_complete(False)
    

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
    suite.add_test("websocket_protocol_model_set", (), True, True, 
        websocket_protocol_model_set)
    suite.add_test("websocket_protocol_model_get", (), True, True, 
        websocket_protocol_model_get)
    suite.add_test("websocket_interface", (), True, True, websocket_interface)
    return suite



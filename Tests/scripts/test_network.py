"""
testing script for the network component
"""
# Standard library imports 
from queue import Queue

# Local imports 
from Src.Components.network import Request, WSInterface, WSProtocolAttributes, \
                                WebsocketProtocolModel,Network
from ..suites import TestSuite, TestSuiteAttributes

############################### GLOBALS #####################################

########################## TEST DEFINITIONS ##################################

############################ REQUESTS TESTS

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

def request_send_request_get() -> bool:
    request = Request()
    empty_data_dict = {
        "params" : {},
        "data" : {},
        "json" : {},
        "auth" : {},
        "headers" : {}}

    get_url = "https://postman-echo.com/get?foo1=bar1&foo2=bar2"
    success, req_dict = request.send_request("GET",get_url,empty_data_dict)
    return success and req_dict["status_code"] == 200

def request_send_request_post() -> bool:
    request = Request()
    empty_data_dict = {
        "params" : {},
        "data" : {},
        "json" : {},
        "auth" : {},
        "headers" : {}}
    
    post_url = "https://postman-echo.com/post"
    success, req_dict = request.send_request("POST",post_url,empty_data_dict)
    return success and req_dict["status_code"] == 200

def request_send_request_options() -> bool:
    request = Request()
    empty_data_dict = {
        "params" : {},
        "data" : {},
        "json" : {},
        "auth" : {},
        "headers" : {}}
    
    options_url = "https://postman-echo.com/get?foo1=bar1&foo2=bar2"
    success, req_dict = request.send_request("OPTIONS",options_url,empty_data_dict)
    return success and req_dict["status_code"] == 200

def request_send_request_put() -> bool:
    request = Request()
    empty_data_dict = {
        "params" : {},
        "data" : {},
        "json" : {},
        "auth" : {},
        "headers" : {}}
    
    put_url = "https://postman-echo.com/put"
    success, req_dict = request.send_request("PUT",put_url,empty_data_dict)  
    return success and req_dict["status_code"] == 200

def request_send_request_patch() -> bool:
    request = Request()
    empty_data_dict = {
        "params" : {},
        "data" : {},
        "json" : {},
        "auth" : {},
        "headers" : {}}
    
    patch_url = "https://postman-echo.com/patch"
    success, req_dict = request.send_request("PATCH",patch_url,empty_data_dict)
    return success and req_dict["status_code"] == 200

def request_send_request_delete() -> bool:
    request = Request()
    empty_data_dict = {
        "params" : {},
        "data" : {},
        "json" : {},
        "auth" : {},
        "headers" : {}}
    
    delete_url = "https://postman-echo.com/delete"
    success, req_dict = request.send_request("DELETE",delete_url,empty_data_dict)
    return success and req_dict["status_code"] == 200

def request_send_bad_request_invalid_url() -> bool:
    request = Request()
    empty_data_dict = {
        "params" : {},
        "data" : {},
        "json" : {},
        "auth" : {},
        "headers" : {}}

    invalid_url = "https://invalid.com"
    success, _ = request.send_request("GET",invalid_url, empty_data_dict)
    return not success

def request_send_bad_request_invalid_keys() -> bool:
    request = Request()
    invalid = {
        "bad" : {},
        "data" : {},
        "json" : {},
        "auth" : {},
        "headers" : {}}

    valid_url = "https://postman-echo.com/get?foo1=bar1&foo2=bar2"
    success, _ = request.send_request("GET",valid_url, invalid)
    return not success

def request_send_bad_request_invalid_url_keys() -> bool:
    request = Request()
    invalid = {
        "bad" : {},
        "data" : {},
        "json" : {},
        "auth" : {},
        "headers" : {}}

    invalid_url = "https://invalid.com"
    success, _ = request.send_request("GET",invalid_url, invalid)
    return not success

def request_send_bad_request_invalid_request_type() -> bool:
    request = Request()
    invalid = {
        "params" : {},
        "data" : {},
        "json" : {},
        "auth" : {},
        "headers" : {}}

    valid_url = "https://postman-echo.com/get?foo1=bar1&foo2=bar2"
    success, req_dict = request.send_request("BAD_GET",valid_url, invalid)
    return not success and all([v == None for v in req_dict.values()])

####################### WebsocketProtocolModel test
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
        model.set(WSProtocolAttributes.callback_data_parameter, {}) and \
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
        model.get(WSProtocolAttributes.callback_data_parameter)[0] and \
        not model.get("Not real")[0]

############################# WSInterface Tests


#### WSInterface callback definitions

def on_connect_callback(model : WebsocketProtocolModel) -> None:
    try:
        print("On connect...")
        status, return_data =  model.get(
            WSProtocolAttributes.callback_return_data)
        response = return_data["response"]
        print("OnConnect\nServer connected: {}".format(response.peer))
        print("OnConnect status: {}".format(status))
        print("Websocket Protocol : {}".format(response.protocol))
        print("Protocol Version : {}\n".format(response.version))
    except: 
        print("On connect failed...")
    

def on_connecting_callback(model : WebsocketProtocolModel) -> None:
    try:
        print("On connecting...")
        status, return_data  = model.get(WSProtocolAttributes.callback_return_data)
        print("On connecting status: {}".format(status)) 

    except:
        print("On connecting failed")

def on_open_callback(model : WebsocketProtocolModel) -> None:

    try:
        print("Opening API connection")
        status, return_data  = model.get(WSProtocolAttributes.callback_return_data)
        task_data = model.get(WSProtocolAttributes.callback_data_parameter)
        print("On open status: {}".format(status))
        print("Task data: {}".format(task_data))
        msg = 'WebSocket rocks!'.encode('utf-8')
        model.get(WSProtocolAttributes.send_message_callback)[1](
            payload = msg, is_binary = True )
    except:
        print("On open failed.")

def on_message_callback(model : WebsocketProtocolModel) -> None:
    try:
        print("On message")
        status, return_data  = model.get(WSProtocolAttributes.callback_return_data)
        payload = return_data["payload"].decode("utf-8")
        is_binary = return_data["is_binary"]
        print("Getting message: {}".format(payload))
        print("Is binary: {}".format(is_binary))
        model.get(WSProtocolAttributes.send_close_callback)[1]("1000")
    except:
        print("On message failed.")

def on_close_callback(model : WebsocketProtocolModel) -> None:
    try:
        status, return_data = model.get(WSProtocolAttributes.callback_return_data)
        print("\nClosing API WebSocket connection")
        print('Websocket Connection closed:\n\tCode: {0}\n\tReason: {1}\n'
            '\twasClean: {2}'.format(return_data["code"], return_data["reason"], 
                                    return_data["was_clean"]))
    except:
        print("On close failed")

#### WSInterface test definitions.

def WSInterface_set() -> bool:
    """
    Tests all setters for WSInterface.

    Tests:
        1. Provide valid values for all setters.
        2. Provide invalid values for all setters. 

    Returns:
        (bool): True if all the tests pass. False otherwise.
    """
    ws_test_url =  "wss://echo.websocket.org"
    ws_test_headers = {}
    data_queue = Queue()
    data_queue.put(("Test"))
    callbacks = {
        "on_connect" : on_connect_callback,
        "on_connecting" : on_connecting_callback,
        "on_message" : on_message_callback,
        "on_open" : on_open_callback,
        "on_close" : on_close_callback}
    ws_interface = WSInterface(ws_test_url, ws_test_headers)
    return ws_interface.set_num_threads(5) and \
            ws_interface.set_callbacks(callbacks) and \
            ws_interface.set_data_queue(data_queue) and \
            not ws_interface.set_num_threads(2000) and \
            not ws_interface.set_callbacks({})
    
def WSInterface_set_bad_callbacks() -> bool:
    ws_test_url =  "wss://echo.websocket.org"
    ws_test_headers = {}
    callbacks = {
        "bad" : on_connect_callback,
        "on_connecting" : on_connecting_callback,
        "on_message" : on_message_callback,
        "on_open" : on_open_callback,
        "on_close" : on_close_callback}
    
    ws_interface = WSInterface(ws_test_url, ws_test_headers)
    return not ws_interface.set_callbacks(callbacks)

def WSInterface_get() -> bool:
    """
    Tests all getters in WSInterface.

    Tests:
        1. Ensure that get_configurations returns a valid dictionary.
        2. Ensure that the expected keys are returned only.
    
    Returns:
        (bool): True if all the tests pass. False otherwise.
    """
    expected_keys = [
        "factory_threads" ,
        "max_allowed_threads",
        "factory_configurations" ]
    ws_test_url =  "wss://echo.websocket.org"
    ws_test_headers = {} 
    ws_interface = WSInterface(ws_test_url, ws_test_headers)
    configs = ws_interface.get_configurations()
    return type(configs) == dict and \
        len(configs.keys()) == len(expected_keys) and \
        all([ k for k in configs.keys() if k in expected_keys ])

def WSInterface_open_connection() -> bool:
    """
    Tests the open_connection_until_complete WSInterface class that uses 
    the WSInterfaceProtocol and WSInterfaceFactory. 

    Tests:
        1. Set up a valid connection with callbacks that handle exceptions as 
            not a daemon (multi-threaded).
        2. Set up a valid connection with callbacks that handle exceptions as 
            a daemon (multi-threaded).

    Returns:
        (bool): True if all the tests pass. False otherwise.
    """
    # Test 1.
    num_queue_items = 50
    thread_count = 50
    ws_test_url =  "wss://echo.websocket.org"
    ws_test_headers = {}
    callbacks = {
        "on_connect" : on_connect_callback,
        "on_connecting" : on_connecting_callback,
        "on_message" : on_message_callback,
        "on_open" : on_open_callback,
        "on_close" : on_close_callback}
    daemon_test_queue = Queue()
    test_queue = Queue()
    for i in range(num_queue_items):
        daemon_test_queue.put(("Test string {}".format(i)))
        test_queue.put(("Test string {}".format(i)))
        
    # Create websocket interface interface instance 
    ws_interface = WSInterface(ws_test_url, ws_test_headers)
    ws_interface.set_num_threads(thread_count)
    ws_interface.set_data_queue(test_queue)
    ws_interface.set_callbacks(callbacks)
    # Starting connection
    success_1 = ws_interface.open_connection_until_complete(False)
    # Re-adding daemon tasks and restarting WSInterface as a daemon
    ws_interface.set_data_queue(daemon_test_queue)
    success_2 = ws_interface.open_connection_until_complete(True)
    return success_1 and success_2

def WSInterface_open_connection_valid_no_daemon() -> bool:
    num_queue_items = 50
    thread_count = 50
    ws_test_url =  "wss://echo.websocket.org"
    ws_test_headers = {}
    callbacks = {
        "on_connect" : on_connect_callback,
        "on_connecting" : on_connecting_callback,
        "on_message" : on_message_callback,
        "on_open" : on_open_callback,
        "on_close" : on_close_callback}
    daemon_test_queue = Queue()
    test_queue = Queue()
    for i in range(num_queue_items):
        daemon_test_queue.put(("Test string {}".format(i)))
        test_queue.put(("Test string {}".format(i)))
    
    ws_interface = WSInterface(ws_test_url, ws_test_headers)
    ws_interface.set_num_threads(thread_count)
    ws_interface.set_data_queue(test_queue)
    ws_interface.set_callbacks(callbacks)

    success = ws_interface.open_connection_until_complete(False)

    return success

def WSInterface_open_connection_valid_daemon() -> bool:
    num_queue_items = 50
    thread_count = 50
    ws_test_url =  "wss://echo.websocket.org"
    ws_test_headers = {}
    callbacks = {
        "on_connect" : on_connect_callback,
        "on_connecting" : on_connecting_callback,
        "on_message" : on_message_callback,
        "on_open" : on_open_callback,
        "on_close" : on_close_callback}
    daemon_test_queue = Queue()
    test_queue = Queue()
    for i in range(num_queue_items):
        daemon_test_queue.put(("Test string {}".format(i)))
        test_queue.put(("Test string {}".format(i)))
    
    ws_interface = WSInterface(ws_test_url, ws_test_headers)
    ws_interface.set_num_threads(thread_count)
    ws_interface.set_data_queue(test_queue)
    ws_interface.set_callbacks(callbacks)

    ws_interface.set_data_queue(daemon_test_queue)
    success = ws_interface.open_connection_until_complete(True)
    
    return success

########################### Network tests

def network_websocket_connection() -> bool:
    """
    Tests the websocket_connect method of the network class.

    Tests:
        1. Use valid params to connect to the websocket server.
        2. Use invalid params to try and connect with the server.
    """
    network = Network()
    num_tasks = 50
    thread_count = 50
    tasks = list()
    ws_test_url =  "wss://echo.websocket.org"
    ws_test_headers = {}
    callbacks = {
        "on_connect" : on_connect_callback,
        "on_connecting" : on_connecting_callback,
        "on_message" : on_message_callback,
        "on_open" : on_open_callback,
        "on_close" : on_close_callback}
    for i in range(num_tasks):
        tasks.append("Task {}".format(i))
    # Running request both as daemon and not daemon.
    return network.websocket_connect(
        url=ws_test_url, headers=ws_test_headers, num_threads= thread_count,
        tasks_data=tasks,is_daemon=True,callbacks=callbacks)

def network_websocket_connection_bad_threads() -> bool:
    network = Network()
    num_tasks = 50
    thread_count = 0
    tasks = list()
    ws_test_url =  "wss://echo.websocket.org"
    ws_test_headers = {}
    callbacks = {
        "on_connect" : on_connect_callback,
        "on_connecting" : on_connecting_callback,
        "on_message" : on_message_callback,
        "on_open" : on_open_callback,
        "on_close" : on_close_callback}
    for i in range(num_tasks):
        tasks.append("Task {}".format(i))
    return not network.websocket_connect(
        url=ws_test_url, headers=ws_test_headers, num_threads= thread_count,
        tasks_data=tasks,is_daemon=True,callbacks=callbacks)

def network_websocket_connection_bad_callback() -> bool:
    network = Network()
    num_tasks = 50
    thread_count = 50
    tasks = list()
    ws_test_url =  "wss://echo.websocket.org"
    ws_test_headers = {}
    callbacks = {
        "on_connect" : on_connect_callback,
        "on_connecting" : on_connecting_callback,
        "on_message" : on_message_callback,
        "on_open" : on_open_callback,
        "on_close" : on_close_callback}
    for i in range(num_tasks):
        tasks.append("Task {}".format(i))
    return not network.websocket_connect(
        url=ws_test_url, headers=ws_test_headers, num_threads= thread_count,
        tasks_data=tasks,is_daemon=True,callbacks=callbacks)

def network_websocket_connection_bad_callback() -> bool:
    network = Network()
    num_tasks = 50
    thread_count = 50
    tasks = list()
    ws_test_url =  "wss://echo.websocket.org"
    ws_test_headers = {}
    callbacks = {
        "bad" : on_connect_callback,
        "on_connecting" : on_connecting_callback,
        "on_message" : on_message_callback,
        "on_open" : on_open_callback,
        "on_close" : on_close_callback}
    for i in range(num_tasks):
        tasks.append("Task {}".format(i))
    return not network.websocket_connect(
        url=ws_test_url, headers=ws_test_headers, num_threads= thread_count,
        tasks_data=tasks,is_daemon=True,callbacks=callbacks)

def network_websocket_connection_bad_url() -> bool:
    network = Network()
    num_tasks = 50
    thread_count = 50
    tasks = list()
    ws_test_url =  "wss://foobar.org"
    ws_test_headers = {}
    callbacks = {
        "on_connect" : on_connect_callback,
        "on_connecting" : on_connecting_callback,
        "on_message" : on_message_callback,
        "on_open" : on_open_callback,
        "on_close" : on_close_callback}
    for i in range(num_tasks):
        tasks.append("Task {}".format(i))
    return not network.websocket_connect(
        url=ws_test_url, headers=ws_test_headers, num_threads= thread_count,
        tasks_data=tasks,is_daemon=True,callbacks=callbacks)

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
    suite.add_test("request_send_request_get", (), True, True, request_send_request_get)
    suite.add_test("request_send_request_options", (), True, True, request_send_request_options)
    suite.add_test("request_send_request_post", (), True, True, request_send_request_post)
    suite.add_test("request_send_request_put", (), True, True, request_send_request_put)
    suite.add_test("request_send_request_patch", (), True, True, request_send_request_patch)
    suite.add_test("request_send_request_delete", (), True, True, request_send_request_delete)
    suite.add_test("request_send_bad_request_invalid_url", (), True, True, request_send_bad_request_invalid_url)
    suite.add_test("request_send_bad_request_invalid_keys", (), True, True, request_send_bad_request_invalid_keys)
    suite.add_test("request_send_bad_request_invalid_url_keys", (), True, True, request_send_bad_request_invalid_url_keys)
    suite.add_test("request_send_bad_request_invalid_request_type", (), True, True, request_send_bad_request_invalid_request_type)

    # WebsocketProtocolModel tests 
    suite.add_test("websocket_protocol_model_set", (), True, True, 
       websocket_protocol_model_set)
    suite.add_test("websocket_protocol_model_get", (), True, True, 
        websocket_protocol_model_get)
    # WSInterface tests
    suite.add_test("WSInterface_set",(),True,True,WSInterface_set)
    suite.add_test("WSInterface_set_bad_callbacks",(),True,True,WSInterface_set_bad_callbacks)
    suite.add_test("WSInterface_get", (), True, True, WSInterface_get)
    # suite.add_test("WSInterface_open_connection",
    #                   (), True, True, WSInterface_open_connection)
    suite.add_test("WSInterface_open_connection_valid_no_daemon",
                       (), True, True, WSInterface_open_connection_valid_no_daemon)
    suite.add_test("WSInterface_open_connection_valid_daemon",
                        (), True, True, WSInterface_open_connection_valid_daemon)
    # Network tests
    suite.add_test("network_websocket_connection", (), True, True,
        network_websocket_connection)
    suite.add_test("network_websocket_connection_bad_threads", (), True, True,
         network_websocket_connection_bad_threads)
    suite.add_test("network_websocket_connection_bad_callback", (), True, True,
         network_websocket_connection_bad_callback)
    # suite.add_test("network_websocket_connection_bad_url", (), True, True,
    #     network_websocket_connection_bad_url)
    return suite



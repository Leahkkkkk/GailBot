# Local imports
from Src.components.network import WebsocketProtocolModel, WSProtocolAttributes,\
    Network

############################### GLOBALS #####################################

############################### SETUP #####################################


def on_connect_callback(model: WebsocketProtocolModel) -> None:
    try:
        print("On connect...")
        status, return_data = model.get(
            WSProtocolAttributes.callback_return_data)
        response = return_data["response"]
        print("OnConnect\nServer connected: {}".format(response.peer))
        print("OnConnect status: {}".format(status))
        print("Websocket Protocol : {}".format(response.protocol))
        print("Protocol Version : {}\n".format(response.version))
    except:
        print("On connect failed...")


def on_connecting_callback(model: WebsocketProtocolModel) -> None:
    try:
        print("On connecting...")
        status, return_data = model.get(
            WSProtocolAttributes.callback_return_data)
        print("On connecting status: {}".format(status))

    except:
        print("On connecting failed")


def on_open_callback(model: WebsocketProtocolModel) -> None:

    try:
        print("Opening API connection")
        status, return_data = model.get(
            WSProtocolAttributes.callback_return_data)
        task_data = model.get(WSProtocolAttributes.callback_data_parameter)
        print("On open status: {}".format(status))
        print("Task data: {}".format(task_data))
        msg = 'WebSocket rocks!'.encode('utf-8')
        model.get(WSProtocolAttributes.send_message_callback)[1](
            payload=msg, is_binary=True)
    except:
        print("On open failed.")


def on_message_callback(model: WebsocketProtocolModel) -> None:
    try:
        print("On message")
        status, return_data = model.get(
            WSProtocolAttributes.callback_return_data)
        payload = return_data["payload"].decode("utf-8")
        is_binary = return_data["is_binary"]
        print("Getting message: {}".format(payload))
        print("Is binary: {}".format(is_binary))
        model.get(WSProtocolAttributes.send_close_callback)[1]("1000")
    except:
        print("On message failed.")


def on_close_callback(model: WebsocketProtocolModel) -> None:
    try:
        status, return_data = model.get(
            WSProtocolAttributes.callback_return_data)
        print("\nClosing API WebSocket connection")
        print('Websocket Connection closed:\n\tCode: {0}\n\tReason: {1}\n'
              '\twasClean: {2}'.format(return_data["code"], return_data["reason"],
                                       return_data["was_clean"]))
    except:
        print("On close failed")

########################## TEST DEFINITIONS #################################


def test_network_websocket_connection() -> None:
    """
    Tests the websocket_connect method of the network class.

    Tests:
        1. Use valid params to connect to the websocket server.
        2. Use invalid params to try and connect with the server.

    Returns:
        (bool): True if all the tests pass. False otherwise.
    """
    network = Network()
    num_tasks = 50
    thread_count = 50
    tasks = list()
    ws_test_url = "wss://echo.websocket.org"
    ws_test_headers = {}
    callbacks = {
        "on_connect": on_connect_callback,
        "on_connecting": on_connecting_callback,
        "on_message": on_message_callback,
        "on_open": on_open_callback,
        "on_close": on_close_callback}
    for i in range(num_tasks):
        tasks.append("Task {}".format(i))
    # Running request both as daemon and not daemon.
    assert network.websocket_connect(
        url=ws_test_url, headers=ws_test_headers, num_threads=thread_count,
        tasks_data=tasks, is_daemon=True, callbacks=callbacks)


def test_network_websocket_connection_bad_threads() -> None:
    """
    Tests the websocket_connect method of the network class.

    Tests:
        1. Use invalid thread param to try and connect with the server.

    Returns:
        (bool): True if all the tests pass. False otherwise.
    """
    network = Network()
    num_tasks = 50
    thread_count = 0
    tasks = list()
    ws_test_url = "wss://echo.websocket.org"
    ws_test_headers = {}
    callbacks = {
        "on_connect": on_connect_callback,
        "on_connecting": on_connecting_callback,
        "on_message": on_message_callback,
        "on_open": on_open_callback,
        "on_close": on_close_callback}
    for i in range(num_tasks):
        tasks.append("Task {}".format(i))
    assert not network.websocket_connect(
        url=ws_test_url, headers=ws_test_headers, num_threads=thread_count,
        tasks_data=tasks, is_daemon=True, callbacks=callbacks)


def test_network_websocket_connection_bad_callback() -> None:
    """
    Tests the websocket_connect method of the network class.

    Tests:
        1. Use invalid callback param to try and connect with the server.

    Returns:
        (bool): True if all the tests pass. False otherwise.
    """
    network = Network()
    num_tasks = 50
    thread_count = 50
    tasks = list()
    ws_test_url = "wss://echo.websocket.org"
    ws_test_headers = {}
    callbacks = {
        "bad": on_connect_callback,
        "on_connecting": on_connecting_callback,
        "on_message": on_message_callback,
        "on_open": on_open_callback,
        "on_close": on_close_callback}
    for i in range(num_tasks):
        tasks.append("Task {}".format(i))
    assert not network.websocket_connect(
        url=ws_test_url, headers=ws_test_headers, num_threads=thread_count,
        tasks_data=tasks, is_daemon=True, callbacks=callbacks)


# TODO: This test does not run because WS_factory cannot validate URLS for wss.
#       Uncomment after fixing the issue
# def test_network_websocket_connection_bad_url() -> None:
#     """
#     Tests the websocket_connect method of the network class.

#     Tests:
#         1. Use invalid url param to try and connect with the server.

#     Returns:
#         (bool): True if all the tests pass. False otherwise.
#     """
#     network = Network()
#     num_tasks = 50
#     thread_count = 50
#     tasks = list()
#     ws_test_url = "wss://foobar.org"
#     ws_test_headers = {}
#     callbacks = {
#         "on_connect": on_connect_callback,
#         "on_connecting": on_connecting_callback,
#         "on_message": on_message_callback,
#         "on_open": on_open_callback,
#         "on_close": on_close_callback}
#     for i in range(num_tasks):
#         tasks.append("Task {}".format(i))
#     assert not network.websocket_connect(
#         url=ws_test_url, headers=ws_test_headers, num_threads=thread_count,
#         tasks_data=tasks, is_daemon=True, callbacks=callbacks)

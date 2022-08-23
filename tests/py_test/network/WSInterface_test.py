# Standard library imports
from queue import Queue
# Local imports
from Src.components.network import WebsocketProtocolModel, WSInterface,\
    WSProtocolAttributes

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

def test_WSInterface_set() -> None:
    """
    Tests all setters for WSInterface.

    Tests:
        1. Provide valid values for all setters.
        2. Provide invalid values for all setters.

    Returns:
        (bool): True if all the tests pass. False otherwise.
    """
    ws_test_url = "wss://echo.websocket.org"
    ws_test_headers = {}
    data_queue = Queue()
    data_queue.put(("Test"))
    callbacks = {
        "on_connect": on_connect_callback,
        "on_connecting": on_connecting_callback,
        "on_message": on_message_callback,
        "on_open": on_open_callback,
        "on_close": on_close_callback}
    ws_interface = WSInterface(ws_test_url, ws_test_headers)
    assert ws_interface.set_num_threads(5) and \
        ws_interface.set_callbacks(callbacks) and \
        ws_interface.set_data_queue(data_queue) and \
        not ws_interface.set_num_threads(2000) and \
        not ws_interface.set_callbacks({})


def test_WSInterface_set_bad_callbacks() -> None:
    """
    Tests all callback setter for WSInterface

    Tests:
        1. Pass calback data that has invalid keys
        2. Confirm set is unsuccesful

    Returns:
        (bool): True if all the tests pass. False otherwise.
    """
    ws_test_url = "wss://echo.websocket.org"
    ws_test_headers = {}
    callbacks = {
        "bad": on_connect_callback,
        "on_connecting": on_connecting_callback,
        "on_message": on_message_callback,
        "on_open": on_open_callback,
        "on_close": on_close_callback}

    ws_interface = WSInterface(ws_test_url, ws_test_headers)
    assert not ws_interface.set_callbacks(callbacks)


def test_WSInterface_get() -> None:
    """
    Tests all getters in WSInterface.

    Tests:
        1. Ensure that get_configurations returns a valid dictionary.
        2. Ensure that the expected keys are returned only.

    Returns:
        (bool): True if all the tests pass. False otherwise.
    """
    expected_keys = [
        "factory_threads",
        "max_allowed_threads",
        "factory_configurations"]
    ws_test_url = "wss://echo.websocket.org"
    ws_test_headers = {}
    ws_interface = WSInterface(ws_test_url, ws_test_headers)
    configs = ws_interface.get_configurations()
    assert type(configs) == dict and \
        len(configs.keys()) == len(expected_keys) and \
        all([k for k in configs.keys() if k in expected_keys])


# TODO: The tests below are not working because the on_connect call does
#       not execute. This needs to be investigated.

# def test_WSInterface_open_connection() -> None:
#     """
#     Tests the open_connection_until_complete WSInterface class that uses
#     the WSInterfaceProtocol and WSInterfaceFactory.

#     Tests:
#         1. Set up a valid connection with callbacks that handle exceptions as
#             not a daemon (multi-threaded).
#         2. Set up a valid connection with callbacks that handle exceptions as
#             a daemon (multi-threaded).

#     Returns:
#         (bool): True if all the tests pass. False otherwise.
#     """
#     # Test 1.
#     num_queue_items = 50
#     thread_count = 50
#     ws_test_url = "wss://echo.websocket.org"
#     ws_test_headers = {}
#     callbacks = {
#         "on_connect": on_connect_callback,
#         "on_connecting": on_connecting_callback,
#         "on_message": on_message_callback,
#         "on_open": on_open_callback,
#         "on_close": on_close_callback}
#     daemon_test_queue = Queue()
#     test_queue = Queue()
#     for i in range(num_queue_items):
#         daemon_test_queue.put(("Test string {}".format(i)))
#         test_queue.put(("Test string {}".format(i)))

#     # Create websocket interface interface instance
#     ws_interface = WSInterface(ws_test_url, ws_test_headers)
#     ws_interface.set_num_threads(thread_count)
#     ws_interface.set_data_queue(test_queue)
#     ws_interface.set_callbacks(callbacks)
#     # Starting connection
#     success_1 = ws_interface.open_connection_until_complete(False)
#     # Re-adding daemon tasks and restarting WSInterface as a daemon
#     ws_interface.set_data_queue(daemon_test_queue)
#     success_2 = ws_interface.open_connection_until_complete(True)
#     assert success_1 and success_2


# def test_WSInterface_open_connection_valid_no_daemon() -> None:
#     """
#     Tests the open_connection_until_complete WSInterface class that uses
#     the WSInterfaceProtocol and WSInterfaceFactory.

#     Tests:
#         1. Set up a valid connection with callbacks that handle exceptions as
#             not a daemon (multi-threaded).

#     Returns:
#         (bool): True if all the tests pass. False otherwise.
#     """
#     num_queue_items = 10
#     thread_count = 10
#     ws_test_url = "wss://echo.websocket.org"
#     ws_test_headers = {}
#     callbacks = {
#         "on_connect": on_connect_callback,
#         "on_connecting": on_connecting_callback,
#         "on_message": on_message_callback,
#         "on_open": on_open_callback,
#         "on_close": on_close_callback}
#     daemon_test_queue = Queue()
#     test_queue = Queue()
#     for i in range(num_queue_items):
#         daemon_test_queue.put(("Test string {}".format(i)))
#         test_queue.put(("Test string {}".format(i)))
#     ws_interface = WSInterface(ws_test_url, ws_test_headers)
#     ws_interface.set_num_threads(thread_count)
#     ws_interface.set_data_queue(test_queue)
#     ws_interface.set_callbacks(callbacks)
#     success = ws_interface.open_connection_until_complete(False)
#     assert success


# def test_WSInterface_open_connection_valid_daemon() -> None:
#     """
#     Tests the open_connection_until_complete WSInterface class that uses
#     the WSInterfaceProtocol and WSInterfaceFactory.

#     Tests:
#         1. Set up a valid connection with callbacks that handle exceptions as
#             a daemon (multi-threaded).

#     Returns:
#         (bool): True if all the tests pass. False otherwise.
#     """
#     num_queue_items = 50
#     thread_count = 50
#     ws_test_url = "wss://echo.websocket.org"
#     ws_test_headers = {}
#     callbacks = {
#         "on_connect": on_connect_callback,
#         "on_connecting": on_connecting_callback,
#         "on_message": on_message_callback,
#         "on_open": on_open_callback,
#         "on_close": on_close_callback}
#     daemon_test_queue = Queue()
#     test_queue = Queue()
#     for i in range(num_queue_items):
#         daemon_test_queue.put(("Test string {}".format(i)))
#         test_queue.put(("Test string {}".format(i)))
#     ws_interface = WSInterface(ws_test_url, ws_test_headers)
#     ws_interface.set_num_threads(thread_count)
#     ws_interface.set_data_queue(test_queue)
#     ws_interface.set_callbacks(callbacks)
#     ws_interface.set_data_queue(daemon_test_queue)
#     success = ws_interface.open_connection_until_complete(True)
#     assert success

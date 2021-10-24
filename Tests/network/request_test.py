# Local imports
from Src.components.network import Request

############################### GLOBALS #####################################

########################## TEST DEFINITIONS #################################


def test_request_send_request() -> None:
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
        "params": {},
        "data": {},
        "json": {},
        "auth": {},
        "headers": {}}
    # Using postman urls for testing different request types
    get_url = "https://postman-echo.com/get?foo1=bar1&foo2=bar2"
    options_url = "https://postman-echo.com/get?foo1=bar1&foo2=bar2"
    post_url = "https://postman-echo.com/post"
    put_url = "https://postman-echo.com/put"
    patch_url = "https://postman-echo.com/patch"
    delete_url = "https://postman-echo.com/delete"
    invalid_url = "https://invalid.com"
    # Running requests
    results["GET"] = request.send_request("GET", get_url, empty_data_dict)
    results["OPTIONS"] = request.send_request(
        "OPTIONS", options_url, empty_data_dict)
    results["POST"] = request.send_request("POST", post_url, empty_data_dict)
    results["PUT"] = request.send_request("PUT", put_url, empty_data_dict)
    results["PATCH"] = request.send_request(
        "PATCH", patch_url, empty_data_dict)
    results["DELETE"] = request.send_request(
        "DELETE", delete_url, empty_data_dict)
    # All requests must return True and have status code 200.
    # Checks Invalid url
    assert all([v[0] for v in results.values()]) and \
        all([v[1]["status_code"] == 200 for v in results.values()]) and \
        not request.send_request("GET", invalid_url, empty_data_dict)[0] and \
        not request.send_request("GET", get_url, {"invalid key": None})[0] and \
        not request.send_request("GET", invalid_url, {"invalid key": None})[0]


def test_request_send_request_get() -> None:
    """
    Tests send request method in Request.

    Tests:
        1. Send GET request with no data and valid url

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    request = Request()
    empty_data_dict = {
        "params": {},
        "data": {},
        "json": {},
        "auth": {},
        "headers": {}}

    get_url = "https://postman-echo.com/get?foo1=bar1&foo2=bar2"
    success, req_dict = request.send_request("GET", get_url, empty_data_dict)
    assert success and req_dict["status_code"] == 200


def test_request_send_request_post() -> None:
    """
    Tests send request method in Request.

    Tests:
        1. Send POST request with no data and valid url

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    request = Request()
    empty_data_dict = {
        "params": {},
        "data": {},
        "json": {},
        "auth": {},
        "headers": {}}
    post_url = "https://postman-echo.com/post"
    success, req_dict = request.send_request("POST", post_url, empty_data_dict)
    assert success and req_dict["status_code"] == 200


def test_request_send_request_options() -> None:
    """
    Tests send request method in Request.

    Tests:
        1. Send OPTIONS request with no data and valid url

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    request = Request()
    empty_data_dict = {
        "params": {},
        "data": {},
        "json": {},
        "auth": {},
        "headers": {}}
    options_url = "https://postman-echo.com/get?foo1=bar1&foo2=bar2"
    success, req_dict = request.send_request(
        "OPTIONS", options_url, empty_data_dict)
    assert success and req_dict["status_code"] == 200


def test_request_send_request_put() -> None:
    """
    Tests send request method in Request.

    Tests:
        1. Send PUT request with no data and valid url

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    request = Request()
    empty_data_dict = {
        "params": {},
        "data": {},
        "json": {},
        "auth": {},
        "headers": {}}
    put_url = "https://postman-echo.com/put"
    success, req_dict = request.send_request("PUT", put_url, empty_data_dict)
    assert success and req_dict["status_code"] == 200


def test_request_send_request_patch() -> None:
    """
    Tests send request method in Request.

    Tests:
        1. Send PATCH request with no data and valid url

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    request = Request()
    empty_data_dict = {
        "params": {},
        "data": {},
        "json": {},
        "auth": {},
        "headers": {}}
    patch_url = "https://postman-echo.com/patch"
    success, req_dict = request.send_request(
        "PATCH", patch_url, empty_data_dict)
    assert success and req_dict["status_code"] == 200


def test_request_send_request_delete() -> None:
    """
    Tests send request method in Request.

    Tests:
        1. Send DELETE request with no data and valid url

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    request = Request()
    empty_data_dict = {
        "params": {},
        "data": {},
        "json": {},
        "auth": {},
        "headers": {}}
    delete_url = "https://postman-echo.com/delete"
    success, req_dict = request.send_request(
        "DELETE", delete_url, empty_data_dict)
    assert success and req_dict["status_code"] == 200


def test_request_send_bad_request_invalid_url() -> None:
    """
    Tests send request method in Request.

    Tests:
        1. Send request with invalid url
        2. Confirm request was unsuccessful

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    request = Request()
    empty_data_dict = {
        "params": {},
        "data": {},
        "json": {},
        "auth": {},
        "headers": {}}
    invalid_url = "https://invalid.com"
    success, _ = request.send_request("GET", invalid_url, empty_data_dict)
    assert not success


def test_request_send_bad_request_invalid_keys() -> None:
    """
    Tests send request method in Request.

    Tests:
        1. Send request with invalid data keys
        2. Confirm request was unsuccessful

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    request = Request()
    invalid = {
        "bad": {},
        "data": {},
        "json": {},
        "auth": {},
        "headers": {}}
    valid_url = "https://postman-echo.com/get?foo1=bar1&foo2=bar2"
    success, _ = request.send_request("GET", valid_url, invalid)
    assert not success


def test_request_send_bad_request_invalid_url_keys() -> None:
    """
    Tests send request method in Request.

    Tests:
        1. Send request with invalid data keys and invalid url
        2. Confirm request was unsuccessful

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    request = Request()
    invalid = {
        "bad": {},
        "data": {},
        "json": {},
        "auth": {},
        "headers": {}}
    invalid_url = "https://invalid.com"
    success, _ = request.send_request("GET", invalid_url, invalid)
    assert not success


def test_request_send_bad_request_invalid_request_type() -> None:
    """
    Tests send request method in Request.

    Tests:
        1. Send request with invalid request type
        2. Confirm request was unsuccessful

    Result:
        (bool): True if all the tests pass. False otherwise.
    """
    request = Request()
    invalid = {
        "params": {},
        "data": {},
        "json": {},
        "auth": {},
        "headers": {}}
    valid_url = "https://postman-echo.com/get?foo1=bar1&foo2=bar2"
    success, req_dict = request.send_request("BAD_GET", valid_url, invalid)
    assert not success and all([v == None for v in req_dict.values()])

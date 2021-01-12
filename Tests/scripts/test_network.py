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

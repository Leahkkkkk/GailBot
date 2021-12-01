# Standard library imports 
from typing import Dict, Tuple
# Third party imports 
import requests
import validators
from copy import deepcopy

class Request:
    """
    Wrapper that allows HTTP requests to be made.

    Params:
        REQUEST_TYPES (Tuple[str]): Types of http requests that are accepted.
    """
    REQUEST_TYPES = ("GET","OPTIONS","HEAD","POST","PUT","PATCH","DELETE")

    def __init__(self, timeout : int = 60, allow_redirects : bool = True,
            verify : bool = True ) -> None:
        """
        Args:
            timeout (int): Time after which request times out. 60 seconds default.
            allow_redirects (bool): True to be redirected by server. False otherwise.
            verify (bool): True to verify server contact. False otherwise.
        """
        # Function mappings for requests 
        self.methods = {
            "GET" : self._get,
            "OPTIONS" : self._options,
            "HEAD" : self._head,
            "POST" : self._post,
            "PUT" : self._put,
            "PATCH" : self._patch,
            "DELETE" : self._delete}
        # Parameters to configure a request.
        self.request_params = {
            "timeout" : timeout,
            "allow_redirects" : allow_redirects,
            "verify" : verify}
        # Tuple defining the keys required to be in data dictionary for a request.
        self.data_keys = ("params", "data", "json", "auth", "headers")
        # Defines the keys that will be in a response from a Request object
        self.response_keys = (
            "content","apparent_encoding" ,"cookies" ,"time_elapsed" ,
            "response_encoding", "is_redirect", "response_ok", "reason",
            "status_code", "response_url")

    def send_request(self, request_type : str, url : str, data : Dict) \
            -> Tuple[bool, Dict]:
        """
        Sends an HTTP request of the defined type to the specified url.

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
        
        Returns:
            Tuple[bool, Dict]: 
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

        request_type = request_type.upper()
        response = self._generate_response(None)
        is_success = False 
        # The request type and url need to be valid 
        if not request_type in self.REQUEST_TYPES or \
                not self._is_valid_url(url):
            return (is_success, response)
        # Preparing request parameters 
        is_prepared, params = self._prepare_request_args(data)
        if is_prepared:
            is_success, request_response = \
                self.methods[request_type](url,params)
            if is_success:
                response = self._generate_response(request_response)
        return (is_success, response)

        
    ############################ PRIVATE METHODS ###########################

    #### HTTP Methods 

    def _get(self, url : str, kwargs : Dict) -> Tuple[bool,requests.Response]:
        """
        Send a GET request to the specified url with the provided kwargs
        
        Args:
            url (str): Url to send request to.
            kwargs (Dict): Keyword arguments to be passed
            
        Returns:
            (Tuple[bool,requests.Response]): 
                bool is True if the request if successful. False otherwise.
                requests.Response object returned as a result of the request.
        """
        try:
            return (True,requests.get(url,**kwargs))
        except:
            return (False, None)

    def _options(self, url : str, kwargs : Dict) -> Tuple[bool,requests.Response]:
        """
        Send an OPTIONS request to the specified url with the provided kwargs
        
        Args:
            url (str): Url to send request to.
            kwargs (Dict): Keyword arguments to be passed
            
        Returns:
            (Tuple[bool,requests.Response]): 
                bool is True if the request if successful. False otherwise.
                requests.Response object returned as a result of the request. 
                This object is None if the request fails.
        """
        try:
            return (True, requests.options(url, **kwargs))
        except:
            return (False, None)
            

    def _head(self, url : str, kwargs : Dict) -> Tuple[bool,requests.Response]:
        """
        Send a HEAD request to the specified url with the provided kwargs
        
        Args:
            url (str): Url to send request to.
            kwargs (Dict): Keyword arguments to be passed
            
        Returns:
            (Tuple[bool,requests.Response]): 
                bool is True if the request if successful. False otherwise.
                requests.Response object returned as a result of the request.
                This object is None if the request fails.
        """
        try:
            return (True,requests.head(url, **kwargs))
        except:
            return (False, None)

    def _post(self, url : str, kwargs : Dict) -> Tuple[bool,requests.Response]:
        """
        Send a POST request to the specified url with the provided kwargs
        
        Args:
            url (str): Url to send request to.
            kwargs (Dict): Keyword arguments to be passed
            
        Returns:
            (Tuple[bool,requests.Response]): 
                bool is True if the request if successful. False otherwise.
                requests.Response object returned as a result of the request.
                This object is None if the request fails.
        """
        try:
            return (True,requests.post(url, **kwargs))
        except:
            return (False, None)

    def _put(self, url : str, kwargs : Dict) -> Tuple[bool,requests.Response]:
        """
        Send a PUT request to the specified url with the provided kwargs
        
        Args:
            url (str): Url to send request to.
            kwargs (Dict): Keyword arguments to be passed
            
        Returns:
            (Tuple[bool,requests.Response]): 
                bool is True if the request if successful. False otherwise.
                requests.Response object returned as a result of the request.
                This object is None if the request fails.
        """
        try:
            return (True,requests.put(url, **kwargs))
        except:
            return (False, None)

    def _patch(self, url : str, kwargs : Dict) -> Tuple[bool,requests.Response]:
        """
        Send a PATCH request to the specified url with the provided kwargs
        
        Args:
            url (str): Url to send request to.
            kwargs (Dict): Keyword arguments to be passed
            
        Returns:
            (Tuple[bool,requests.Response]): 
                bool is True if the request if successful. False otherwise.
                requests.Response object returned as a result of the request.
                This object is None if the request fails.
        """
        try:
            return (True,requests.patch(url, **kwargs))
        except:
            return (False, None)

    def _delete(self, url : str, kwargs : Dict) -> Tuple[bool,requests.Response]:
        """
        Send a DELETE request to the specified url with the provided kwargs
        
        Args:
            url (str): Url to send request to.
            kwargs (Dict): Keyword arguments to be passed
            
        Returns:
            (Tuple[bool,requests.Response]): 
                bool is True if the request if successful. False otherwise.
                requests.Response object returned as a result of the request. 
                This object is None if the request fails.
        """
        try:
            return (True,requests.delete(url, **kwargs))
        except:
            return (False, None)

    #### Others 

    def _prepare_request_args(self,data : Dict) \
            -> Tuple[bool, Dict]:
        """
        Creates a request in the appropriate format that will be sent to the 
        http server.

        Args:
            data (Dict): Data that is sent with the request.
        
        Returns:
            (Tuple[bool, Dict]): 
                Bool is True if successfully created. False otherwise
                Dict contains the request that can be sent to the server.
        """
        # Ensure that the data dictionary has the correct keys. 
        for k in self.data_keys:
            if k not in data.keys():
                return (False, {})
        # Create dictionary to be passed as part of the http request.
        data.update(deepcopy(self.request_params))
        return (True, data)

    def _is_valid_url(self, url : str) -> bool:
        """
        Determines if the provided string is a valid url.

        Args:
            url (str)
        
        Returns:
            (bool): True if the string is a valid url. False otherwise.
        """
        return validators.url(url)

    def _generate_response(self, request_response : requests.Response) -> Dict:
        """
        Generates an object that can be returned after a request has been made.

        Args:
            request_response (requests.Response):
                Object returned by an http request.
        
        Returns:
            (Dict): Object that can be returned by the Requests class.
        """
        response = dict.fromkeys(self.response_keys)
        try:
            response["content"] = request_response.content
            response["apparent_encoding"] = request_response.apparent_encoding
            response["cookies"] = request_response.cookies
            response["time_elapsed"] = request_response.elapsed
            response["response_encoding"] = request_response.encoding
            response["is_redirect"] = request_response.is_redirect
            response["response_ok"] = request_response.ok,
            response["reason"] = request_response.reason
            response["status_code"] = request_response.status_code
            response["response_url"] = request_response.url
            return response
        # Case where the request_response is not of the expected type.
        except:
            return response






    
'''
File: Request.py
Project: GailBot GUI
File Created: 2023/04/01
Author: Siara Small  & Vivian Li
-----
Last Modified:2023/05/06
Modified By:  Siara Small  & Vivian Li
-----
Description: define the interface for Request object that can be handled by 
             controller 
'''
from abc import ABC
class Request(ABC):
    data  = None ## request data
    
    def succeed(self, data):
        """succeed continuation that takes in the response data, 
           will be called when the controller is able to acquire response 
           from gailbot api 

        Args:
            data (any): the response data

        """
        raise NotImplementedError

    def fail(self, msg: str):
        """failure continuation that takes in an error message, 
           will be called when the controller failed to acquire response 
           from gailbot api

        Args:
            msg (str): a string with the error information

        """
        raise NotImplementedError
'''
File: DataOrganizer.py
Project: GailBot GUI
File Created: 2023/04/01
Author: Siara Small  & Vivian Li
-----
Last Modified:2023/05/18
Modified By:  Siara Small  & Vivian Li
-----
Description:  base class for the organizer class 
'''
from abc import ABC
from gailbot.api import GailBot
from view.signal.interface import DataSignal
from view.signal.Request import Request
from gbLogger import makeLogger

class DataOrganizer(ABC):
    """base class for data organizer,subclass of this class will 
       handle gui signal by calling function from gailbot api ,
       and send the response back to the gui by calling continuation 
       function stored in an instance of Request object
    """
    def __init__(self, gbAPI: GailBot, signal: DataSignal) -> None:
        """ 

        Args:
            gbAPI (GailBot): an instance of gailbot api 
            signal (DataSignal): an instance of DataSignal that stores gui's 
                                 signals that send request to gailbot api 
                                 
        """
        self.gb = gbAPI
        self.logger = makeLogger()
        self.registerSignals(signal)
    
    def registerSignals(self, signal:DataSignal):
        """main function that connect request signals to handler functions

        Args:
            signal (DataSignal): an instance of DataSignal that contains 
                                 request signal sent by frontend gui
        """
        signal.postRequest.connect(self.postHandler)
        signal.deleteRequest.connect(self.deleteHandler)
        signal.getRequest.connect(self.getHandler)
        signal.editRequest.connect(self.editHandler)
        signal.viewSourceRequest.connect(self.viewSourceHandler)
        signal.getAllNameRequest.connect(self.getAllNamesHandler)
    
    def postHandler(self, request: Request):
        """handle request that post data to gailbot """
        raise NotImplementedError

    def deleteHandler(self, request: Request):
        """handle request that delete data from gailbot"""
        raise NotImplementedError

    def getHandler(self, request: Request):
        """ handle request that get data from gailbot """
        raise NotImplementedError
    
    def editHandler(self, request: Request):
        """ handle request that edit data stored in gailbot """
        raise NotImplementedError

    def viewSourceHandler(self, request: Request):
        """ handle request that ask for getting source file on disk """
        raise NotImplementedError
    
    def getAllNamesHandler(self, request: Request):
        """ handle request that ask for getting all data's names stored in gailbot 
            such as getting all setting profiles' names 
        """
        raise NotImplementedError
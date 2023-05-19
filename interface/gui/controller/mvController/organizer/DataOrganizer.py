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
from gbLogger import makeLogger

class DataOrganizer(ABC):
    def __init__(self, gbController: GailBot, signal: DataSignal) -> None:
        self.gb = gbController
        self.logger = makeLogger()
        self.registerSignals(signal)
    
    def registerSignals(self, signal:DataSignal):
       signal.postRequest.connect(self.postHandler)
       signal.deleteRequest.connect(self.deleteHandler)
       signal.getRequest.connect(self.getHandler)
       signal.editRequest.connect(self.editHandler)
       signal.viewSourceRequest.connect(self.viewSourceHandler)
       signal.getAllNameRequest.connect(self.getAllNamesHandler)
    
    def postHandler():
        raise NotImplementedError

    def deleteHandler():
        raise NotImplementedError

    def getHandler():
        raise NotImplementedError
    
    def editHandler():
        raise NotImplementedError

    def viewSourceHandler():
        raise NotImplementedError
    
    def getAllNamesHandler():
        raise NotImplementedError
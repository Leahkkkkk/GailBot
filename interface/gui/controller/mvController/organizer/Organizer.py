'''
File: Organizer.py
Project: GailBot GUI
File Created: 2023/04/01
Author: Siara Small  & Vivian Li
-----
Last Modified:2023/05/06
Modified By:  Siara Small  & Vivian Li
-----
Description: declare the interface for Organizer 
'''
from abc import ABC, abstractmethod
from gbLogger import makeLogger

class Organizer(ABC):
    def __init__(self, gb, profileSignal):
        self.logger = makeLogger()
        self.gb = gb
        self.registerSignal(profileSignal)

    @abstractmethod
    def registerSignal(self, signal):
        pass

    @abstractmethod
    def postHandler(self, postRequest):
        raise NotImplementedError()

    @abstractmethod
    def deleteHandler(self, deleteRequest):
        raise NotImplementedError()

    @abstractmethod
    def editHandler(self, editRequest):
        raise NotImplementedError()

    @abstractmethod
    def getHandler(self, getRequest):
        raise NotImplementedError()

    @abstractmethod
    def viewSourceHandler(self, viewRequest):
        raise NotImplementedError()

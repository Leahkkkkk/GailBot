'''
File: Controller.py
Project: GailBot GUI
File Created: Wednesday, 15th September 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Wednesday, 5th October 2022 5:24:18 pm
Modified By:  Siara Small  & Vivian Li
-----
'''
from typing import Set
import logging 

from controller.TranscribeController import TranscribeController
from controller.MVController import MVController
from model import Model
from view import MainWindow
from util import Logger
from PyQt6.QtCore import pyqtSlot, QObject, QThreadPool 

from PyQt6.QtCore import pyqtSignal, QObject

class Signal(QObject):
    """ a signal object that contains signal for communication between 
        backend transcription process and frontend view object"""
    fileProgress = pyqtSignal(tuple)
    restart = pyqtSignal()
    

class Controller(QObject):
    """ Controller for Gailbot GUI """
    def __init__(self):
        super().__init__()
        self.ModelObj = Model.Model()
        self.ThreadPool = QThreadPool()
        
        # database
        self.FileData = self.ModelObj.FileData
        self.ProfileData = self.ModelObj.ProfileData
        self.PluginData = self.ModelObj.PluginData
        
        # view object
        self.ViewObj = MainWindow.MainWindow(
            self.ModelObj.ProfileData.profilekeys)
    
        # connecting view and database
        self.MVController = MVController(
            self.ViewObj, 
            self.FileData, 
            self.ProfileData, 
            self.PluginData)
        
        # transcribe controller will only be initializes when user make a 
        # transcribe request 
        self.transcribeController = None
        self.signal = Signal()
       
    
    def _initLogger(self):
        """ initialize the loggier """
        logDisplay = self.ViewObj.getLogDisplayer()
        self.logHandler = Logger.ConsoleHandler(logDisplay)
        logging.getLogger().addHandler(self.logHandler)
        logging.getLogger().setLevel(logging.DEBUG)
        self.logger = Logger.makeLogger("B")
        self.logger.info("Initialize the controller")
        
 
    def run(self):
        """ Public function that run the GUI app """
        self._initLogger()
        self.handleViewSignal()
        self.ViewObj.show()
        self.MVController.exec()
        self.handleTanscribeSignal()
    
    def handleViewSignal(self):
        """ handling signal to change the interface content from view object  """
        self.ViewObj.viewSignal.restart.connect( self.restart
        )
        
    def restart(self):
        self.signal.restart.emit()
        logging.getLogger().removeHandler(self.logHandler)
        
    ###################   gailbot  handler #############################   
    def handleTanscribeSignal(self):
        """ handle signal from View that requests to transcrib the file"""
        self.ViewObj.fileTableSignals.transcribe.connect(self._transcribeFiles)
        self.signal.fileProgress.connect(self.FileData.updateFileProgress)
        
    @pyqtSlot(set)
    def _transcribeFiles(self, files: Set[str]):
        """ transcribing the files

        Args:
            files (Set[str]): a set of file keys that identify the files that
                              will be transcribed
        """
        self.logger.info(files)
        transcribeList = []
        # get the file object from the database
        for key in files: 
            fileData = self.ModelObj.FileData.getTranscribeData(key)
            transcribeList.append(fileData)
            
        # run Gailbot re
        self._runGailBot(transcribeList)
        
    def _runGailBot(self, files):
        """run gailbot on a separate thread 

        Args:
            files (List): a list of files stored in key data pair that will
                          be trancribed
        """
        self.transcribeController = TranscribeController(
            self.ThreadPool, 
            self.ViewObj, 
            files)
        self.transcribeController.runGailBot()
    
   
'''
File: Controller.py
Project: GailBot GUI
File Created: Wednesday, 15th September 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Wednesday, 5th October 2022 5:24:18 pm
Modified By:  Siara Small  & Vivian Li
-----
Description:
Main controller for the app 
Connect between the database, view object and the backend transcription process
'''
import sys
from typing import Set
import logging 

from controller.TranscribeController import TranscribeController
from controller.MVController import MVController
from model import Model
from view import MainWindow
from util import Logger

from PyQt6.QtCore import pyqtSlot, QObject, QThreadPool, pyqtSignal

class Signal(QObject):
    """ a signal object that contains signal for communication between 
        backend transcription process and frontend view object"""
    fileProgress = pyqtSignal(tuple)
    restart      = pyqtSignal()
    

class Controller(QObject):
    """ Controller for Gailbot GUI 
    
    Field:
    1. ModelObj     : the database with file, profile and plugin data 
    2. ThreadPool   : a threadpool to run backend function in parallel with 
                      front-end interface 
    3. ViewObj      : a view object that implement ths front end interface 
    4. MVController : a model view controller that connect front-end view and 
                      database
    5. Transcribe controller: a controller that connect transcription process 
                              with view object 
    
    Public Function: 
    run()    : driver function to run the entire application 
    restart(): send a signal to restart the app 
    
    """
    def __init__(self):
        super().__init__()
        self.ModelObj = Model.Model()
        self.ThreadPool = QThreadPool()
        self.ViewObj = MainWindow.MainWindow(
            self.ModelObj.ProfileData.profilekeys)
        self.MVController = MVController(
            self.ViewObj, 
            self.ModelObj.FileData, 
            self.ModelObj.ProfileData, 
            self.ModelObj.PluginData)
        # transcribe controller is initially null until user makes a transcribe 
        # request 
        self.transcribeController = None
        self.signal = Signal()
 
    def run(self):
        print("run controller")
        """ Public function that run the GUI app """
        self._initLogger()
        self._handleViewSignal()
        self.ViewObj.show()
        self.MVController.exec()
        self._handleTanscribeSignal()
    
    def _handleViewSignal(self):
        """ handling signal to change the interface content from view object  """
        self.ViewObj.viewSignal.restart.connect( self.restart
        )
        
    def restart(self):
        self.signal.restart.emit()
        logging.getLogger().removeHandler(self.logHandler)
        
    ###################   gailbot  handler #############################   
    def _handleTanscribeSignal(self):
        """ handle signal from View that requests to transcribe the file"""
        self.ViewObj.fileTableSignals.transcribe.connect(self._transcribeFiles)
        self.signal.fileProgress.connect(
            self.ModelObj.FileData.updateFileProgress)
        
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
            
        # run gailbot 
        self._runGailBot(transcribeList)
        
    def _runGailBot(self, files):
        """run gailbot on a separate thread 

        Args:
            files (List): a list of files stored in key data pair that will
                          be transcribed
        """
        self.transcribeController = TranscribeController(
            self.ThreadPool, 
            self.ViewObj, 
            files)
        self.transcribeController.runGailBot()
    
    def _initLogger(self):
        """ initialize the loggier """
        logDisplay = self.ViewObj.getLogDisplayer()
        self.logHandler = Logger.ConsoleHandler(logDisplay)
        logging.getLogger().addHandler(self.logHandler)
        logging.getLogger().setLevel(logging.DEBUG)
        self.logger = Logger.makeLogger("B")
        self.logger.info("Initialize the controller")
         
   
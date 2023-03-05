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
import glob
import os
from typing import Set, Tuple
import logging 
import time

from config.ConfigPath import BackEndDataPath
from model import Model, FileObj
from controller.TranscribeController import TranscribeController
from controller.MVController import MVController# TODO: why
from view import MainWindow
from view.components import WorkSpaceDialog
from util import Logger
from util.GailBotData import getWorkPath, FileManage

from gailbot.api import GailBot

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
        userRoot = self.launchApp()
        self.init_application(userRoot)
        self.run()
        
    def launchApp(self) -> str:
        try:
            if not os.path.exists(os.path.join(os.getcwd(), BackEndDataPath.workSpaceData)):
                pathDialog = WorkSpaceDialog()
                pathDialog.exec()
                userRoot = pathDialog.userRoot
            else:
                userRoot = getWorkPath().workSpace
            return userRoot
        except Exception as e:
            self.logger.error(e)
    
    def init_application(self, userRoot) -> bool:
        try:
            self.gb = GailBot(userRoot)
            self.Model = Model(self.gb)
            self.ViewObj = MainWindow.MainWindow(self.gb.get_available_settings())
            
            self.MVController = MVController(
                self.ViewObj, 
                self.Model.fileOrganizer, 
                self.Model.profileOrganizer, 
                self.Model.pluginOrganizer)
            
            self.ThreadPool = QThreadPool()
            
            self.transcribeController = None 
            self.signal = Signal
        except Exception as e:
            self.logger.error("Error in app initialization {e}")
            
        
    def run(self):
        """ Public function that run the GUI app """
        self._initLogger()
        self._handleViewSignal()
        self.ViewObj.show()
        self.MVController.exec()
        self._handleTanscribeSignal()
        self._clearLog()
    
    def _handleViewSignal(self):
        """ handling signal to change the interface content from view object  """
        self.ViewObj.viewSignal.restart.connect(self.restart)
        
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
            file_name, file  = self.ModelObj.FileData.getTranscribeData(key)
            profile = self.ModelObj.ProfileData.get_profile(file.Profile)
            transcribeList.append((file_name, file, profile))
            
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
         
    def _clearLog(self):
        """ clear the log that is  """
        currentTime = int(time.time())
        deleteTime = currentTime - FileManage.AUTO_DELETE_TIME
        logdir = getWorkPath().logFiles
        files = glob.iglob(os.path.join(logdir, "*.log"))
        for file in files:
            fileTime = int(os.path.getctime(file))
            if fileTime <= deleteTime :
                os.remove(file)
            
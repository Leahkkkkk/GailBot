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
import time
from controller.util.io import is_directory, delete
from view.signal.Request import Request
from controller.transcribeController import TranscribeController
from controller.mvController import MVController
from gbLogger import makeLogger
from view.config import getWorkPaths, getLogManagementData
from gailbot.api import GailBot
from view import ViewController
from PyQt6.QtCore import QObject, QThreadPool, pyqtSignal
class Signal(QObject):
    """ a signal object that contains signal for communication between
        backend transcription process and frontend view object"""
    restart      = pyqtSignal()

class Controller(QObject):
    """ Controller for Gailbot GUI

    Field:
    1. ModelObj     : the database with file, profile and plugin data
    2. threadPool   : a threadpool to run backend function in parallel with
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
        self.signal = Signal()
        
        # initialize the gailbot workspace
        workSpace = getWorkPaths()
        for path in workSpace.__dict__.values():
            if not is_directory(path):
                os.makedirs(path) 
        backendRoot = workSpace.backend 
        
        # create logger
        self.logger = makeLogger()
        self.logger.info(f"controller initialized")
        self.logger.info(backendRoot)
        
        # initialize the application
        self.initApp(backendRoot)

    def initApp(self, backendRoot) -> bool:
        try:
            # initialize gailbot
            self.gb = GailBot(backendRoot)
            assert self.gb
            self.logger.info("GailBot initialized")

            # initialize view object
            self.ViewObj = ViewController()
            assert self.ViewObj
            self.logger.info("View Object initialized")
            
            # initialize model view controller for dynamically changing view
            self.MVController = MVController(self.ViewObj, self.gb)
            assert self.MVController
            self.logger.info("MV Controller initialized")

            # initialize thread
            self.threadPool = QThreadPool()
            self.logger.info("Threadpool initialized")

            # initialize transcribe controller
            self.transcribeController = TranscribeController(
                self.threadPool, self.ViewObj, self.gb)
            assert self.transcribeController
            self.logger.info("Transcribe controller initialized")
        except Exception as e:
            self.logger.error(f"Error in app initialization {e}", exc_info=e)

    def run(self):
        """ Public function that run the GUI app """
        try:
            self.logger.info("start running application")
            self._handleViewSignal()
            self.logger.info("connect to view")
        except Exception as e:
            self.logger.error(f"error connecting to view {e}", exc_info=e)
        try:
            self.ViewObj.show()
            self.MVController.exec()
            self.logger.info("connect to model view controller")
            self._handleTranscribeSignal()
            self.logger.info("connect to transcribe signal")
        except Exception as e:
            self.logger.error(f"error running the app {e}", exc_info=e)
        self._clearLog()

    def clearCache(self):
        """ clear the cache of gailbot workspace, this will delete the entire 
            GailBot folder stored on the User's disk 
        """
        self.logger.info("clear cache handler activated")
        workSpace = getWorkPaths()
        for path in workSpace.__dict__.values():
            if is_directory(path):
                delete(path)
                os.makedirs(path, exist_ok=True) 
        self.gb.reset_workspace()
        self.restart()
        
    def restart(self):
        """ send signal to restart the application, the owner of controller
            class is expected to handle this signal by relaunching the application
        """
        self.signal.restart.emit()

    def _handleViewSignal(self):
        """ handling signal to change the interface content from view object  """
        self.ViewObj.getViewSignal().restart.connect(self.restart)
        self.ViewObj.getViewSignal().clearcache.connect(self.clearCache)

   
    ###################   gailbot  handler #############################
    def _handleTranscribeSignal(self):
        """ handle signal from View that requests to transcribe the file"""
        self.ViewObj.getTranscriptionSignal().transcribe.connect(self._runGailBot)
        
    
    def _runGailBot(self, transcribeRequest: Request):
        """run gailbot on a separate thread

        Args:
            files (List): a list of files stored in key data pair that will
                          be transcribed
        """
        try:
            self.transcribeController.runGailBot(transcribeRequest)
        except Exception as e:
            self.logger.error(f"error in running gailbot transcription:{e}", exc_info=e)

    def _clearLog(self):
        """ clear the log that is expired"""
        currentTime = int(time.time())
        deleteTime = currentTime - getLogManagementData().AUTO_DELETE_TIME * 24 * 60
        logdir = getWorkPaths().logFiles
        files = glob.iglob(os.path.join(logdir, "*.log"))
        for file in files:
            fileTime = int(os.path.getctime(file))
            if fileTime <= deleteTime :
                os.remove(file)

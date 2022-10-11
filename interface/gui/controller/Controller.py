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

from model import Model
from view import MainWindow
from util import Logger
from controller.Thread import DummyRunnable, GBRunnable

from PyQt6.QtCore import QThreadPool

class Controller:
    """ Controller for Gailbot GUI """
    def __init__(self):
        self.ModelObj = Model.Model()
        self.ViewObj = MainWindow.MainWindow(self,self.ModelObj.SettingModel.data)
        self.ViewObj.setFileModel(self.ModelObj.FileModel, 
                                  self.ModelObj.ConfirmFileModel,
                                  self.ModelObj.ProcessingFileModel,
                                  self.ModelObj.SuccessedFileMode)
        self.ThreadPool = QThreadPool()
        self.logger = Logger.makeLogger("Backend")
    
    def run(self):
        """ Public function that run the GUI app """
        self.ViewObj.show()
        
    
    def addFile(self, fileObj):
        """ handle user request to add a file
        Args: 
            fileinfo: a list of file object 
        """
        self.logger.info("")
        self.ModelObj.FileModel.addFileHandler(fileObj)
        
    def runGailBot(self, key):
        """ wrapper function to run GailBot """
        self.logger.info("")
        
        if self.ThreadPool.activeThreadCount() > 1:
            self.logger.warn("Thread Busy")
            self.ViewObj.busyThreadPool()
        else: 
            self._runGailBotFun(key)


    def cancelGailBot(self):
        """  cancel the GailBot thread from running """
        self.logger.info("")
        self.worker.kill()
        self._showUploadFile()
    
    def _runDummyGB(self, key:int):
        """ dummy test function to test thread performance """
        self.logger.info("")
        self.worker = DummyRunnable.Worker()
        self.worker.signals.start.connect(self._showInProgress)
        self.worker.signals.finished.connect(self._showFinished)
        self.worker.signals.killed.connect(self._showUploadFile)
        self.ThreadPool.start(self.worker)
   
    def _runGailBotFun(self, key:int):
        """run gailbot on a separate thread 

        Args:
            key (int): an index key that identify the file from the file 
                       dataabse
        """
        def chageTranscribeStatus():
            self.logger.info("")
            self.ModelObj.FileModel.changeToTranscribed(key)
            
        self.logger.info("")
        file = self.ModelObj.FileModel.getFile(key)
        self.worker = GBRunnable.Worker(file["name"], file["path"],key)
        print(file["name"], file["path"],key)
        self.worker.signals.start.connect(self._showInProgress)
        self.worker.signals.finished.connect(self._showFinished)
        self.worker.signals.finished.connect(chageTranscribeStatus)
        self.worker.signals.progress.connect(self._sendTranscribeProgressMsg)
        self.worker.signals.error.connect(self.ViewObj.TranscribeFailed)
        self.ThreadPool.start(self.worker)

    
    def _showInProgress(self):
        """ change to Transcribe in progress page  """
        self.logger.info("")
        self.ViewObj.showTranscribeInProgress()


    def _showFinished(self):
        """ change to finished page """
        self.logger.info("")
        self.ViewObj.showTranscribeSuccess()
    
    def _sendTranscribeProgressMsg(self, msg:str):
        """ display progress message from the GailBot thread on statusbar
        
        Args:
            msg(str): messagte to be displayed 
        """
        self.logger.info("")
        self.ViewObj.showStatusMsg(msg, 10000)
        if self.ThreadPool.activeThreadCount() <= 1:
            self.ViewObj.freeThread()
    
    def _showUploadFile(self):
        """ change to initial file upload page"""
        self.logger.info("")
        self.ViewObj.showFileUploadPage()



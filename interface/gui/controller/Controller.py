""" Gaibolt Controller

"""
from PyQt6.QtCore import *
from controller.Thread import DummyRunnable, GBRunnable
from view import MainWindow
from model import Model
from util import Logger

class Controller:
    def __init__(self):
        self.ModelObj = Model.Model()
        self.ViewObj = MainWindow.MainWindow(self, self.ModelObj.SettingModel.data,  self.ModelObj)
        self.ThreadPool = QThreadPool()
        self.logger = Logger.makeLogger("Backend")
    
    def run(self):
        self.ViewObj.show()
        
    """ @addfile """
    """ handle user request to add a file """
    def addfile(self, fileinfo):
        self.logger.info("")
        self.ModelObj.FileModel.addfilehandler(fileinfo[0])
       
    """ @runGailBot """
    """ wrapper function for testing running gailbot on separate thread/process """
    def runGailBot(self, key):
        self.logger.info("")
        
        if self.ThreadPool.activeThreadCount() > 1:
            self.logger.warn("Thread Busy")
            self.ViewObj.busyThreadPool()
        else: 
            self._runGailBotFun(key)


    """ @cancelGailBot """
    """ cancel the GailBot thread from running  """
    def cancelGailBot(self):
        self.logger.info("")
        self.worker.kill()
        self._showUploadFile()
    
    """ @runEventLoopThread """
    """ dummy test function to test thread performance  """
    def _runDummyGB(self, key:int):
        self.logger.info("")
        self.worker = DummyRunnable.Worker()
        self.worker.signals.start.connect(self._showInProgress)
        self.worker.signals.finished.connect(self._showFinished)
        self.worker.signals.killed.connect(self._showUploadFile)
        self.ThreadPool.start(self.worker)
   
    """ @runGailBotFun """
    """ run gailbot on a separate thread """ 
    def _runGailBotFun(self, key:int):
        def chageTranscribeStatus():
            self.logger.info("")
            self.ModelObj.FileModel.changeToTranscribed(key)
            
        self.logger.info("")
        file = self.ModelObj.FileModel.getfile(key)
        self.worker = GBRunnable.Worker(file["name"], file["path"],key)
        self.worker.signals.start.connect(self._showInProgress)
        self.worker.signals.finished.connect(self._showFinished)
        self.worker.signals.finished.connect(chageTranscribeStatus)
        self.worker.signals.progress.connect(self._sendTranscribeProgressMsg)
        self.worker.signals.error.connect(self.ViewObj.TranscribeFailed)
        self.ThreadPool.start(self.worker)


    """ @ShowInProgress """
    """ change to Transcribe in progress page  """
    def _showInProgress(self):
        self.logger.info("")
        self.ViewObj.showTranscribeInProgress()

    """ @ShowFinished """
    """ change to finished page """
    def _showFinished(self):
        self.logger.info("")
        self.ViewObj.showTranscribeSuccess()
    
    def _sendTranscribeProgressMsg(self, msg:str):
        self.logger.info("")
        self.ViewObj.showStatusMsg(msg, 10000)
        if self.ThreadPool.activeThreadCount() <= 1:
            self.ViewObj.freeThread()
    
    """ @showUploadFile """
    """ change to initial file upload page """
    def _showUploadFile(self):
        self.logger.info("")
        self.ViewObj.showFileUploadPage()

    """ run the app """

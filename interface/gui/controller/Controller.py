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
from re import A
from typing import Set

from model import Model
from view import MainWindow
from util import Logger
from controller.Thread import DummyRunnable, GBRunnable

from PyQt6.QtCore import QThreadPool, pyqtSignal, QObject

class Controller:
    """ Controller for Gailbot GUI """
    def __init__(self):
        self.ModelObj = Model.Model()
        self.ViewObj = MainWindow.MainWindow(
            self, 
            self.ModelObj.ProfileData.form,
            self.ModelObj.ProfileData.profilekeys)
        
        self.ThreadPool = QThreadPool()
        self.logger = Logger.makeLogger("Backend")
        self._connectViewToFileDB()
        self._connectFileDBToView()
        self._handleTanscribeSignal()
        self._connectViewToProfileDB()
        self._connectProfileDBToView()
    
    def run(self):
        """ Public function that run the GUI app """
        self.ViewObj.show()
    
    def _showInProgress(self):
        """ change to Transcribe in progress page  """
        self.logger.info("")
        self.ViewObj.showTranscribeInProgress()

    def _showFinished(self, key):
        """ change to finished page """
        self.logger.info("")
        self.ViewObj.showTranscribeSuccess()
        self.ViewObj.changeFileStatusToTranscribed(key)
    
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
    
    def _connectFileDBToView(self):
        dbSignal = self.ModelObj.FileData.signals
        profile = self.ModelObj.ProfileData
        view = self.ViewObj
        dbSignal.fileAdded.connect(view.addFileToTables)
        dbSignal.profileRequest.connect(profile.get)
        
    def _connectViewToFileDB(self):
        viewSignal = self.ViewObj.fileTableSignals
        db = self.ModelObj.FileData
        viewSignal.postFile.connect(db.post)
        viewSignal.delete.connect(db.delete)
        viewSignal.editFile.connect(db.edit)
        viewSignal.changeProfile.connect(db.editFileProfile)
        viewSignal.changeStatus.connect(db.editFileStatus)
        viewSignal.requestprofile.connect(db.requestSetting)

    def _handleTanscribeSignal(self):
        self.ViewObj.fileTableSignals.transcribe.connect(self._transcribeFiles)
    
    def _transcribeFiles(self, files: Set[str]):
        """ TODO: support transcribing multiple files and apply different setting data """
        self.logger.info(files)
        self.logger.info(len(files))
        for key in files: 
            fileData = self.ModelObj.FileData.getTranscribeData(key)
            key, name , path, output  = fileData
            self.logger.info(key)
            self.logger.info(name)
            self.logger.info(path)
            self.logger.info(output)
            #TODO: run gailbot 
    
            # self._runGailBot(name, path, output, key)

    def _runGailBot(self, name, path, output, key):
        """ wrapper function to run GailBot """
        self.logger.info("")
        print(self.ThreadPool.activeThreadCount())
        if self.ThreadPool.activeThreadCount() > 1:
            self.logger.warn("Thread Busy")
            self.ViewObj.busyThreadPool()
        else: 
            self._runGailBotFun(name, path, output, key)


    def cancelGailBot(self):
        """  cancel the GailBot thread from running """
        self.logger.info("")
        self.worker.kill()
        self._showUploadFile()
        
    def _runGailBotFun(self, name, path, output, key):
        """run gailbot on a separate thread 

        Args:
            key (int): an index key that identify the file from the file 
                       dataabse
        """
        print(name, path,output,key)
        self.worker = GBRunnable.Worker(name, path, output, key)
        self.worker.signals.start.connect(self._showInProgress)
        self.worker.signals.finished.connect(self._showFinished)
        self.worker.signals.progress.connect(self._sendTranscribeProgressMsg)
        self.worker.signals.error.connect(self.ViewObj.TranscribeFailed)
        self.ThreadPool.start(self.worker)
        
    def _connectViewToProfileDB(self):
        viewSignal = self.ViewObj.profileSignals
        db = self.ModelObj.ProfileData
        viewSignal.post.connect(db.post)
        viewSignal.get.connect(db.get)
        viewSignal.edit.connect(db.edit)
    
    def _connectProfileDBToView(self):
        dbSignal = self.ModelObj.ProfileData.signals
        profileView = self.ViewObj.MainStack.SettingPage
        fileView = self.ViewObj.MainStack.FileUploadPage.fileTable
        dbSignal.send.connect(profileView.loadProfile)
        dbSignal.profileAdded.connect(profileView.addProfile)
        dbSignal.profileAdded.connect(fileView.addProfile)
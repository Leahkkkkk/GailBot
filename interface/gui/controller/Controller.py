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

from model import Model
from view import MainWindow
from util import Logger
from controller.Thread import  GBRunnable
from controller.Signals import Signal

from PyQt6.QtCore import QThreadPool

class Controller:
    """ Controller for Gailbot GUI """
    def __init__(self):
        self.ModelObj = Model.Model()
        self.FileData = self.ModelObj.FileData
        self.ProfileData = self.ModelObj.ProfileData
        self.PluginData = self.ModelObj.PluginData
        self.ViewObj = MainWindow.MainWindow(
            self, 
            self.ModelObj.ProfileData.form,
            self.ModelObj.ProfileData.profilekeys)
        self.signal = Signal()
        
        self.ThreadPool = QThreadPool()
        self.logger = Logger.makeLogger("Backend")
        self._connectControllerToView()
        self._connectViewToFileDB()
        self._connectFileDBToView()
        self._handleTanscribeSignal()
        self._connectViewToProfileDB()
        self._connectProfileDBToView()
        self._connectPluginDBToView()
        self._connectViewToPluginDB()
    
    def run(self):
        """ Public function that run the GUI app """
        self.ViewObj.show()
    
    def _connectControllerToView(self):
        self.signal.busy.connect(
            self.ViewObj.busyThreadPool)
        self.signal.start.connect(
            self.ViewObj.showTranscribeInProgress)
        self.signal.finish.connect(
            self.ViewObj.showTranscribeSuccess)
        self.signal.killed.connect(
            self.ViewObj.showFileUploadPage)
        self.ViewObj.fileTableSignals.cancel.connect(
            self.cancelGailBot)
        self.signal.progress.connect(
            self._sendTranscribeProgressMsg
        )
        self.signal.error.connect(
            self.ViewObj.TranscribeFailed
        )
        self.signal.fileTranscribed.connect(
            self.FileData.editFileStatus)

    
    ################### connecting file database to file table ################ 
    def _connectFileDBToView(self):
        dbSignal = self.ModelObj.FileData.signals
        profile = self.ModelObj.ProfileData
        view = self.ViewObj
        dbSignal.fileAdded.connect(view.addFileToTables)
        dbSignal.profileRequest.connect(profile.get)
        dbSignal.fileUpdated.connect(view.updateFile)
        
    def _connectViewToFileDB(self):
        viewSignal = self.ViewObj.fileTableSignals
        db = self.ModelObj.FileData
        viewSignal.postFile.connect(db.post)
        viewSignal.delete.connect(db.delete)
        viewSignal.editFile.connect(db.edit)
        viewSignal.changeProfile.connect(db.editFileProfile)
        viewSignal.changeStatus.connect(db.editFileStatus)
        viewSignal.requestprofile.connect(db.requestSetting)

    ################### connecting plugin database to profole table ###########
    def _connectViewToPluginDB(self):
        viewSignal = self.ViewObj.profileSignals
        db = self.ModelObj.PluginData
        viewSignal.addPlugin.connect(db.post)
    
    def _connectPluginDBToView(self):
        dbSignal = self.ModelObj.PluginData.signals 
        pluginView = self.ViewObj.MainStack.ProfileSettingPage
        dbSignal.pluginAdded.connect(pluginView.addPluginHandler)

    ############  connecting the profile database to profile page #############       
    def _connectViewToProfileDB(self):
        viewSignal = self.ViewObj.profileSignals
        db = self.ModelObj.ProfileData
        viewSignal.post.connect(db.post)
        viewSignal.get.connect(db.get)
        viewSignal.edit.connect(db.edit)
    
    def _connectProfileDBToView(self):
        dbSignal = self.ModelObj.ProfileData.signals
        profileView = self.ViewObj.MainStack.ProfileSettingPage
        fileView = self.ViewObj.MainStack.FileUploadPage.fileTable
        dbSignal.send.connect(profileView.loadProfile)
        dbSignal.profileAdded.connect(profileView.addProfile)
        dbSignal.profileAdded.connect(fileView.addProfile)
        

        
    ##########   gailbot running hendler #################################    
    def _handleTanscribeSignal(self):
        self.ViewObj.fileTableSignals.transcribe.connect(self._transcribeFiles)
    
    def _transcribeFiles(self, files: Set[str]):
        """ transcribing the files

        Args:
            files (Set[str]): a set of file keys that identify the files that
                              will be transcribed
        """
        self.logger.info(files)
        self.logger.info(len(files))
        transcribeList = []
        for key in files: 
            fileData = self.ModelObj.FileData.getTranscribeData(key)
            transcribeList.append(fileData)
        if self.ThreadPool.activeThreadCount() > 1:
            self.logger.warn("Thread Busy")
            self.signal.busy.emit() # TODO: use pysgnal 
        else:
            self._runGailBot(transcribeList)
        
    def _runGailBot(self, files):
        """run gailbot on a separate thread 

        Args:
            key (int): a set of file keys that identify the files that
                              will be transcribed
        """
        self.logger.info(files)
        self.worker = GBRunnable.Worker(files, self.signal)
        self.signal.start.emit()
        self.ThreadPool.start(self.worker)


    def cancelGailBot(self):
        """  TODO: check this functions """
        self.logger.info("")
        self.worker.kill()
        # self._showUploadFile()
        
        
    #####################   TODO: change those function ################
    def _sendTranscribeProgressMsg(self, msg:str):
        """ display progress message from the GailBot thread on statusbar
        
        Args:
            msg(str): messagte to be displayed 
        """
        self.logger.info("")
        self.ViewObj.showStatusMsg(msg, 10000)
        if self.ThreadPool.activeThreadCount() <= 1:
            self.ViewObj.freeThread()
    
    
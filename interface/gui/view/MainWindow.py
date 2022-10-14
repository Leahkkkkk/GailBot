'''
File: MainWindow.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 1:45:53 pm
Modified By:  Siara Small  & Vivian Li
-----
'''

import os
import datetime

from util import Logger 
from view.components import (
    MainStack, 
    StatusBar, 
    MenuBar, 
    Console, 
    MsgBox
)

from controller. Controller import Controller
from model.FileItem import FileItem

from PyQt6.QtCore import QSize, QAbstractTableModel
from PyQt6.QtWidgets import QMainWindow, QFileDialog


class MainWindow(QMainWindow):
    """ mainwindow  of the GUI App"""
    def __init__(
        self, 
        controller: Controller, 
        settingdata: dict, 
    ):
        """initialzie mainwindow object 
        
        Args:
            controller (Controller)
            settingdata (dict)
            modelObj (Model)
        """
        
        super().__init__()
        self.setWindowTitle("My App")
        self.resize(900, 700)
        self.setMinimumSize(QSize(700, 600))
        self.setMaximumSize(QSize(1200, 900))
        self.resize(QSize(1000, 750))
        self.settingdata = settingdata
        self.MainStack = MainStack.MainStack(self.settingdata, parent=self)
        self.setCentralWidget(self.MainStack)
        self.controller = controller
        self.StatusBar = StatusBar.StatusBar()
        self.setStatusBar(self.StatusBar)
        self.MenuBar = MenuBar.ManuBar()
        self.setMenuBar(self.MenuBar)
        self.Console = Console.Console()
        self.logger = Logger.makeLogger("Frontend")
        
        self._connectSignal()
        self._connectController()

    """ Functions provided to controller """
    
    def setFileModel(self, fileModelFull: QAbstractTableModel, 
                           confirmModel: QAbstractTableModel,
                           progressModel:QAbstractTableModel,
                           successModel:QAbstractTableModel):
        
        self.MainStack.FileUploadPage.fileTable.setFileModel(fileModelFull, 
                                                             self.showSettingPage, 
                                                             self.createSettingPage, 
                                                             self.deleteFun)
        self.MainStack.ConfirmTranscribePage.fileTable.setFileModel(confirmModel,
                                                             self.showSettingPage, 
                                                             self.createSettingPage, 
                                                             self.deleteFun)
        self.MainStack.ConfirmTranscribePage.fileTable.addFirstAction(
            self.MainStack.ConfirmTranscribePage.toggleFileDetail)
        self.MainStack.TranscribeProgressPage.fileTable.setFileModel(progressModel,
                                                             self.showSettingPage, 
                                                             self.createSettingPage, 
                                                             self.deleteFun)
        
        self.MainStack.TranscribeSuccessPage.fileTable.setFileModel(successModel,
                                                             self.showSettingPage, 
                                                             self.createSettingPage, 
                                                             self.deleteFun)
      
        self.MainStack.ApplySetProgressPage.fileTable.setFileModel(progressModel,
                                                             self.showSettingPage, 
                                                             self.createSettingPage, 
                                                             self.deleteFun)
        
        self.MainStack.ApplySetSuccessPage.fileTable.setFileModel(successModel,
                                                             self.showSettingPage, 
                                                             self.createSettingPage, 
                                                             self.deleteFun)
    
    def deleteFun(self,fileKey):
        """ TODO: add function to delete file from file table """
        self.controller.deleteFile(fileKey)
        print(fileKey)
    
    def showSettingPage(self):
        """ go to the  setting page 
        TODO: add function to pass in setting data and reload the page dynamically 
        """
        self.MainStack.gotoSettingPage()
   
   
    def createSettingPage(self):
        """ got the setting page to create the new setting 
        TODO: add function to load setting page as default setting page  
        """
        self.MainStack.gotoSettingPage()
        
    def showTranscribeInProgress(self):
        """goes to transcribe in progress page"""
        self.MainStack.gotoTranscribeInProgress()
        
    def showTranscribeSuccess(self):
        """goes to trancription success page"""
        self.MainStack.gotoTranscribeSuccess()
    
    def showFileUploadPage(self):
        """goes to file upload page"""
        self.MainStack.gotoFileUploadPage()
    
    def busyThreadPool(self):
        """shows busy thread pool message"""
        self.msgBox = MsgBox.WarnBox("The GailBot is too busy to receive your request!")
    
    def showStatusMsg(self, msg, time=None):
        """shows status message"""
        self.StatusBar.showStatusMsg(msg, time)
    
    def freeThread(self):
        """clears thread message"""
        self.StatusBar.clearMessage()
    
    def TranscribeFailed(self, err:str):
        """shows transcription failed message"""
        self.msgBox = MsgBox.WarnBox(f"Transcription Failed, error: {err}", 
                                     self.showFileUploadPage)
        self.MainStack.TranscribeProgressPage.IconImg.stop()
        
    """ private function """
    def _connectSignal(self):
        """ connect to signal """
        self.MenuBar.OpenConsole.triggered.connect(lambda: self.Console.show())
        self.MenuBar.CloseConsole.triggered.connect(lambda: self.Console.hide())
        
    def _connectController(self):
        """ connect to controller """
        self.MainStack.FileUploadPage.uploadFileBtn.clicked.connect(self._addfile)
        self.MainStack.ConfirmTranscribePage.confirmBtn.clicked.connect(self._transcribe)
    
    def _addfile(self):
        """ add file to file database """
        fileDialog = QFileDialog(self)
        fileFilter = "*.txt *.wav *.png"
        fileDialog.setNameFilter(fileFilter)
        if fileDialog.exec():
            file = fileDialog.selectedFiles()
            if file:
                path = fileDialog.directoryUrl().toString()
                filePath = path[7:]
                fileObj = FileItem(file[0], filePath,"Default")
                key = self.controller.addFile(fileObj)
                self.MainStack.FileUploadPage.fileTable.addActionWidget( 
                                                            self.showSettingPage, 
                                                            self.createSettingPage, 
                                                            self.deleteFun,
                                                            key = key)
            else:
                return None
    
    def _transcribe(self):
        """ call controller to transcribe audio file"""
        indices = self.MainStack.FileUploadPage.fileTable.selectedIndexes()
        if indices:
            key = indices[0].row()
            self.controller.runGailBot(key)
        self.logger.info("")

    """ functions provided to child elements"""
    def confirmCancel(self):
        """ handle event when user tries to cancel the thread """
        self.logger.info("")
        self.controller.cancelGailBot()
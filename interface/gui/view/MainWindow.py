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


from util import Logger 
from view.components import (
    MainStack, 
    StatusBar, 
    MenuBar, 
    Console, 
)

from view import Signals
from view.widgets import MsgBox
from controller. Controller import Controller
from model.FileItem import FileItem
from PyQt6.QtCore import QSize, QAbstractTableModel
from PyQt6.QtWidgets import QMainWindow, QFileDialog



class MainWindow(QMainWindow):
    """ mainwindow  of the GUI App"""
    def __init__(
        self, 
        controller: Controller, 
        settingform:dict,
        settingkey: list
    ):
        """initialzie mainwindow object 
        
        Args:
            controller (Controller)
            settingform (dict)
        """
        super().__init__()
        self.fileTableSignals = Signals.FileSignals()
        self.profileSignals = Signals.ProfileSignals()
        
        self.setWindowTitle("GailBot")
        self.resize(900, 700)
        self.setMinimumSize(QSize(700, 600))
        self.setMaximumSize(QSize(1200, 900))
        self.resize(QSize(1000, 750))
    
        self.MainStack = MainStack.MainStack(
            settingform, 
            settingkey,
            self.fileTableSignals, 
            self.profileSignals,
            parent=self)
        
        
        self.setCentralWidget(self.MainStack)
        self.controller = controller
        self.StatusBar = StatusBar.StatusBar()
        self.setStatusBar(self.StatusBar)
        self.MenuBar = MenuBar.ManuBar()
        self.setMenuBar(self.MenuBar)
        self.Console = Console.Console()
        self.logger = Logger.makeLogger("Frontend")
        self._connectSignal()

    """ Functions provided to controller """
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

    """ functions provided to child elements"""
    def confirmCancel(self):
        """ handle event when user tries to cancel the thread """
        self.logger.info("")
        self.MainStack.gotoFileUploadPage()
        self.controller.cancelGailBot()
    
    def changeFileStatusToTranscribed(self,key):
        pass
        # self.MainStack.FileUploadPage.fileTable.changeToTranscribed(key)
    
    def addFileToTables(self, file:dict):
        self.MainStack.addFileToTables(file)
        
    def updateFile(self, data:tuple):
        self.MainStack.updateFile(data)
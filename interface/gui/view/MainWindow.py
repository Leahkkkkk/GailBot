'''
File: MainWindow.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 1:45:53 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: implement the main window for the GUI interface
'''
from typing import List 
import os 
import shutil
import glob

from util import Logger
from config.ConfigPath import BackEndDataPath
from view.components import (
    MainStack, 
    StatusBar, 
    MenuBar, 
    Console, 
)

from view import Signals
from view.components import WorkSpaceDialog
from view.widgets import MsgBox
from util.Style import Dimension
from util.Path import getProjectRoot
from util.GailBotData import getWorkPath
from util.Text import About


from PyQt6.QtCore import QSize, QObject, pyqtSignal
from PyQt6.QtWidgets import QMainWindow

class ViewSignals(QObject):
    restart = pyqtSignal()
    
class MainWindow(QMainWindow):
    """ mainwindow  of the GUI App"""
    def __init__(
        self, 
        settingkey: List [str ]
    ):
        """initialize mainWindow object 
        
        Args:
            settingkey: (List [str ]) a list of predefined setting profile names
        """
        super().__init__()
        self.fileTableSignals = Signals.FileSignals()
        self.profileSignals = Signals.ProfileSignals()
        self.viewSignal = ViewSignals()
        self.StatusBar = StatusBar.StatusBar()
        self.setStatusBar(self.StatusBar)
        self.MenuBar = MenuBar.ManuBar()
        self.setMenuBar(self.MenuBar)
        self.Console = Console.Console()
        self.logger = Logger.makeLogger("F")
        
        self.setWindowTitle(About.APP_TITTLE)
        self.setMinimumSize(QSize(Dimension.WIN_MIN_WIDTH, Dimension.WIN_MIN_HEIGHT))
        self.setMaximumSize(
            QSize(Dimension.WINMAXWIDTH, Dimension.WINMAXHEIGHT))

    
        self.MainStack = MainStack.MainStack(
            settingkey,
            self.fileTableSignals, 
            self.profileSignals,
            parent=self)
        
        self.setCentralWidget(self.MainStack)
        self.setContentsMargins(0,0,0,0)
        self._connectSignal()
        self._openWorkSpaceDialog()

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
    
    def showFileProgress(self, msg):
        self.fileTableSignals.progressChanged.emit(msg)
    
    def freeThread(self):
        """clears thread message"""
        self.StatusBar.clearMessage()
    
    def TranscribeFailed(self, err:str):
        """shows transcription failed message"""
        self.msgBox = MsgBox.WarnBox(f"Transcription Failed, error: {err}", 
                                     self.showFileUploadPage)
        self.MainStack.TranscribeProgressPage.IconImg.stop()
        
    def confirmCancel(self):
        """ handle event when user tries to cancel the thread """
        self.logger.info("")
        self.MainStack.gotoFileUploadPage()

    def addFileToTables(self, file:dict):
        """ add file to file upload table """
        self.MainStack.addFileToTables(file)
        
    def updateFile(self, data:tuple):
        """ update file information on file upload file """
        self.MainStack.updateFile(data)
    
    def getLogDisplayer(self):
        """ return the widget that display the logging message """
        return self.Console.LogBox
    
    def changeFiletoTranscribed(self, key:str):
        """ change the file status to be transcribed 
            currently delete the file from the table
        """
        self.MainStack.changeToTranscribed(key)
    
    def closeEvent(self, a0) -> None:
        super().closeEvent(a0)
        self._copylog()
        
    """ private function """
    def _connectSignal(self):
        """ connect to signal """
        self.MainStack.SystemSettingPage.signal.restart.connect(self._restart)
        self.MenuBar.OpenConsole.triggered.connect(lambda: self.Console.show())
        self.MenuBar.CloseConsole.triggered.connect(lambda: self.Console.hide())
        self.fileTableSignals.cancel.connect(self.confirmCancel)
    
    def _restart(self):
        """ restarting the app """
        self.viewSignal.restart.emit()
        self.hide()
        self.close()
    
    def _openWorkSpaceDialog(self):
        """ open a dialog to ask user for the path to work space directory """
        basedir = getProjectRoot()
        if not os.path.exists(os.path.join(basedir, BackEndDataPath.workSpaceData)):
            pathDialog = WorkSpaceDialog.WorkSpaceDialog()
            pathDialog.exec()

    def _copylog(self):
        """ copy log file to the frontend/logfiles folder """
        frontEndDir = getWorkPath().logFiles
        
        if not os.path.isdir(frontEndDir):
            os.makedirs(frontEndDir)
            
        files = glob.iglob(os.path.join(getProjectRoot(), "*.log"))
        for file in files:
            if os.path.isfile(file):
                name = os.path.basename(file)
                shutil.copy2(file, os.path.join(frontEndDir, name))
                os.remove(file)
    

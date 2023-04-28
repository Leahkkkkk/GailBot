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
from typing import List, Dict, Tuple
import logging 
from gbLogger import Logger
from view.components.Window import (
    MainStack, 
    StatusBar, 
    MenuBar, 
    Console, 
)
from view.util.ErrorMsg import WARN, ERR
from view.signal.signalObject import FileSignal, GBTranscribeSignal, GuiSignal

from view.widgets import WarnBox
from view.config.Style import Dimension
from view.config.Text import About
from config_frontend import FRONTEND_CONFIG_ROOT
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
    """ mainwindow  of the GUI App"""
    def __init__(
        self, 
    ):
        """initialize mainWindow object 
        
        Args:
            settingkey: (List [str ]) a list of predefined setting profile names
        """
        super().__init__()
        # initialize the main view controller 
        self.logger = Logger.makeLogger("F")
        self.logger.info(f"the frontend configuration file is stored at {FRONTEND_CONFIG_ROOT}")
        
        # initialize the signal
        self.fileTableSignals = FileSignal
        self.transcribeSignal = GBTranscribeSignal
        self.viewSignal = GuiSignal
        self.logger.info(f"signals initialized")
        
        # initialzie the menu bar and the footer
        self.StatusBar = StatusBar()
        self.setStatusBar(self.StatusBar)
        self.MenuBar = MenuBar()
        self.setMenuBar(self.MenuBar)
        self.Console = Console()
        self.logger.info("console initialized")
        self.setWindowTitle(About.APP_TITTLE)
        self.setMinimumSize(QSize(Dimension.WIN_MIN_WIDTH, Dimension.WIN_MIN_HEIGHT))
        self.setMaximumSize(QSize(Dimension.WINMAXWIDTH, Dimension.WINMAXHEIGHT))
        self.MainStack = MainStack() 
        self.logger.info("main stack initialized")
        self.setCentralWidget(self.MainStack)
        self.setContentsMargins(0,0,0,0)
        self._connectSignal()
        self._initLogger()

    def addAvailableSetting(self, profiles: List[Tuple[str, Dict]]):
        """ initialize available setting to interface"""
        try:
            self.MainStack.addAvailableSettings(profiles)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            self.showError(ERR.FAIL_TO.format("load setting"))
    
    def addAvailableEngineSettings(self, settings: List[Tuple[str, Dict]]):
        """ initialize available setting to interface"""
        try:
            self.MainStack.addAvailableEngines(settings)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            self.showError(ERR.FAIL_TO.format("load setting"))
    
    def addAvailablePluginSuites(self, pluginSuites: List[Tuple[str, Dict[str, str]]]):
        """ initialize available plugin to interface """
        try:
            self.MainStack.addAvailablePluginSuites(pluginSuites)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            self.showError(ERR.FAIL_TO.format("load plugin"))
  
    """ Functions provided to controller """
    def showTranscribeInProgress(self):
        """goes to transcribe in progress page"""
        try:
            self.MainStack.gotoTranscribeInProgress()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            self.showError(ERR.FAIL_TO.format("load transcription in progress page"))
            
    def showTranscribeSuccess(self):
        """goes to trancription success page"""
        try:
            self.MainStack.gotoTranscribeSuccess()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            self.showError(ERR.FAIL_TO.format("load transcription success page"))
    
    def showFileUploadPage(self):
        """goes to file upload page"""
        try:
            self.MainStack.gotoFileUploadPage()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            self.showError(ERR.FAIL_TO.format("load file upload page"))
    
    def showStatusMsg(self, msg, time=None):
        """shows status message"""
        try:
            self.StatusBar.showStatusMsg(msg, time)
        except Exception as e:
            self.showError(ERR.FAIL_TO.format("status bar message"))
    
    def showFileProgress(self, progress: Tuple[str, str]):
        """show file progress in transcribe in progress page"""
        try:
            self.transcribeSignal.updateProgress.emit(progress)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            self.showError(ERR.FAIL_TO.format("show file progress"))
            
    def freeThread(self):
        """clears thread message"""
        try:
            self.StatusBar.clearMessage()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            self.showError(ERR.FAIL_TO.format("clear the thread"))
    
        
    def changeFiletoTranscribed(self, key:str):
        """ change the file status to be transcribed 
            currently delete the file from the table
        """
        try:
            self.MainStack.changeToTranscribed(key)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            self.showError(ERR.FAIL_TO.format("change the file status"))
           
            
    def removeFile(self, key:str):
        """ change the file status to be transcribed 
            currently delete the file from the table
        """
        try:
            self.MainStack.removeFile(key)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            self.showError(ERR.FAIL_TO.format("change the file status"))
    
    def closeEvent(self, a0) -> None:
        """  called when application closes """
        try:
            super().closeEvent(a0)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            self.showError(ERR.FAIL_TO.format("relaunch gailbot, please restart application"))
        
    def showError(self, errorMsg:str):
        WarnBox(errorMsg) 
    
    """ private function """
    def _connectSignal(self):
        """ connect to signal """
        self.MainStack.SettingPage.SysPage.signal.restart.connect(self._restart)
        self.MainStack.SettingPage.SysPage.signal.clearCache.connect(
            lambda: self.viewSignal.clearcache.emit())
        self.MenuBar.OpenConsole.triggered.connect(lambda: self.Console.show())
        self.MenuBar.CloseConsole.triggered.connect(lambda: self.Console.hide())
    
    def _restart(self):
        """ restarting the app """
        self.viewSignal.restart.emit()
        self.hide()
        self.close()

    def _initLogger(self):
        consoleLog = Logger.ConsoleHandler(self.Console.LogBox)
        logging.getLogger().addHandler(consoleLog)
        logging.getLogger().setLevel(logging.DEBUG) 
        
        
    
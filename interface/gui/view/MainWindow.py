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
from view.components import (
    MainStack, 
    StatusBar, 
    MenuBar, 
    Console, 
)
from view.components.PluginSuiteDetails import PluginSuiteDetails
from view.util.ErrorMsg import WARN, ERR
from view.Signals import FileSignals, ViewSignals, ProfileSignals, PluginSignals
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
        self.fileTableSignals = FileSignals()
        self.profileSignals = ProfileSignals()
        self.viewSignal = ViewSignals()
        self.pluginSignal = PluginSignals()
        self.logger.info(f"signals initialized")
        
        # initialzie the menu bar and the footer
        self.StatusBar = StatusBar.StatusBar()
        self.setStatusBar(self.StatusBar)
        self.MenuBar = MenuBar.ManuBar()
        self.setMenuBar(self.MenuBar)
        self.Console = Console.Console()
        self.logger.info("console initialized")
        self.setWindowTitle(About.APP_TITTLE)
        self.setMinimumSize(QSize(Dimension.WIN_MIN_WIDTH, Dimension.WIN_MIN_HEIGHT))
        self.setMaximumSize(QSize(Dimension.WINMAXWIDTH, Dimension.WINMAXHEIGHT))
        self.MainStack = MainStack.MainStack(
            self.fileTableSignals, 
            self.profileSignals, 
            self.pluginSignal)
        self.logger.info("main stack initialized")
        self.setCentralWidget(self.MainStack)
        self.setContentsMargins(0,0,0,0)
        self._connectSignal()
        self._initLogger()


    def addAvailableSetting(self, profileNames: List[str]):
        """ initialize available setting to interface"""
        try:
            self.MainStack.addAvailableSetting(profileNames)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            self.showError(ERR.FAIL_TO.format("load setting"))
    
    def addAvailablePluginSuites(self, pluginSuites: List[Tuple[str, Dict[str, str]]]):
        """ initialize available plugin to interface """
        try:
            for suite in pluginSuites:
                self.addPlugin(suite)
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
    
    def busyThreadPool(self):
        """shows busy thread pool message"""
        self.showError(WARN.BUSY_THREAD)
    
        
    def showStatusMsg(self, msg, time=None):
        """shows status message"""
        try:
            self.StatusBar.showStatusMsg(msg, time)
        except Exception as e:
            self.showError(ERR.FAIL_TO.format("status bar message"))
    
    def showFileProgress(self, progress: Tuple[str, str]):
        """show file progress in transcribe in progress page"""
        try:
            self.fileTableSignals.progressChanged.emit(progress)
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
    
    def TranscribeFailed(self, err:str):
        """shows transcription failed message"""
        self.msgBox = WarnBox(
            f"Transcription Failed, error: {err}", self.showFileUploadPage)
        self.MainStack.TranscribeProgressPage.IconImg.stop()
            
        
    def confirmCancel(self):
        """ handle event when user tries to cancel the thread """
        try:
            self.logger.info("")
            self.MainStack.gotoFileUploadPage()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            self.showError(ERR.FAIL_TO.format("cancel transcription"))

    def addFileToTables(self, file:dict):
        """ add file to file upload table """
        try:
            self.MainStack.addFileToTables(file)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            self.showError(ERR.FAIL_TO.format("upload file"))
            
    def updateFile(self, data:tuple):
        """ update file information on file upload file """
        try:
            self.MainStack.updateFile(data)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            self.showError(ERR.FAIL_TO.format("update file information"))
            
    def changeFiletoTranscribed(self, key:str):
        """ change the file status to be transcribed 
            currently delete the file from the table
        """
        try:
            self.MainStack.changeToTranscribed(key)
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
        
    def addProfile(self, profileName:str) -> None:
        """ add a new profile with name being profileName to the profile 
            setting page and file table file profile options
        """
        try:
            self.MainStack.ProfileSettingPage.addProfile(profileName)
            self.MainStack.FileUploadPage.fileTable.addProfile(profileName)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            self.showError(ERR.FAIL_TO.format("add profile,"))
            
    def deleteProfile(self, profileName:str) -> None: 
        """ delete profile with name being profileName from the profile 
            setting page and file table file profile options
        """
        try:
            self.MainStack.FileUploadPage.fileTable.deleteProfile(profileName)
            self.MainStack.ProfileSettingPage.deleteProfileConfirmed(True)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            self.showError(ERR.FAIL_TO.format("delete profile"))
        
    def loadProfile(self, data: Tuple[str, Dict]):
        try:
            self.MainStack.ProfileSettingPage.loadProfile(data)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            self.showError(ERR.FAIL_TO.format("load profile"))
            
    def showError(self, errorMsg:str):
        WarnBox(errorMsg) 
    
    def addPlugin(self, pluginSuite: Tuple[str, Dict[str, str]]): 
        """ 
        add a plugin identified by pluginName
        """
        self.MainStack.ProfileSettingPage.addPluginHandler(pluginSuite)
     
    # TODO:   
    def displayPluginSuiteDetail(self, suiteInfo) -> None :
        """ 
        open a frontend dialog to display suiteInfo 
        """
        try:
            display = PluginSuiteDetails(suiteInfo)
            display.exec()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            self.showError(ERR.FAIL_TO.format("display plugin suite detail"))
    
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

    def _initLogger(self):
        consoleLog = Logger.ConsoleHandler(self.Console.LogBox)
        logging.getLogger().addHandler(consoleLog)
        logging.getLogger().setLevel(logging.DEBUG) 
        
        
    
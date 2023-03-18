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
import os 
import shutil
import glob
import logging
from gbLogger import Logger
from view.components import (
    MainStack, 
    StatusBar, 
    MenuBar, 
    Console, 
)

from view.Signals import FileSignals, ViewSignals, ProfileSignals
from view.widgets import MsgBox
from view.config.Style import Dimension
from view.config.Text import About
from config_frontend import FRONTEND_CONFIG_ROOT
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    """ mainwindow  of the GUI App"""
    def __init__(
        self, 
        setting_data: Dict[str, Dict]
    ):
        """initialize mainWindow object 
        
        Args:
            settingkey: (List [str ]) a list of predefined setting profile names
        """
        super().__init__()
        # initialize the main view controller 
        self.logger = Logger.makeLogger("F")
        self.logger.info(f"start to initialize view object, get available profile {setting_data}")
        self.logger.info(f"the frontend configuration file is stored at {FRONTEND_CONFIG_ROOT}")
        # initialize the signal
        self.fileTableSignals = FileSignals()
        self.profileSignals = ProfileSignals()
        self.viewSignal = ViewSignals()
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
            setting_data,
            self.fileTableSignals, 
            self.profileSignals)
        self.logger.info("main stack initialized")
        self.setCentralWidget(self.MainStack)
        self.setContentsMargins(0,0,0,0)
        self._connectSignal()
        self._initLogger()

    """ Functions provided to controller """
    def showTranscribeInProgress(self):
        """goes to transcribe in progress page"""
        try:
            self.MainStack.gotoTranscribeInProgress()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            self.showError(f"Failed to load transcription in progress page due to the error {e}, please try to re-transcribe")
            
    def showTranscribeSuccess(self):
        """goes to trancription success page"""
        try:
            self.MainStack.gotoTranscribeSuccess()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            self.showError(f"Failed to load transcription success page due to the error {e}, please try to reload the application")
    
    def showFileUploadPage(self):
        """goes to file upload page"""
        try:
            self.MainStack.gotoFileUploadPage()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            self.showError(f"Failed to load file upload page due to the error {e}, please try again")
    
    def busyThreadPool(self):
        """shows busy thread pool message"""
        try:
            self.msgBox = MsgBox.WarnBox("The GailBot is too busy to receive your request!")
        except Exception as e:
            self.logger.error(e, exc_info=e)
            self.showError(f"The GailBot is too bust to receive your request!")
        
    def showStatusMsg(self, msg, time=None):
        """shows status message"""
        try:
            self.StatusBar.showStatusMsg(msg, time)
        except Exception as e:
            self.logger.info("ERROR: failed to show error message in status bar {e}")
            pass  # pass the error if the error bar cannot show the error TODO: revise with better handler
    
    def showFileProgress(self, msg):
        try:
            self.fileTableSignals.progressChanged.emit(msg)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            self.showError(f"Failed to show file progress due to error {e}, please check back later ")
            
    def freeThread(self):
        """clears thread message"""
        try:
            self.StatusBar.clearMessage()
        except Exception as e:
            self.logger.error(e, exc_info=e)
    
    def TranscribeFailed(self, err:str):
        """shows transcription failed message"""
        try:
            self.msgBox = MsgBox.WarnBox(f"Transcription Failed, error: {err}", 
                                        self.showFileUploadPage)
            self.MainStack.TranscribeProgressPage.IconImg.stop()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            
        
    def confirmCancel(self):
        """ handle event when user tries to cancel the thread """
        try:
            self.logger.info("")
            self.MainStack.gotoFileUploadPage()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            MsgBox.WarnBox(f"Error in canceling the application {e}")

    def addFileToTables(self, file:dict):
        """ add file to file upload table """
        try:
            self.MainStack.addFileToTables(file)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            MsgBox.WarnBox(f"Error in adding files to table {e}")
            
    def updateFile(self, data:tuple):
        """ update file information on file upload file """
        try:
            self.MainStack.updateFile(data)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            MsgBox.WarnBox(f"Error in updating the file {e}")
            
    def changeFiletoTranscribed(self, key:str):
        """ change the file status to be transcribed 
            currently delete the file from the table
        """
        try:
            self.MainStack.changeToTranscribed(key)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            MsgBox.WarnBox(f"Error in changing the file status to be transcribed {e}")
            
    def closeEvent(self, a0) -> None:
        """  called when application closes """
        try:
            super().closeEvent(a0)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            MsgBox.WarnBox(f"Failed to automatically relaunch gailbot, please restart application")
        
    def addProfile(self, profileName:str) -> None:
        """ add a new profile with name being profileName to the profile 
            setting page and file table file profile options
        """
        try:
            self.MainStack.ProfileSettingPage.addProfile(profileName)
            self.MainStack.FileUploadPage.fileTable.addProfile(profileName)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            MsgBox.WarnBox(f"Failed to add profile, get error {e}")
            
    def deleteProfile(self, profileName:str) -> None: 
        """ delete profile with name being profileName from the profile 
            setting page and file table file profile options
        """
        try:
            self.MainStack.FileUploadPage.fileTable.deleteProfile(profileName)
            self.MainStack.ProfileSettingPage.deleteProfileConfirmed(True)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            MsgBox.WarnBox(f"Failed to delete profile")
        
    def loadProfile(self, data: Tuple[str, Dict]):
        try:
            self.MainStack.ProfileSettingPage.loadProfile(data)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            MsgBox.WarnBox(f"Failed to load profile, get the error {e}")
            
    def showError(self, errorMsg:str):
        MsgBox.WarnBox(errorMsg) 
    
    def addPlugin(self, pluginName: str): 
        self.MainStack.ProfileSettingPage.addPluginHandler(pluginName)
        
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
        
        
  
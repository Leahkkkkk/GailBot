'''
File: MainStack.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 9:59:56 am
Modified By:  Siara Small  & Vivian Li
-----
Description: implementation of the main page Stack
'''
from typing import Tuple, List, Dict
from gbLogger import makeLogger
from view.config.Style import STYLE_DATA
from view.widgets.MsgBox import WarnBox
from view.pages import (
        WelcomePage, 
        ConfirmTranscribePage,
        FileUploadPage,
        SettingPage,
        TranscribeProgressPage,
        TranscribeSuccessPage,
)
from view.widgets.Background import (
    initHomePageBackground, 
    initSubPageBackground,
    initPrimaryColorBackground
)
from PyQt6.QtWidgets import QStackedWidget
from PyQt6.QtCore import QSize

class MainStack(QStackedWidget):
    """ Implementation of the main page stack.
        This module contains all the pages of gui interface as child widgets. 
        It mainly implements the logic of page redirection. 
        
        It also implements the functionalities to handle database signal, 
        when the signal need to be handled by multiple pages. 
        
    """
    def __init__(
        self, 
        *args, 
        **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.logger= makeLogger()
        self.setMaximumSize(
            QSize(STYLE_DATA.Dimension.WINMAXWIDTH, 
                  STYLE_DATA.Dimension.WINMAXHEIGHT))
        self._initPage()
        self._pageRedirect()
        self._connectSignal()
    
    def addAvailableSettings(self, profiles: List[Tuple[str, Dict]]):    
        """ add the available setting to the profile setting interface

        Args:
            profileNames (List[str]): a list of profile names
        """
        self.SettingPage.addAvailableSettings(profiles)
        
    def addAvailableEngines(self, engines: List[Tuple[str, Dict]]):
        self.SettingPage.addAvailableEngines(engines)
   
    def addAvailablePluginSuites(self, pluginSuites: List[Tuple[str, Dict, str]]):
        self.SettingPage.addAvailablePluginSuites(pluginSuites)

    def gotoTranscribeInProgress(self):
        """ redirect to transcribe in progress page """
        self.TranscribeProgressPage.IconImg.start()
        self.setCurrentWidget(self.TranscribeProgressPage)
        
    def gotoTranscribeSuccess(self):
        """ redirect to transcribe success page """
        self.setCurrentWidget(self.TranscribeSuccessPage)
       
    def gotoFileUploadPage(self):
        """ redirect to go to file upload page """
        self.setCurrentWidget(self.FileUploadPage)
    
    def gotoSettingPage(self, setting:str = None):
        """ go to setting page with the setting data """
        self.setCurrentWidget(self.SettingPage)
        self.SettingPage.settingStack.setCurrentWidget(
            self.SettingPage.ProfilePage)
      
    def updateFile(self, data:Tuple[str,str,str]):
        """ public function that update the files to all the file tables  """
        self.FileUploadPage.fileTable.updateFileContent(data)
        self.ConfirmTranscribePage.fileTable.updateFileContent(data)
        self.TranscribeProgressPage.fileTable.updateFileContent(data)
        self.TranscribeSuccessPage.fileTable.updateFileContent(data)
    
    def changeToTranscribed(self, key: str):
        """ public function that change the file status on all file tables """
        self.TranscribeSuccessPage.fileTable.changeFileToTranscribed(key)
    
    def removeFile(self, key:str):
        pass 
    
    
    def _initPage(self):
        """ initialize all pages on stack widget, using current widget to 
            mimic the functionality of swapping pages """
        self.WelcomePage = WelcomePage.WelcomePage(self)
        initHomePageBackground(self.WelcomePage)
        self.FileUploadPage = FileUploadPage.FileUploadPage() 
        initSubPageBackground(self.FileUploadPage)
        self.ConfirmTranscribePage = ConfirmTranscribePage.ConfirmTranscribePage()
        initSubPageBackground(self.ConfirmTranscribePage)
        self.SettingPage = SettingPage.SettingPage()
        initPrimaryColorBackground(self.SettingPage)
        self.TranscribeProgressPage = TranscribeProgressPage.TranscribeProgressPage()
        initSubPageBackground(self.TranscribeProgressPage)
        self.TranscribeSuccessPage = TranscribeSuccessPage.TranscribeSuccessPage()
        initSubPageBackground(self.TranscribeSuccessPage)
       
        # NOTE: the current record page is not used
        # self.RecordPage = RecordPage.RecordPage()
        # initSubPageBackground(self.RecordPage)
        
        self.addWidget(self.WelcomePage)
        self.addWidget(self.ConfirmTranscribePage)
        self.addWidget(self.FileUploadPage)
        self.addWidget(self.TranscribeProgressPage)
        self.addWidget(self.TranscribeSuccessPage)
        self.addWidget(self.SettingPage)
        self.setCurrentWidget(self.WelcomePage)
        # self.addWidget(self.RecordPage)
    
    def _changeBkg(self):
        initHomePageBackground(self.WelcomePage)
        initSubPageBackground(self.FileUploadPage)
        initSubPageBackground(self.ConfirmTranscribePage)
        initPrimaryColorBackground(self.SettingPage)
        initSubPageBackground(self.TranscribeProgressPage)
        initSubPageBackground(self.TranscribeSuccessPage)
        
    def _pageRedirect(self):
        """ initializes button click to page redirect functionality  """
        self.WelcomePage.StartBtn.clicked.connect(self.gotoFileUploadPage)
        self.FileUploadPage.settingBtn.clicked.connect(lambda: 
                self.setCurrentWidget(self.SettingPage))
        self.TranscribeSuccessPage.moreBtn.clicked.connect(self.gotoFileUploadPage)
        self.TranscribeSuccessPage.returnBtn.clicked.connect(lambda: 
                self.setCurrentWidget(self.WelcomePage))
        self.ConfirmTranscribePage.confirmBtn.clicked.connect(
            self.FileUploadPage._disallowTranscribe)
        self.SettingPage.cancelBtn.clicked.connect(self.gotoFileUploadPage)
        self.FileUploadPage.gotoMainBtn.clicked.connect(lambda:
                self.setCurrentWidget(self.WelcomePage))
        self.FileUploadPage.transcribeBtn.clicked.connect(lambda:
            self.setCurrentWidget(self.ConfirmTranscribePage))
        self.ConfirmTranscribePage.cancelBtn.clicked.connect(self.gotoFileUploadPage)
        
    def _connectSignal(self):
        """ connecting the signal  """
        ####  for selection
        self.SettingPage.ProfilePage.signal.addSucceed.connect(
            self.FileUploadPage.fileTable.addProfile)
        ##### when profile is deleted, the file table  delete profile name
        ####  from selection 
        self.SettingPage.ProfilePage.signal.deleteSucceed.connect(
            self.FileUploadPage.fileTable.deleteProfile)
        
        ### signal to change view color 
        STYLE_DATA.signal.changeColor.connect(self._changeBkg)
        
    
    # show a specific profile identified by profile name

class Request:
    def __init__(self, data, succeed: callable = None) -> None:
        self.data = data
        self.succeed = succeed
    
    def fail(self, msg: str):
        WarnBox(msg)
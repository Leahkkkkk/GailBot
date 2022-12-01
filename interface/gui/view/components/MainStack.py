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
from typing import Tuple

from util.Logger import makeLogger
from util.Style import Dimension
from util.Text import MainStackText
from view.pages import (
        WelcomePage, 
        ConfirmTranscribePage,
        FileUploadPage,
        ProfileSettingPage,
        TranscribeProgressPage,
        TranscribeSuccessPage,
        RecordPage, 
        SystemSettingPage
)
from view.widgets.Background import (
    initHomePageBackground, 
    initSubpageBackgorund,
    initPrimaryColorBackground)

from PyQt6.QtWidgets import QStackedWidget, QTabWidget
from PyQt6.QtCore import QSize


class MainStack(QStackedWidget):
    """ Implementation of the main page stack.
        This module contains all the pages of gui interface as child widgets. 
        It mainly implements the logic of page redirection. 
        
        It also implements the functionalities to handle database signal, 
        when the signal need to be handled by multiple pages. 
    
        Constructor Args:
        1. profileKeys : a list of initial profile keys, this is  passed 
                         down to the profile setting page in order to allow 
                         user to load initial profiles 
        2. fileTableSignal: a signal object to support communication between 
                            file database and view, this is  passed down to 
                            pages with file table 
        3. profilSignals: a signal object to support communication between 
                            profile database and view, this is passed down to 
                            profile page
        
    """
    def __init__(
        self, 
        profileKeys,       
        fileTableSignal,   
        profileSignals,    
        parent, 
        *args, 
        **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.profileKeys = profileKeys
        self.fileSignal = fileTableSignal
        self.profileSignals = profileSignals
        self.logger= makeLogger("F")
        self.parent = parent 
        self.setMaximumSize(
            QSize(Dimension.WINMAXWIDTH, Dimension.WINMAXHEIGHT))
        self._initPage()
        self._pageRedirect()
        self._connectSignal()
        
    def _connectSignal(self):
        """ connecting the signal  """
        # self.logger.info("connect signal")
        self.FileUploadPage.fileTable.viewSignal.goSetting.connect(
            self.gotoSettingPage)
        self.ConfirmTranscribePage.fileTable.viewSignal.goSetting.connect(
            self.gotoSettingPage)
        self.FileUploadPage.fileTable.viewSignal.transferState.connect(
            self.ConfirmTranscribePage.fileTable.filterFile)
        self.ConfirmTranscribePage.fileTable.viewSignal.transferState.connect(
            self.TranscribeProgressPage.fileTable.filterFile)
        self.ConfirmTranscribePage.fileTable.viewSignal.transferState.connect(
            self.TranscribeSuccessPage.fileTable.filterFile)
 
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
        self.setCurrentWidget(self.MainSetting)
        self.MainSetting.setCurrentWidget(self.ProfileSettingPage)
        self.ProfileSettingPage.settingStack.setCurrentIndex(1)
        if setting:
            self.ProfileSettingPage.selectSettings.setCurrentText(setting)
    
    def _initPage(self):
        """ initialize all pages on stack widget, using current widget to mimic the functionality of swapping pages """
        self.WelcomePage = WelcomePage.WelcomePage(self)
        initHomePageBackground(self.WelcomePage)
        self.FileUploadPage = FileUploadPage.FileUploadPage(
            self.profileKeys,self.fileSignal) 
        initSubpageBackgorund(self.FileUploadPage)
        self.ConfirmTranscribePage = ConfirmTranscribePage.ConfirmTranscribePage(
            self.fileSignal)
        initSubpageBackgorund(self.ConfirmTranscribePage)
        self.ProfileSettingPage = ProfileSettingPage.ProfileSettingPage(
            self.profileKeys, self.profileSignals)
        initPrimaryColorBackground(self.ProfileSettingPage)
        self.TranscribeProgressPage = TranscribeProgressPage.TranscribeProgressPage(
            self.fileSignal)
        initSubpageBackgorund(self.TranscribeProgressPage)
        self.TranscribeSuccessPage = TranscribeSuccessPage.TranscribeSuccessPage(
            self.fileSignal)
        initSubpageBackgorund(self.TranscribeSuccessPage)
        self.RecordPage = RecordPage.RecordPage()
        initSubpageBackgorund(self.RecordPage)
        self.SystemSettingPage = SystemSettingPage.SystemSettingPage()
        initPrimaryColorBackground(self.SystemSettingPage)
        self.MainSetting = QTabWidget()
        self.MainSetting.addTab(
            self.ProfileSettingPage, MainStackText.ProfileSetting)
        self.MainSetting.addTab(
            self.SystemSettingPage, MainStackText.SystemSetting) 
        
        self.addWidget(self.WelcomePage)
        self.addWidget(self.ConfirmTranscribePage)
        self.addWidget(self.FileUploadPage)
        self.addWidget(self.TranscribeProgressPage)
        self.addWidget(self.TranscribeSuccessPage)
        self.addWidget(self.RecordPage)
        self.addWidget(self.MainSetting)
        self.setCurrentWidget(self.MainSetting)
    
    def _pageRedirect(self):
        """ initializes button click to page redirect functionality  """
        self.WelcomePage.StartBtn.clicked.connect(self.gotoFileUploadPage)
        self.FileUploadPage.settingBtn.clicked.connect(lambda: 
                self.setCurrentWidget(self.MainSetting))
        self.TranscribeSuccessPage.moreBtn.clicked.connect(self.gotoFileUploadPage)
        self.TranscribeSuccessPage.returnBtn.clicked.connect(lambda: 
                self.setCurrentWidget(self.WelcomePage))
        self.ProfileSettingPage.cancelBtn.clicked.connect(self.gotoFileUploadPage)
        self.FileUploadPage.gotoMainBtn.clicked.connect(lambda:
                self.setCurrentWidget(self.WelcomePage))
        self.FileUploadPage.recordBtn.clicked.connect(lambda:
                self.setCurrentWidget(self.RecordPage))
        self.FileUploadPage.transcribeBtn.clicked.connect(lambda:
            self.setCurrentWidget(self.ConfirmTranscribePage))
        self.RecordPage.cancelBtn.clicked.connect(self.gotoFileUploadPage)
        self.ConfirmTranscribePage.cancelBtn.clicked.connect(self.gotoFileUploadPage)
        self.ProfileSettingPage.saveBtn.clicked.connect(self.gotoFileUploadPage)
        self.SystemSettingPage.cancelBtn.clicked.connect(self.gotoFileUploadPage)
        self.SystemSettingPage.saveBtn.clicked.connect(self.gotoFileUploadPage)
        
    
    def addFileToTables(self, file:dict):
        """ public function that add files to all the file tables """
        self.FileUploadPage.fileTable.addFile(file)
        self.ConfirmTranscribePage.fileTable.addFile(file)
        self.TranscribeProgressPage.fileTable.addFile(file)
        self.TranscribeSuccessPage.fileTable.addFile(file)
    
    def updateFile(self, data:Tuple[str,str,str]):
        """ public function that update the files to all the file tables  """
        self.FileUploadPage.fileTable.updateFileContent(data)
        self.ConfirmTranscribePage.fileTable.updateFileContent(data)
        self.TranscribeProgressPage.fileTable.updateFileContent(data)
        self.TranscribeSuccessPage.fileTable.updateFileContent(data)
    
    def changeToTranscribed(self, key: str):
        """ public function that change the file status on all file tables """
        self.FileUploadPage.fileTable.changeFileToTranscribed(key)
        self.ConfirmTranscribePage.fileTable.changeFileToTranscribed(key)
        self.TranscribeProgressPage.fileTable.changeFileToTranscribed(key)
        self.TranscribeSuccessPage.fileTable.changeFileToTranscribed(key)
        self.FileUploadPage.fileTable.removeFile(key)
        self.ConfirmTranscribePage.fileTable.transferList.clear()
    
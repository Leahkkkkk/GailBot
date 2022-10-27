'''
File: MainStack.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 9:59:56 am
Modified By:  Siara Small  & Vivian Li
-----
'''
from util.Logger import makeLogger

from view.pages import (
        WelcomePage, 
        ConfirmTranscribePage,
        FileUploadPage,
        SettingPage,
        TranscribeProgressPage,
        TranscribeSuccessPage,
        RecordPage
)
from view.widgets.FileTable import (
    FileTable
)
from view.widgets.PopUpTab import (
    FileDetails
)

from view.style.styleValues import Dimension

from PyQt6.QtWidgets import QStackedWidget


class MainStack(QStackedWidget):
    """ implementation of the page stack """
    def __init__(
        self, 
        settingform,       # for initializing setting form 
        profilekeys,       # a list of initial profile keys 
        fileTableSignal,   # signals for managing file data
        profileSignals,    # signals for manmaging profile data
        parent, 
        *args, 
        **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.profileForm = settingform
        self.profilekeys = profilekeys
        self.fileSignal = fileTableSignal
        self.profileSignals = profileSignals
        self.logger= makeLogger("Frontend")
        self.parent = parent 
        self.setMaximumSize(Dimension.WIN_MAXSIZE)
        self._initPage()
        self._pageRedirect()
        self._connectSignal()
        
    def _connectSignal(self):
        self.logger.info("connect signal")
        self.FileUploadPage.fileTable.signals.goSetting.connect(
            self.gotoSettingPage)
        self.ConfirmTranscribePage.fileTable.signals.goSetting.connect(
            self.gotoSettingPage)
        self.FileUploadPage.fileTable.signals.transferState.connect(
            self.ConfirmTranscribePage.fileTable.filterFile)
        self.ConfirmTranscribePage.fileTable.signals.transferState.connect(
            self.TranscribeProgressPage.fileTable.filterFile)
        self.TranscribeProgressPage.fileTable.signals.transferState.connect(
            self.TranscribeSuccessPage.fileTable.filterFile)
 
    def gotoTranscribeInProgress(self, fileData : dict = None):
        """ redirect to transcribe in progress page """
        self.TranscribeProgressPage.IconImg.start()
        self.setCurrentWidget(self.TranscribeProgressPage)
        
            
    def gotoTranscribeSuccess(self, fileData: dict = None):
        """ redirect to transcribe success page """
        self.setCurrentWidget(self.TranscribeSuccessPage)
       
        
    def gotoFileUploadPage(self):
        """ redirect to go to file upload page """
        self.setCurrentWidget(self.FileUploadPage)
    
    def gotoSettingPage(self, setting:str = None):
        """ go to setting page with the setting data """
        self.setCurrentWidget(self.SettingPage)
        self.SettingPage.settingStack.setCurrentIndex(1)
        if setting:
            self.SettingPage.selectSettings.setCurrentText(setting)
    
    def _initPage(self):
        """ initialize all pages on stack widget  """
        self.WelcomePage = WelcomePage.WelcomePage(self)
        self.FileUploadPage = FileUploadPage.FileUploadPage(
            self.profilekeys,
            self.fileSignal) 
        self.ConfirmTranscribePage = ConfirmTranscribePage.ConfirmTranscribePage(self.fileSignal)
        self.SettingPage = SettingPage.SettingPage(
            self.profileForm, 
            self.profilekeys,
            self.profileSignals)
        self.TranscribeProgressPage = TranscribeProgressPage.TranscribeProgressPage(self.fileSignal)
        self.TranscribeSuccessPage = TranscribeSuccessPage.TranscribeSuccessPage(self.fileSignal)
        self.RecordPage = RecordPage.RecordPage()
        self.addWidget(self.WelcomePage)
        self.addWidget(self.ConfirmTranscribePage)
        self.addWidget(self.FileUploadPage)
        self.addWidget(self.SettingPage)
        self.addWidget(self.TranscribeProgressPage)
        self.addWidget(self.TranscribeSuccessPage)
        self.addWidget(self.RecordPage)
        self.setCurrentWidget(self.SettingPage)
        
        
    def _pageRedirect(self):
        """ initialize button click to page rediect functionality  """
        self.WelcomePage.StartBtn.clicked.connect(lambda: 
                self.setCurrentWidget(self.FileUploadPage))
        self.FileUploadPage.settingProfile.clicked.connect(lambda: 
                self.setCurrentWidget(self.SettingPage))
        self.TranscribeSuccessPage.moreBtn.clicked.connect(lambda: 
                self.setCurrentWidget(self.FileUploadPage))
        self.TranscribeSuccessPage.returnBtn.clicked.connect(lambda: 
                self.setCurrentWidget(self.WelcomePage))
        self.SettingPage.cancelBtn.clicked.connect(lambda:  
                self.setCurrentWidget(self.FileUploadPage))
        self.FileUploadPage.gotoMainBtn.clicked.connect(lambda:
                self.setCurrentWidget(self.WelcomePage))
        self.FileUploadPage.recordBtn.clicked.connect(lambda:
                self.setCurrentWidget(self.RecordPage))
        self.FileUploadPage.transcribeBtn.clicked.connect(lambda:
            self.setCurrentWidget(self.ConfirmTranscribePage))
        self.RecordPage.cancelBtn.clicked.connect(lambda:
                self.setCurrentWidget(self.FileUploadPage))
        self.ConfirmTranscribePage.cancelBtn.clicked.connect(lambda:
            self.setCurrentWidget(self.FileUploadPage))
        self.SettingPage.saveBtn.clicked.connect(lambda:
            self.setCurrentWidget(self.FileUploadPage))
    
    def addFileToTables(self, file:dict):
        self.FileUploadPage.fileTable.addFile(file)
        self.ConfirmTranscribePage.fileTable.addFile(file)
        self.TranscribeProgressPage.fileTable.addFile(file)
        self.TranscribeSuccessPage.fileTable.addFile(file)
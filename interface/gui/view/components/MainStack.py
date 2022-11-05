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
from typing import Tuple
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



from util.Config import Dimension, MainStackText

from PyQt6.QtWidgets import QStackedWidget, QTabWidget
from PyQt6.QtCore import QSize


class MainStack(QStackedWidget):
    """ implementation of the page stack """
    def __init__(
        self, 
        profilekeys,       # a list of initial profile keys 
        fileTableSignal,   # signals for managing file data
        profileSignals,    # signals for manmaging profile data
        parent, 
        *args, 
        **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.profilekeys = profilekeys
        self.fileSignal = fileTableSignal
        self.profileSignals = profileSignals
        self.logger= makeLogger("Frontend")
        self.parent = parent 
        self.setMaximumSize(
            QSize(Dimension.WINMAXWIDTH, Dimension.WINMAXHEIGHT))
        self.setContentsMargins(0,0,0,0)
        self._initPage()
        self._pageRedirect()
        self._connectSignal()
        
    def _connectSignal(self):
        """ conecting the signal  """
        self.logger.info("connect signal")
        self.FileUploadPage.fileTable.viewSignal.goSetting.connect(
            self.gotoSettingPage)
        self.ConfirmTranscribePage.fileTable.viewSignal.goSetting.connect(
            self.gotoSettingPage)
        self.FileUploadPage.fileTable.viewSignal.transferState.connect(
            self.ConfirmTranscribePage.fileTable.filterFile)
        self.ConfirmTranscribePage.fileTable.viewSignal.transferState.connect(
            self.TranscribeProgressPage.fileTable.filterFile)
        self.TranscribeProgressPage.fileTable.viewSignal.transferState.connect(
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
        """ initialize all pages on stack widget  """
        self.WelcomePage = WelcomePage.WelcomePage(self)
        self.FileUploadPage = FileUploadPage.FileUploadPage(
            self.profilekeys,self.fileSignal) 
        self.ConfirmTranscribePage = ConfirmTranscribePage.ConfirmTranscribePage(
            self.fileSignal)
        self.ProfileSettingPage = ProfileSettingPage.ProfileSettingPage(
            self.profilekeys, self.profileSignals)
        self.TranscribeProgressPage = TranscribeProgressPage.TranscribeProgressPage(
            self.fileSignal)
        self.TranscribeSuccessPage = TranscribeSuccessPage.TranscribeSuccessPage(
            self.fileSignal)
        self.RecordPage = RecordPage.RecordPage()
        self.SystemSettingPage = SystemSettingPage.SystemSettingPage()
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
        self.setCurrentWidget(self.FileUploadPage)
    
    def _pageRedirect(self):
        """ initialize button click to page rediect functionality  """
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
        """ publich function that change the file status on all file tabless """
        self.FileUploadPage.fileTable.changeFileToTranscribed(key)
        self.ConfirmTranscribePage.fileTable.changeFileToTranscribed(key)
        self.TranscribeProgressPage.fileTable.changeFileToTranscribed(key)
        self.TranscribeSuccessPage.fileTable.changeFileToTranscribed(key)
        self.FileUploadPage.fileTable.removeFile(key)
        self.ConfirmTranscribePage.fileTable.transferList.clear()
    

        

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

from view.pages import (
        WelcomePage, 
        ApplySetProgressPage, 
        ApplySetSuccessPage, 
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
from view.widgets.FileTab import (
    FileDetails
)

from view.style.styleValues import Dimension

from PyQt6.QtWidgets import QStackedWidget


class MainStack(QStackedWidget):
    """ implementation of the page stack """
    def __init__(self, data, parent, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.settingdata = data["setting"]
        self.filedata = data["file"]
        self.parent = parent 
        self.setMaximumSize(Dimension.WIN_MAXSIZE)
        self._initPage()
        self._pageRedirect()
        
    
    
    def gotoTranscribeInProgress(self, fileData : dict = None):
        """ redirect to transcribe in progress page """
        self.TranscribeProgressPage.IconImg.start()
        self.setCurrentWidget(self.TranscribeProgressPage)
        if fileData:
            self._setTable(self.TranscribeProgressPage.fileTable, fileData)
            
    
    def gotoTranscribeSuccess(self, fileData: dict = None):
        """ redirect to transcribe success page """
        self.setCurrentWidget(self.TranscribeSuccessPage)
        if fileData:
            self._setTable(self.TranscribeSuccessPage.fileTable, fileData)
        
    def gotoFileUploadPage(self):
        """ redirect to go to file upload page """
        self.setCurrentWidget(self.FileUploadPage)
    
    def confirmCancel(self):
        """ redirect to confirm cancel page """
        self.parent.confirmCancel()
    
    def gotoSettingPage(self, setting:str = None):
        """ go to setting page with the setting data """
        self.setCurrentWidget(self.SettingPage)
        self.SettingPage.settingStack.setCurrentIndex(1)
        if setting:
            self.SettingPage.selectSettings.setCurrentText(setting)
        
    def gotoConfirmPage(self, fileData):
        """ TODO: make separate function to transcribe data to different table """
        self._setTable(self.ConfirmTranscribePage.fileTable, fileData)
        self._setTable(self.TranscribeProgressPage.fileTable, fileData)
        successData = dict(fileData)
        for items in successData.values():
            items["Status"] = "Transcribed"
            
        self._setTable(self.TranscribeSuccessPage.fileTable, fileData)
        self.setCurrentWidget(self.ConfirmTranscribePage)
    
    def _setTable(self, table:FileTable, fileData: dict):
        table.clearAll()
        table.addFilesToTable(fileData)
    
    def _initPage(self):
        """ initialize all pages on stack widget  """
        self.WelcomePage = WelcomePage.WelcomePage(self)
        self.ApplySetProgressPage = ApplySetProgressPage.ApplySetProgressPage(self)
        self.ApplySetSuccessPage = ApplySetSuccessPage.ApplySetSuccessPage(self)
        self.ConfirmTranscribePage = ConfirmTranscribePage.ConfirmTranscribePage(self)
        self.FileUploadPage = FileUploadPage.FileUploadPage(self.filedata, 
                                                            list(self.settingdata.keys()))
        self.SettingPage = SettingPage.SettingPage(self.settingdata, self)
        self.TranscribeProgressPage = TranscribeProgressPage.TranscribeProgressPage(self)
        self.TranscribeSuccessPage = TranscribeSuccessPage.TranscribeSuccessPage(self)
        self.RecordPage = RecordPage.RecordPage()
        self.addWidget(self.WelcomePage)
        self.addWidget(self.ApplySetProgressPage)
        self.addWidget(self.ApplySetSuccessPage)
        self.addWidget(self.ConfirmTranscribePage)
        self.addWidget(self.FileUploadPage)
        self.addWidget(self.SettingPage)
        self.addWidget(self.TranscribeProgressPage)
        self.addWidget(self.TranscribeSuccessPage)
        self.addWidget(self.RecordPage)
        self.setCurrentWidget(self.WelcomePage)
        
        
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
        self.RecordPage.cancelBtn.clicked.connect(lambda:
                self.setCurrentWidget(self.FileUploadPage))
        self.ConfirmTranscribePage.cancelBtn.clicked.connect(lambda:
            self.setCurrentWidget(self.FileUploadPage))
        self.SettingPage.saveBtn.clicked.connect(lambda:
            self.setCurrentWidget(self.FileUploadPage))
        self.FileUploadPage.fileTable.signals.goSetting.connect(self._OpenFileDetails)
        self.ConfirmTranscribePage.fileTable.signals.goSetting.connect(self._OpenFileDetails)
        self.FileUploadPage.fileTable.signals.sendFile.connect(self.gotoConfirmPage)
        self.ConfirmTranscribePage.fileTable.signals.sendFile.connect(self.gotoTranscribeInProgress)
        self.TranscribeProgressPage.fileTable.signals.sendFile.connect(self.gotoTranscribeSuccess)
        
        """ TODO: change this to a pop up instead of redirect """
        self.FileUploadPage.signals.gotoSetting.connect(self.gotoSettingPage)
        
    def _OpenFileDetails(self, profileKey:str):
        fileDetailDialog = FileDetails(self.settingdata[profileKey])
        fileDetailDialog.exec()
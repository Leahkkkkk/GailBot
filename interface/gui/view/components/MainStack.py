from PyQt6.QtWidgets import QStackedWidget, QWidget
from PyQt6 import QtCore 
from view.pages import (
        WelcomePage, 
        ApplySetProgressPage, 
        ApplySetSuccessPage, 
        ConfirmTranscribePage,
        FileUploadPage,
        SettingPage,
        TranscribeProgressPage,
        TranscribeSuccessPage)

class MainStack(QStackedWidget):
    def __init__(self, settingdata, parent, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.settingdata = settingdata
        self.parent = parent 
        self.setMinimumSize(QtCore.QSize(0, 0))
        self.setMaximumSize(QtCore.QSize(1200, 1200))
        self._initPage()
        self._pageRedirect()
    
    def gotoTranscribeInProgress(self):
        self.TranscribeProgressPage.IconImg.start()
        self.setCurrentWidget(self.TranscribeProgressPage)
    
    def gotoTranscribeSuccess(self):
        self.setCurrentWidget(self.TranscribeSuccessPage)
        
    def gotoFileUploadPage(self):
        self.setCurrentWidget(self.FileUploadPage)
    
    def confirmCancel(self):
        self.parent.confirmCancel()
    
    def _initPage(self):
        self.WelcomePage = WelcomePage.WelcomePage(self)
        self.ApplySetProgressPage = ApplySetProgressPage.ApplySetProgressPage(self)
        self.ApplySetSuccessPage = ApplySetSuccessPage.ApplySetSuccessPage(self)
        self.ConfirmTranscribePage = ConfirmTranscribePage.ConfirmTranscribePage(self)
        self.FileUploadPage = FileUploadPage.FileUploadPage(self)
        self.SettingPage = SettingPage.SettingPage(self.settingdata, self)
        self.TranscribeProgressPage = TranscribeProgressPage.TranscribeProgressPage(self)
        self.TranscribeSuccessPage = TranscribeSuccessPage.TranscribeSuccessPage(parent=self)
        self.setMaximumSize(QtCore.QSize(1000, 800))
        
        self.addWidget(self.WelcomePage)
        self.addWidget(self.ApplySetProgressPage)
        self.addWidget(self.ApplySetSuccessPage)
        self.addWidget(self.ConfirmTranscribePage)
        self.addWidget(self.FileUploadPage)
        self.addWidget(self.SettingPage)
        self.addWidget(self.TranscribeProgressPage)
        self.addWidget(self.TranscribeSuccessPage)
        self.setCurrentWidget(self.WelcomePage)
    
    def _gotoConfirm(self):
        if self.FileUploadPage.fileTable.selectedIndexes():
            self.setCurrentWidget(self.ConfirmTranscribePage)
        
    def _pageRedirect(self):
        self.WelcomePage.StartBtn.clicked.connect(lambda: 
                self.setCurrentWidget(self.FileUploadPage))
        self.WelcomePage.HomeSetBtn.clicked.connect(lambda: 
                self.setCurrentWidget(self.SettingPage))
        self.TranscribeSuccessPage.moreBtn.clicked.connect(lambda: 
                self.setCurrentWidget(self.FileUploadPage))
        self.TranscribeSuccessPage.returnBtn.clicked.connect(lambda: 
                self.setCurrentWidget(self.WelcomePage))
        self.FileUploadPage.settingBtn.clicked.connect(lambda: 
                self.setCurrentWidget(self.SettingPage))
        self.SettingPage.exitBtn.clicked.connect(lambda:    
                self.setCurrentWidget(self.FileUploadPage))
        self.SettingPage.cancelBtn.clicked.connect(lambda:  
                self.setCurrentWidget(self.FileUploadPage))
        self.FileUploadPage.transcribeBtn.clicked.connect(self._gotoConfirm)
        self.TranscribeSuccessPage.postSetBtn.clicked.connect(lambda:
                self.setCurrentWidget(self.SettingPage))
        self.FileUploadPage.gotoMainBtn.clicked.connect(lambda:
                self.setCurrentWidget(self.WelcomePage))
    
        
    
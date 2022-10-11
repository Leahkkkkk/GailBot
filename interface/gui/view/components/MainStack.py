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
        TranscribeSuccessPage
)
from view.style.styleValues import Dimension

from PyQt6.QtWidgets import QStackedWidget

class MainStack(QStackedWidget):
    """ implementation of the page stack """
    def __init__(self, settingdata, parent, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.settingdata = settingdata
        self.parent = parent 
        self.setMaximumSize(Dimension.WIN_MAXSIZE)
        self._initPage()
        self._pageRedirect()
    
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
    
    def confirmCancel(self):
        """ redirect to confirm cancel page """
        self.parent.confirmCancel()
    
    def _initPage(self):
        """ initialize all pages on stack widget  """
        self.WelcomePage = WelcomePage.WelcomePage(self)
        self.ApplySetProgressPage = ApplySetProgressPage.ApplySetProgressPage(self)
        self.ApplySetSuccessPage = ApplySetSuccessPage.ApplySetSuccessPage(self)
        self.ConfirmTranscribePage = ConfirmTranscribePage.ConfirmTranscribePage(self)
        self.FileUploadPage = FileUploadPage.FileUploadPage(self)
        self.SettingPage = SettingPage.SettingPage(self.settingdata, self)
        self.TranscribeProgressPage = TranscribeProgressPage.TranscribeProgressPage(self)
        self.TranscribeSuccessPage = TranscribeSuccessPage.TranscribeSuccessPage(self)
        self.addWidget(self.WelcomePage)
        self.addWidget(self.ApplySetProgressPage)
        self.addWidget(self.ApplySetSuccessPage)
        self.addWidget(self.ConfirmTranscribePage)
        self.addWidget(self.FileUploadPage)
        self.addWidget(self.SettingPage)
        self.addWidget(self.TranscribeProgressPage)
        self.addWidget(self.TranscribeSuccessPage)
        self.setCurrentWidget(self.WelcomePage)
        
    def _pageRedirect(self):
        """ initialize button click to page rediect functionality  """
        self.WelcomePage.StartBtn.clicked.connect(lambda: 
                self.setCurrentWidget(self.TranscribeSuccessPage))
        self.WelcomePage.HomeSetBtn.clicked.connect(lambda: 
                self.setCurrentWidget(self.SettingPage))
        self.TranscribeSuccessPage.moreBtn.clicked.connect(lambda: 
                self.setCurrentWidget(self.FileUploadPage))
        self.TranscribeSuccessPage.returnBtn.clicked.connect(lambda: 
                self.setCurrentWidget(self.WelcomePage))
        self.SettingPage.exitBtn.clicked.connect(lambda:    
                self.setCurrentWidget(self.FileUploadPage))
        self.SettingPage.cancelBtn.clicked.connect(lambda:  
                self.setCurrentWidget(self.FileUploadPage))
        self.FileUploadPage.transcribeBtn.clicked.connect(lambda:
                self.setCurrentWidget(self.ConfirmTranscribePage))
        self.TranscribeSuccessPage.postSetBtn.clicked.connect(lambda:
                self.setCurrentWidget(self.SettingPage))
        self.FileUploadPage.gotoMainBtn.clicked.connect(lambda:
                self.setCurrentWidget(self.WelcomePage))
    
        
    
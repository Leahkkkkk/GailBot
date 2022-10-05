from PyQt6.QtWidgets import *
from PyQt6 import QtCore
from view.pages import RequiredSetPage, PostSetPage
from view.widgets import Button
from view.style import style

""" class for settings page"""
class SettingPage(QWidget):
    """ initialize class"""
    def __init__(self, settingdata, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.settingdata = settingdata
        self._initWidget()
        self._initLayout()
        self._connectSignal()
    """ initialize widgets"""
    def _initWidget(self):
        self.cancelBtn = Button.BorderBtn("Cancel", style.Color.ORANGE)
        self.saveBtn = Button.ColoredBtn("save", style.Color.GREEN)
        self.exitBtn = QPushButton("exit")
        self.requiredSetBtn = QPushButton("required setting")
        self.postSetBtn = QPushButton("post transcription settings")
        
        self.settingStack = QStackedWidget(self)
        self.RequiredSetPage = RequiredSetPage.RequiredSetPage(self.settingdata["engine"])
        self.PostSetPage = PostSetPage.PostSetPage(self.settingdata["Post Transcribe"])        
        self.settingStack.addWidget(self.RequiredSetPage)
        self.settingStack.addWidget(self.PostSetPage)
    """initialize layout"""
    def _initLayout(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        """ add widget to layout """
        self.layout.addWidget(self.requiredSetBtn, 0, 0)
        self.layout.addWidget(self.postSetBtn, 1, 0)
        self.layout.addWidget(self.saveBtn,7,0)
        self.layout.addWidget(self.exitBtn,8,0)
        self.layout.addWidget(self.cancelBtn, 9, 0)
        self.layout.addWidget(self.settingStack, 1, 1, 8, 4)
        self.settingStack.resize(QtCore.QSize(500,800))
    """handles signals"""
    def _connectSignal(self):
        self.postSetBtn.clicked.connect(lambda: self.settingStack.
                                        setCurrentWidget(self.PostSetPage))
        self.requiredSetBtn.clicked.connect(lambda: self.settingStack.
                                            setCurrentWidget(self.RequiredSetPage))
        self.saveBtn.clicked.connect(self.RequiredSetPage.submitForm)
        

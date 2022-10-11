'''
File: SettingPage.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 11:11:19 am
Modified By:  Siara Small  & Vivian Li
-----
'''

from view.style.styleValues import Color
from view.style.Background import initBackground
from view.pages import RequiredSetPage, PostSetPage
from view.widgets import Button

from PyQt6.QtWidgets import (
    QWidget, 
    QPushButton,
    QStackedWidget, 
    QGridLayout
)
from PyQt6 import QtCore

class SettingPage(QWidget):
    """ class for settings page"""
    def __init__(self, settingdata, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.settingdata = settingdata
        self._initWidget()
        self._initLayout()
        self._connectSignal()
        self._initStyle()
    
    def _initWidget(self):
        """ initialize widgets"""
        self.cancelBtn = Button.BorderBtn("Cancel", Color.ORANGE)
        self.saveBtn = Button.ColoredBtn("save and exit", Color.GREEN)
        self.requiredSetBtn = QPushButton("required setting")
        self.postSetBtn = QPushButton("post transcription settings")
        
        self.settingStack = QStackedWidget(self)
        self.RequiredSetPage = RequiredSetPage.RequiredSetPage(self.settingdata["engine"])
        self.PostSetPage = PostSetPage.PostSetPage(self.settingdata["Post Transcribe"])        
        self.settingStack.addWidget(self.RequiredSetPage)
        self.settingStack.addWidget(self.PostSetPage)
    
    def _initLayout(self):
        """initialize layout"""
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        """ add widget to layout """
        self.layout.addWidget(self.requiredSetBtn, 0, 0)
        self.layout.addWidget(self.postSetBtn, 1, 0)
        self.layout.addWidget(self.saveBtn,3,0)
        self.layout.addWidget(self.cancelBtn, 4, 0)
        self.layout.addWidget(self.settingStack, 1, 1, 8, 4)
        self.settingStack.resize(QtCore.QSize(500,800))
        initBackground(self)
   
   
    def _connectSignal(self):
        """handles signals"""
        self.postSetBtn.clicked.connect(lambda: self.settingStack.
                                        setCurrentWidget(self.PostSetPage))
        self.requiredSetBtn.clicked.connect(lambda: self.settingStack.
                                            setCurrentWidget(self.RequiredSetPage))
        self.saveBtn.clicked.connect(self.RequiredSetPage.submitForm)
    
    def _initStyle(self):
        self.settingStack.setObjectName("settingStack")
        self.settingStack.setStyleSheet("#settingStack {border-left: 1px solid black}")
        

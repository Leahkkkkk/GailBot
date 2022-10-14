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
    QGridLayout, 
    QComboBox
)
from PyQt6 import QtCore

class SettingPage(QWidget):
    """ class for settings page"""
    def __init__(self, settingdata:dict, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.settingdata = settingdata
        self.profileKeys = list(settingdata)
        self._initWidget()
        self._initLayout()
        self._connectSignal()
        self._initStyle()
    
    def _initWidget(self):
        """ initialize widgets"""
        self.selectSettings = QComboBox()
        self.selectSettings.addItems(self.profileKeys)
        self.cancelBtn = Button.BorderBtn("Cancel", Color.ORANGE)
        self.saveBtn = Button.ColoredBtn("save and exit", Color.GREEN)
        self.requiredSetBtn = QPushButton("required setting")
        self.postSetBtn = QPushButton("post transcription settings")

        self.settingStack = QStackedWidget(self)
        self.RequiredSetPage = RequiredSetPage.RequiredSetPage(self.settingdata[self.profileKeys[0]]["engine"])
        self.PostSetPage = PostSetPage.PostSetPage(self.settingdata[self.profileKeys[0]]["Post Transcribe"])   
        self.selectSettings.setCurrentIndex(0)     
        
        self.placeHolder = QWidget()
        self.settingStack.addWidget(self.placeHolder)
        self.settingStack.addWidget(self.RequiredSetPage)
        self.settingStack.addWidget(self.PostSetPage)
        self.settingStack.setCurrentWidget(self.RequiredSetPage)
    
    def _initLayout(self):
        """initialize layout"""
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        """ add widget to layout """
        self.layout.addWidget(self.selectSettings, 0, 0)
        self.layout.addWidget(self.requiredSetBtn, 1, 0)
        self.layout.addWidget(self.postSetBtn, 2, 0)
        self.layout.addWidget(self.saveBtn,5,0)
        self.layout.addWidget(self.cancelBtn, 6, 0)
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
        self.selectSettings.currentIndexChanged.connect(self._changeSettingProfile)
    
    def _initStyle(self):
        self.settingStack.setObjectName("settingStack")
        # self.settingStack.setStyleSheet("#settingStack {border: none; border-left:0.5px solid grey;}")
    
    """ TODO: improve functions to dynamically change setting and fetch setting data """
    def _changeSettingProfile(self, index):
        self.settingStack.setCurrentWidget(self.placeHolder)
        key = self.selectSettings.itemText(index)
        self.settingStack.removeWidget(self.RequiredSetPage)
        self.RequiredSetPage = RequiredSetPage.RequiredSetPage(self.settingdata[key]["engine"])
        self.settingStack.addWidget(self.RequiredSetPage)
        self.settingStack.removeWidget(self.PostSetPage)
 
        self.PostSetPage = PostSetPage.PostSetPage(self.settingdata[key]["Post Transcribe"])     
        self.settingStack.addWidget(self.PostSetPage)
        self.settingStack.setCurrentWidget(self.RequiredSetPage)
   
        


        

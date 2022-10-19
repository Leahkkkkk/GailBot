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

""" 
TODO: create new profile functionality
TODO: save profile data functionality 
TODO: load setting values based on a setting values dictionary
TODO: disable edits for setting form
TODO: change name settingdata to settingFormData 
                  the counter part is settingValueData
TODO: make a combobox widget
"""
from typing import Dict, TypedDict

from view.style.styleValues import Color, FontSize, Dimension
from view.style.Background import initBackground
from view.Text.LinkText import Links
from view.pages import RequiredSetPage, PostSetPage
from view.widgets import Button, Label, ComboBox

from PyQt6.QtWidgets import (
    QWidget, 
    QStackedWidget, 
    QGridLayout, 
    QComboBox
)
from PyQt6 import QtCore

class SettingPage(QWidget):
    """ class for settings page"""
    def __init__(self, settingdata:Dict[str, dict], *args, **kwargs) -> None:
        
        super().__init__(*args, **kwargs)
        self.settingdata = settingdata
        self.profileKeys = list(settingdata)  # stores all the keys of the setting data 
        self._initWidget()
        self._initLayout()
        self._connectSignal()
        self._initStyle()
    
    def _initWidget(self):
        """ initialize widgets"""
        self.selectSettings = ComboBox.ComboBox()
        self.selectSettings.addItems(self.profileKeys)
        self.cancelBtn = Button.BorderBtn("Cancel", Color.ORANGE)
        self.saveBtn = Button.ColoredBtn("save and exit", Color.GREEN)
        self.requiredSetBtn = Button.BorderBtn("required setting", 
                                               Color.GREYDARK,FontSize.BTN, 0)
        self.requiredSetBtn.setFixedWidth(190)
        self.postSetBtn = Button.BorderBtn("post transcription settings",Color.GREYDARK,FontSize.BTN,0)
        self.postSetBtn.setFixedWidth(190)
        self.GuideLink = Label.Label(Links.guideLink, FontSize.LINK, link=True)

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
        self.layout.addWidget(self.selectSettings, 0, 0, 
                              alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.requiredSetBtn, 1, 0,
                              alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.postSetBtn, 2, 0,
                              alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.saveBtn,5,0,
                              alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.cancelBtn, 6, 0,
                              alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.GuideLink, 8, 0,
                              alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.settingStack, 0, 1, 10, 4)
        self.layout.setContentsMargins(0,0,0,0)

        self.settingStack.resize(QtCore.QSize(500,800))
        self.settingStack.setContentsMargins(0,0,0,0)
        self.saveBtn.setFixedSize(Dimension.BGBUTTON)
        self.cancelBtn.setFixedSize(Dimension.RBUTTON)
        
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
        """ add this to an external stylesheet"""
        self.settingStack.setStyleSheet("#settingStack {border: none; border-left:0.5px solid grey;}")
    
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
   
        


        

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
from ctypes import alignment
import tomli 
from typing import Dict, List, Set

from util.Config import Color, FontSize, ProfileSettingForm
from util.Logger import makeLogger
from view.style.styleValues import Dimension
from view.Signals import ProfileSignals
from view.style.Background import initBackground
from view.Text.LinkText import Links
from view.pages import RequiredSetPage, PostSetPage, PluginPage
from view.widgets import Button, Label, ComboBox, SideBar, Image
from view.components.CreateNewSettingTab import CreateNewSetting
from view.components.PluginDialog import PluginDialog

from PyQt6.QtWidgets import (
    QWidget, 
    QStackedWidget, 
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout
)
from PyQt6 import QtCore

center = QtCore.Qt.AlignmentFlag.AlignHCenter
bottom = QtCore.Qt.AlignmentFlag.AlignBottom
class ProfileSettingPage(QWidget):
    """ class for settings page"""
    def __init__(
        self, 
        settingForm:Dict[str, dict], 
        profilekeys:List[str],
        plugins:Set[str],
        signals:ProfileSignals,
        *args, 
        **kwargs) -> None:
        
        super().__init__(*args, **kwargs)
        self.settingForm = settingForm
        self.signals = signals
        self.profilekeys = profilekeys
        self.plugins = plugins
        self.logger = makeLogger("Frontend")
        self._initWidget()
        self._initLayout()
        self._connectSignal()
        self._initStyle()
    
    def _initWidget(self):
        """ initialize widgets"""
        initBackground(self)
        self.sideBar = SideBar.SideBar()
        self.selectSettings = ComboBox.ComboBox()
        self.selectSettings.addItems(self.profilekeys)
        
        self.cancelBtn = Button.BorderBtn(
            "Cancel", 
            Color.ORANGE)
        self.saveBtn = Button.ColoredBtn(
            "Save and Exit", 
            Color.GREEN)
        self.newProfileBtn = Button.ColoredBtn(
            "Create New Profile", 
            Color.BLUEMEDIUM)
        self.requiredSetBtn = Button.BorderBtn(
            "Required Settings", 
            Color.GREYDARK, 
            FontSize.BTN, 0)
        self.requiredSetBtn.setFixedWidth(190)
        self.postSetBtn = Button.BorderBtn(
            "Post-Transcription Settings", 
            Color.GREYDARK, 
            FontSize.BTN, 0)
        self.postSetBtn.setFixedWidth(190)
        self.GuideLink = Label.Label(
            Links.guideLink, 
            FontSize.LINK, 
            link=True)
        self.newPluginBtn = Button.ColoredBtn(
            "Add New Plugin",
            Color.BLUEMEDIUM)
        self.pluginBtn = Button.BorderBtn(
            "Plugin Setting",
            Color.GREYDARK,FontSize.BTN,0
        )
       
        self.pluginBtn.setFixedWidth(190)
        self.settingStack = QStackedWidget(self)
        self.RequiredSetPage = RequiredSetPage.RequiredSetPage(
            ProfileSettingForm.RequiredSetting)
        self.PostSetPage = PostSetPage.PostSetPage(
            ProfileSettingForm.PostTranscribe)   
        self.PluginPage = PluginPage.PluginPage(self.plugins)
        
        self.selectSettings.setCurrentIndex(0)     
        self.placeHolder = QWidget()
        self.settingStack.addWidget(self.placeHolder)
        self.settingStack.addWidget(self.RequiredSetPage)
        self.settingStack.addWidget(self.PostSetPage)
        self.settingStack.addWidget(self.PluginPage)
        self.settingStack.setCurrentWidget(self.RequiredSetPage)

    
    def _initLayout(self):
        """initialize layout"""
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0,0,0,0)
        self.horizontalLayout.setSpacing(0)
        self.setLayout(self.horizontalLayout)
        
        """ add widget to layout """
        self.sideBar.addWidget(self.selectSettings)
        self.sideBar.addWidget(self.requiredSetBtn)
        self.sideBar.addWidget(self.postSetBtn)
        self.sideBar.addWidget(self.pluginBtn)
        self.sideBar.addWidget(self.newPluginBtn)
        self.sideBar.addWidget(self.newProfileBtn)
        self.sideBar.addWidget(self.saveBtn)
        self.sideBar.addWidget(self.cancelBtn)
        self.sideBar.addWidget(self.GuideLink, alignment=bottom)
        self.horizontalLayout.addWidget(self.sideBar)
        self.horizontalLayout.addWidget(self.settingStack)
        self.settingStack.resize(QtCore.QSize(500,800))
        self.settingStack.setContentsMargins(0,0,0,0)
        self.saveBtn.setFixedSize(Dimension.BGBUTTON)
        self.cancelBtn.setFixedSize(Dimension.RBUTTON)
        self.newProfileBtn.setFixedSize(Dimension.BGBUTTON)
        self.newPluginBtn.setFixedSize(Dimension.BGBUTTON)
   
   
    def _connectSignal(self):
        """handles signals"""
        self.postSetBtn.clicked.connect(
            lambda: self.settingStack.setCurrentWidget(self.PostSetPage))
        self.requiredSetBtn.clicked.connect(
            lambda: self.settingStack.setCurrentWidget(self.RequiredSetPage))
        self.pluginBtn.clicked.connect(
            lambda: self.settingStack.setCurrentWidget(self.PluginPage))
        
        self.saveBtn.clicked.connect(self.RequiredSetPage.submitForm)
        
        self.selectSettings.currentTextChanged.connect(self._getProfile)

        self.newProfileBtn.clicked.connect(self.createNewSetting)
        self.saveBtn.clicked.connect(self.updateProfile)
        self.newPluginBtn.clicked.connect(self.addPluginRequest)
    
    def _initStyle(self):
        self.settingStack.setObjectName("settingStack")
        """ add this to an external stylesheet"""
        self.settingStack.setStyleSheet("#settingStack {border: none; border-left:0.5px solid grey;}")
   
    def _getProfile(self, profileName:str):
        """ send the request to database to get profile data  """
        self.signals.get.emit(profileName)
        
    def _postNewProfile(self, profile: tuple):
        """ send the request to database to post a new profile data """
        self.signals.post.emit(profile)
    
    def createNewSetting(self):
        """ open a pop up window for user to create new setting profile """
        createNewSettingTab = CreateNewSetting(
                        list(ProfileSettingForm.RequiredSetting["Engine"]),
                             ProfileSettingForm.RequiredSetting["Engine"],
                             ProfileSettingForm.RequiredSetting["OutPut Format"],
                             ProfileSettingForm.PostTranscribe,
                             self.plugins)
        createNewSettingTab.signals.newSetting.connect(self._postNewProfile)
        createNewSettingTab.exec()
        
        
    def loadProfile(self, profile:tuple):
        """ load the profile data to be presented onto the table """
        key, data = profile 
        self.selectSettings.setCurrentText(key)
        self.PostSetPage.setValue(data["PostTranscribe"])
        self.RequiredSetPage.setValue(data["RequiredSetting"])
        self.PluginPage.setValue(data["Plugins"])
    
    def addProfile (self, profileName:str):
        """ adding a new profile optin to the setting page 
        Arg:
            profileName
        
        """
        self.selectSettings.addItem(profileName)
    
    def addPluginRequest(self):
        """ open a pop up window to add plugin
        """
        pluginDialog = PluginDialog(self.signals)
        pluginDialog.exec()
    
    def addPluginHandler(self, plugin:str):
        # self.plugins.add(plugin)
        self.PluginPage.addNewPlugin(plugin)
        
    def updateProfile(self):
        """ update the new profile setting """
        newSetting = dict()
        newSetting["RequiredSetting"] = self.RequiredSetPage.getValue()
        newSetting["PostTranscribe"]  = self.PostSetPage.getValue()
        newSetting["Plugins"] = self.PluginPage.getValue()
        self.logger.info(newSetting)
        profileKey = self.selectSettings.currentText()
        self.signals.edit.emit((profileKey, newSetting))

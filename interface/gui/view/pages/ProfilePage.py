'''
File: ProfilePage.py
Project: GailBot GUI
File Created: 2022/10/
Author: Siara Small  & Vivian Li
-----
Last Modified:2023/04/18
Modified By:  Siara Small  & Vivian Li
-----
Description: 
'''
from typing import List
from view.config.Text import ProfilePageText as Text
from view.signal import EngineSignal, ProfileSignal
from view.Request import Request
from view.components.SettingTables import ProfileTable
from view.components.SettingConfig import CreateNewProfile
from PyQt6.QtCore import Qt
from .BaseSettingPage import BaseSettingPage

center  = Qt.AlignmentFlag.AlignHCenter

class ProfilePage(BaseSettingPage):
    def __init__(
        self,
        *args, 
        **kwargs) -> None:
        """ initializes class """
        self.headerText = Text.HEADER
        self.captionText = Text.CAPTION
        self.addNewButtonText = Text.CREATE_NEW
        self.signal = ProfileSignal
        self.engineSignal = EngineSignal
        self.mainTable = ProfileTable(self.signal, engineSignal=self.engineSignal, parent=self)
        self.availableEngineSettings : List[str] = []
        self.availablePluginSettings : List[str] = []
        super().__init__( *args, **kwargs)
    
    def addItem(self):
        newProfile = CreateNewProfile(
            self.availableEngineSettings, 
            self.availablePluginSettings,
            self.engineSignal)
        newProfile.signals.addProfile.connect(self.sendAddRequest)
        newProfile.exec()
    
    def addPluginSuite(self, name:str):
        self.availablePluginSettings.append(name)
    
    def deletePlugin(self, name:str):
        if name in self.availablePluginSettings:
            self.availablePluginSettings.remove(name)
   
    def addEngineSetting(self, name:str):
        self.availableEngineSettings.append(name)

    def deleteEngine(self, name:str):
        if name in self.availableEngineSettings:
            self.availableEngineSettings.remove(name)
        
'''
File: ProfilePage.py
Project: GailBot GUI
File Created: 2022/10/
Author: Siara Small  & Vivian Li
-----
Last Modified:2023/04/18
Modified By:  Siara Small  & Vivian Li
-----
Description: implementation of profile setting page 
'''
from typing import List
from view.config.Text import PROFILE_PAGE as Text
from view.config.InstructionText import INSTRUCTION
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
        self.START = Text.CAPTION
        self.addNewButtonText = Text.CREATE_NEW
        self.signal = ProfileSignal
        self.engineSignal = EngineSignal
        self.mainTable = ProfileTable(self.signal, engineSignal=self.engineSignal, parent=self)
        self.availableEngineSettings : List[str] = []
        self.availablePluginSettings : List[str] = []
        self.instruction = INSTRUCTION.PROFILE_TABLE_INS
        super().__init__( *args, **kwargs)
    
    def addItem(self):
        """ open a dialogue that allows user to create a new profile """
        newProfile = CreateNewProfile(
            self.availableEngineSettings, 
            self.availablePluginSettings,
            self.engineSignal)
        newProfile.signals.addProfile.connect(self.sendAddRequest)
        newProfile.exec()
    
    def addPluginSuite(self, name:str):
        """ add a plugin suite to the current list of available plugin suite """
        self.availablePluginSettings.append(name)
    
    def deletePlugin(self, name:str):
        """ delete a plugin suite from the current list of available plugin suite """
        if name in self.availablePluginSettings:
            self.availablePluginSettings.remove(name)
   
    def addEngineSetting(self, name:str):
        """ add an engine setting to the current list of available engine """
        self.availableEngineSettings.append(name)

    def deleteEngine(self, name:str):
        """ delete an engine from the current list of available engine """
        if name in self.availableEngineSettings:
            self.availableEngineSettings.remove(name)
        
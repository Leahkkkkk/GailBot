from typing import List
from view.config.Text import ProfilePageText as Text
from view.Signals import DataSignal
from view.Request import Request
from view.widgets.ProfileTable import ProfileTable 
from view.components.ConfigProfileTab import CreateNewProfile
from PyQt6.QtCore import Qt
from .BaseSettingPage import BaseSettingPage

center  = Qt.AlignmentFlag.AlignHCenter

class ProfilePage(BaseSettingPage):
    def __init__(
        self,
        *args, 
        **kwargs) -> None:
        """ initializes class """
        self.headerText = Text.Header
        self.captionText = Text.Caption
        self.signal = DataSignal()
        self.mainTable = ProfileTable(self.signal, parent=self)
        self.availableEngineSettings : List[str] = []
        self.availablePluginSettings : List[str] = []
        super().__init__( *args, **kwargs)
    
    def addItem(self):
        newProfile = CreateNewProfile(
            self.availableEngineSettings, 
            self.availablePluginSettings)
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
        
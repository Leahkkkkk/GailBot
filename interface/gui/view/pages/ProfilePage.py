
from view.config.Text import ProfilePageText as Text
from view.Signals import DataSignal
from view.Request import Request
from view.widgets.ProfileTable import ProfileTable 
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
        self.mainTable = ProfileTable(self.signal)
        self.plugins = []
        super().__init__( *args, **kwargs)
    
    def addItem(self):
        pass 
    
    def sendAddRequest(self, engineData):
        self.signal.postRequest.emit(
            Request(data=engineData, succeed=self.addSucceed)
        )
    
    def addSucceed(self, data):
        self.mainTable.addItem(data)
        self.signal.addSucceed.emit(data)
        
    def addAvailableSetting(self, profileKeys):
        pass 
    
    def addPluginSuite(self, suite:str):
        self.plugins.append(suite)
    
    def deletePlugin(self, suite:str):
        if suite in self.plugins:
            self.plugins.remove(suite)
    
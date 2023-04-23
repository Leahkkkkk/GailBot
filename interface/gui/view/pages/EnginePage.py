
from view.config.Text import ENGINE_SETTING_TEXT as Text
from view.signal import EngineSignal
from view.Request import Request
from gbLogger import makeLogger
from view.components.SettingTables import EngineTable
from view.components.SettingConfig import CreateNewEngine
from PyQt6.QtCore import Qt
from .BaseSettingPage import BaseSettingPage

center  = Qt.AlignmentFlag.AlignHCenter

class EnginePage(BaseSettingPage):
    def __init__(
        self,
        *args, 
        **kwargs) -> None:
        """ initializes class """
        self.headerText = Text.HEADER
        self.captionText = Text.CAPTION
        self.addNewButtonText = Text.CREATE_NEW
        self.signal = EngineSignal 
        self.mainTable = EngineTable(self.signal)
        super().__init__( *args, **kwargs)
    
    def addItem(self):
        engineDialog = CreateNewEngine()
        engineDialog.signals.addEngine.connect(self.sendAddRequest)
        engineDialog.exec()

    def addAvailableEngine(self, engines):
        self.mainTable.addItems(engines)
    
    
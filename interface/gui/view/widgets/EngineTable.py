from typing import List, Dict, Tuple 
from view.config.Style import STYLE_DATA
from config_frontend import PROJECT_ROOT
from view.config.Text import ENGINE_SETTING_TEXT as TEXT
from view.Signals import DataSignal
from view.widgets import initPrimaryColorBackground, Label
from view.components.ConfigEngineTab import EditEngine
from gbLogger import makeLogger
from .Table import BaseTable
from view.components.SettingDetail import EngineDetail
class EngineTable(BaseTable):
    def __init__(self, signal: DataSignal ):
        super().__init__(TEXT.TABLE_HEADER)
        self.signal = signal
        self.resizeCol(TEXT.TABLE_DIMENSION)
        self.dataKeyToCol = {"engine": 1} 

    def openEditDialog(self, data):
        editDialog = EditEngine(data)
        editDialog.signals.editEngine.connect(self.sendEditRequest)
        editDialog.exec()
    
    def displayDetail(self, data):
        name, setting = data 
        EngineDetail(name, setting)
        
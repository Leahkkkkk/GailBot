import os
from typing import List, Dict, Tuple 
from view.config.Text import ProfilePageText as Text
from view.Signals import DataSignal
from view.Request import Request
from view.util.ErrorMsg import ERR  
from .MsgBox import WarnBox, ConfirmBox
from view.components.ConfigProfileTab import EditProfile
from .Table import BaseTable
from PyQt6.QtWidgets import QWidget

class ProfileTable(BaseTable):
    def __init__(self, signal: DataSignal, engineSignal, parent: QWidget):
        super().__init__(Text.tableHeader)
        self.signal = signal
        self.engineSignal = engineSignal
        self.parent = parent
        self.resizeCol(Text.tableDimension)
        self.dataKeyToCol = {"engine_setting_name": 1,
                             "plugin_setting": 2}
    
    def openEditDialog(self, data):
        editDialog = EditProfile(data, 
                                 self.parent.availableEngineSettings, 
                                 self.parent.availablePluginSettings,
                                 self.engineSignal)
        editDialog.signals.editProfile.connect(self.sendEditRequest)
        editDialog.exec()
    

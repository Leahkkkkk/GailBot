from typing import TypedDict
from .DetailTable import SettingDisplay
from view.config.Style import STYLE_DATA 
from view.widgets.Label import Label 
from view.widgets.Background import initPrimaryColorBackground
from PyQt6.QtWidgets import QDialog, QVBoxLayout
from PyQt6.QtCore import Qt 

class PluginInfo(TypedDict):
    suite_name : str 
    metadata : dict 
    dependency_graph: dict
    documentation: dict
    
class EngineDetail(QDialog):
    def __init__(self, name, data) -> None:
        super().__init__()
        initPrimaryColorBackground(self)
        self._layout = QVBoxLayout()
        self.nameHeader = Label(name, STYLE_DATA.FontSize.HEADER3, STYLE_DATA.FontFamily.MAIN)
        self.settingDisplay = SettingDisplay()
        self.settingDisplay.setData(data)
        self.setLayout(self._layout)
        self._layout.addWidget(self.nameHeader, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._layout.addWidget(self.settingDisplay, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.exec()
from typing import TypedDict, Dict, List
from view.config.Style import STYLE_DATA 
from .DetailTable import PluginListDisplay, SettingDisplay
from view.widgets.Label import Label 
from view.widgets.Background import initPrimaryColorBackground
from PyQt6.QtWidgets import QDialog, QVBoxLayout 
from PyQt6.QtCore import Qt

class ProfileInfo(TypedDict):
    engine_setting: dict 
    engine_setting_name: str 
    plugin_setting: List[str]


class ProfileDetail(QDialog):
    def __init__(self, name, data) -> None:
        super().__init__()
        initPrimaryColorBackground(self)
        self._layout = QVBoxLayout()
        self.nameHeader = Label(name, STYLE_DATA.FontSize.HEADER2, STYLE_DATA.FontFamily.MAIN)
        
        self.settingDisplay = SettingDisplay()
        self.pluginDisplay = PluginListDisplay()
        self.pluginDisplay.setData(data["plugin_setting"])
        self.settingDisplay.setData(data["engine_setting"])
        self.setLayout(self._layout)
        self._layout.addWidget(self.nameHeader, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._layout.addSpacing(10)
        self._layout.addWidget(self.settingDisplay, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._layout.addSpacing(10)
        self._layout.addWidget(self.pluginDisplay, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.exec()

'''
File: SettingDetail.py
Project: GailBot GUI
File Created: 2022/10/
Author: Siara Small  & Vivian Li
-----
Last Modified:2023/04/21
Modified By:  Siara Small  & Vivian Li
-----
Description: implement pop up dialogs to display setting details,
             including engine settings, plugin settings, profile settings
'''
from typing import TypedDict, Dict, List
from view.config.Style import STYLE_DATA 
from view.widgets.Table import BaseTable
from view.widgets.TextDisplay import MarkdownDisplay, TextDisplay
from view.widgets.Label import Label 
from view.widgets.ScrollArea import ScrollArea
from view.widgets.GraphDisplay import GraphDisplay
from view.widgets.Background import initPrimaryColorBackground
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QWidget, QTableWidgetItem
from PyQt6.QtCore import Qt, QSize

class PluginInfo(TypedDict):
    suite_name : str 
    metadata : dict 
    dependency_graph: dict
    documentation: dict

class ProfileInfo(TypedDict):
    engine_setting: dict 
    engine_setting_name: str 
    plugin_setting: List[str]

class PluginSuiteDetails(QDialog):
    def __init__(self, pluginInfo: TypedDict) -> None:
        super().__init__()
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        self.maincontainer = QWidget()
        self._containerLayout = QVBoxLayout()
        self.maincontainer.setLayout(self._containerLayout)
        self._scroll = ScrollArea()
        self._scroll.setWidget(self.maincontainer)
        self._scroll.setWidgetResizable(True)
        self.name = Label(pluginInfo["suite_name"], STYLE_DATA.FontSize.HEADER1, STYLE_DATA.FontFamily.MAIN)
        self.metadata = TextDisplay(pluginInfo["metadata"])
        self.documentation = MarkdownDisplay(pluginInfo["documentation"])
        self.graph = GraphDisplay(pluginInfo["dependency_graph"])
        self._containerLayout.addWidget(self.name, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._containerLayout.addWidget(self.metadata)
        self._containerLayout.addWidget(self.graph)
        self._containerLayout.addWidget(self.documentation)
        self.setMinimumWidth(STYLE_DATA.Dimension.WIN_MIN_WIDTH)
        self.setMaximumWidth(STYLE_DATA.Dimension.WINMAXWIDTH)
        self._scroll.setMinimumWidth(STYLE_DATA.Dimension.WIN_MIN_WIDTH - STYLE_DATA.Dimension.MEDIUM_SPACING)
        self._scroll.setMaximumWidth(STYLE_DATA.Dimension.WINMAXWIDTH - STYLE_DATA.Dimension.MEDIUM_SPACING)
        self.setMaximumHeight(900)
        self.setMinimumHeight(750)
        self._scroll.setMaximumHeight(900)
        self._scroll.ensureWidgetVisible(self.maincontainer)
        self._layout.addWidget(self._scroll, alignment=Qt.AlignmentFlag.AlignHCenter)
        initPrimaryColorBackground(self)

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

class SettingDisplay(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._layout = QVBoxLayout()
        self.currentTableWidget = None 
        self.setLayout(self._layout)
        self.mainLabel = Label("Engine Setting Details", STYLE_DATA.FontSize.HEADER3, STYLE_DATA.FontFamily.MAIN)
        self._layout.addSpacing(20)
        self._layout.setSpacing(STYLE_DATA.Dimension.MEDIUM_SPACING)
        self._layout.addWidget(self.mainLabel, alignment=Qt.AlignmentFlag.AlignCenter)
    
    def setData(self, data: Dict[str, str]):
        if self.currentTableWidget:
            self._layout.removeWidget(self.currentTableWidget)
        newTable = BaseTable(["Setting Options", "Value"])
        newTable.setFixedSize(QSize(STYLE_DATA.Dimension.WIN_MIN_WIDTH//2, 
                                    STYLE_DATA.Dimension.SMALL_TABLE_HEIGHT))
        newTable.resizeCol([0.5, 0.5])
        for row, (key, value) in enumerate(data.items()):
            newTable.insertRow(row)
            key = key.replace("_", " ").upper()
            newTable.setItem(row, 0, QTableWidgetItem(key))
            newTable.setItem(row, 1, QTableWidgetItem(str(value)))
        self._layout.addWidget(newTable,alignment=Qt.AlignmentFlag.AlignHCenter)
        self.currentTableWidget = newTable

class PluginListDisplay(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        self.mainLabel = Label("Plugin Suite Setting", STYLE_DATA.FontSize.HEADER3, STYLE_DATA.FontFamily.MAIN)
        self._layout.addSpacing(20)
        self._layout.setSpacing(STYLE_DATA.Dimension.MEDIUM_SPACING)
        self._layout.addWidget(self.mainLabel, alignment=Qt.AlignmentFlag.AlignCenter)
    
    def setData(self, pluginSuites):
        newTable = BaseTable(["Applied Plugin Suite"])
        newTable.setFixedSize(QSize(STYLE_DATA.Dimension.WIN_MIN_WIDTH//2, 
                                    STYLE_DATA.Dimension.SMALL_TABLE_HEIGHT//2))
        newTable.resizeCol([1])
        for row, suite in enumerate(pluginSuites):
            newTable.insertRow(row)
            newTable.setItem(row, 0, QTableWidgetItem(suite))
        self._layout.addWidget(newTable,alignment=Qt.AlignmentFlag.AlignHCenter)
    
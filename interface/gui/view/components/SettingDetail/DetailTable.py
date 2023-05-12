"""
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
"""
from typing import TypedDict, Dict, List
from view.config.Style import STYLE_DATA
from view.widgets.Table import BaseTable
from view.widgets.Label import Label
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QWidget, QTableWidgetItem
from PyQt6.QtCore import Qt, QSize


class SettingDisplay(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._layout = QVBoxLayout()
        self.currentTableWidget = None
        self.setLayout(self._layout)
        self.mainLabel = Label(
            "Engine Setting Details",
            STYLE_DATA.FontSize.HEADER3,
            STYLE_DATA.FontFamily.MAIN,
        )
        self._layout.addSpacing(20)
        self._layout.setSpacing(STYLE_DATA.Dimension.MEDIUM_SPACING)
        self._layout.addWidget(self.mainLabel, alignment=Qt.AlignmentFlag.AlignCenter)

    def setData(self, data: Dict[str, str]):
        if self.currentTableWidget:
            self._layout.removeWidget(self.currentTableWidget)
        newTable = BaseTable(["Setting Options", "Value"])
        newTable.setFixedSize(
            QSize(
                STYLE_DATA.Dimension.WIN_MIN_WIDTH // 2,
                STYLE_DATA.Dimension.SMALL_TABLE_HEIGHT,
            )
        )
        newTable.resizeCol([0.480, 0.490])
        for row, (key, value) in enumerate(data.items()):
            newTable.insertRow(row)
            key = key.replace("_", " ").upper()
            newTable.setItem(row, 0, QTableWidgetItem(key))
            newTable.setItem(row, 1, QTableWidgetItem(str(value)))
        self._layout.addWidget(newTable, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.currentTableWidget = newTable


class PluginListDisplay(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        self.mainLabel = Label(
            "Plugin Suite Setting",
            STYLE_DATA.FontSize.HEADER3,
            STYLE_DATA.FontFamily.MAIN,
        )
        self._layout.addSpacing(20)
        self._layout.setSpacing(STYLE_DATA.Dimension.MEDIUM_SPACING)
        self._layout.addWidget(self.mainLabel, alignment=Qt.AlignmentFlag.AlignCenter)

    def setData(self, pluginSuites):
        newTable = BaseTable(["Applied Plugin Suite"])
        newTable.setFixedSize(
            QSize(
                STYLE_DATA.Dimension.WIN_MIN_WIDTH // 2,
                STYLE_DATA.Dimension.SMALL_TABLE_HEIGHT // 2,
            )
        )
        newTable.resizeCol([1])
        for row, suite in enumerate(pluginSuites):
            newTable.insertRow(row)
            newTable.setItem(row, 0, QTableWidgetItem(suite))
        self._layout.addWidget(newTable, alignment=Qt.AlignmentFlag.AlignHCenter)

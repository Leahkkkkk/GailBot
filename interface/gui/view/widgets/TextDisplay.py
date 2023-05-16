import markdown
import os
from dataclasses import dataclass

from .Label import Label
from gbLogger import makeLogger
from view.config.Style import STYLE_DATA
from config_frontend import PROJECT_ROOT
from .Background import initPrimaryColorBackground
from PyQt6.QtGui import QTextDocument, QIcon
from PyQt6.QtWidgets import (
    QTextEdit,
    QWidget,
    QGridLayout,
    QDialog,
    QTableWidget,
    QTableWidgetItem,
)
from typing import Dict
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (
    QTableWidget,
    QHeaderView,
    QAbstractItemView,
    QTableWidgetItem,
    QWidget,
    QVBoxLayout,
)
from PyQt6.QtCore import Qt, QModelIndex
from PyQt6.QtGui import QFont


@dataclass 
class DIMENSION:
    INSTRUCTION_TABLE_WIDTH = 850 
    INSTRUCTION_OPTION_WIDTH = 150
    INSTRUCTION_TEXT_WIDTH = 680
    INSTRUCTION_LABEL_WIDTH = 650
    MARKDOWN_HEIGHT = 350
    
class MarkdownDisplay(QTextEdit):
    def __init__(self, filePath):
        super().__init__()
        self.logger = makeLogger()
        with open(filePath, "r") as f:
            markdownText = f.read()
        markdownText = "<center> <h1>Documentation</h1></center> \n" + markdownText
        htmlText = markdown.markdown(markdownText)
        document = QTextDocument()
        document.setHtml(htmlText)
        self.setDocument(document)
        self.setReadOnly(True)
        initPrimaryColorBackground(self)
        self.setStyleSheet(STYLE_DATA.StyleSheet.basic)
        self.setMinimumHeight(350)
        self.verticalScrollBar().setStyleSheet(STYLE_DATA.StyleSheet.SCROLL_BAR)

    def colorChange(self, colormode):
        self.verticalScrollBar().setStyleSheet(STYLE_DATA.StyleSheet.SCROLL_BAR)
        self.setStyleSheet(STYLE_DATA.StyleSheet.basic)


class TextDisplay(QWidget):
    def __init__(self, data: Dict[str, str]):
        super().__init__()
        self._layout = QGridLayout()
        self.setLayout(self._layout)
        row = 0
        for key, value in data.items():
            key = key.capitalize()
            caption = Label(key, STYLE_DATA.FontSize.HEADER3)
            content = Label(value, STYLE_DATA.FontSize.BODY)
            self._layout.addWidget(
                caption, row, 0, alignment=Qt.AlignmentFlag.AlignHCenter
            )
            self._layout.addWidget(
                content, row, 1, alignment=Qt.AlignmentFlag.AlignLeft
            )
            row += 1
        initPrimaryColorBackground(self)
        self.setStyleSheet(STYLE_DATA.StyleSheet.basic)

    def colorChange(self, colormode):
        self.setStyleSheet(STYLE_DATA.StyleSheet.basic)

class DictionaryTableWidget(QTableWidget):
    def __init__(self, dictionary):
        super().__init__()
        self.setColumnCount(2)  # set the number of columns to 2
        self.setRowCount(
            len(dictionary)
        )  # set the number of rows to the length of the dictionary
        self.setHorizontalHeaderLabels(["Option", "Function"])  # set the column headers
        self.populateTable(dictionary)  # popu
        self._initStyle()
        STYLE_DATA.signal.changeColor.connect(self.colorChange)
        STYLE_DATA.signal.changeFont.connect(self.fontChange)

    def populateTable(self, dictionary):
        row = 0
        for key, value in dictionary.items():
            if "icon" in key:
                keyItem = QTableWidgetItem()
                key = key.replace("icon", "").replace(" ", "")
                keyItem.setIcon(QIcon(os.path.join(PROJECT_ROOT, key)))
                self.setItem(row, 0, keyItem)

            else:
                keyItem = Label(
                    key, STYLE_DATA.FontSize.BODY, STYLE_DATA.FontFamily.OTHER
                )
                keyItem.setFixedWidth(DIMENSION.INSTRUCTION_LABEL_WIDTH)
                self.setCellWidget(row, 0, keyItem)
                keyItem.setContentsMargins(10, 0, 0, 0)
            valueItem = Label(
                value, STYLE_DATA.FontSize.BODY, STYLE_DATA.FontFamily.OTHER
            )
            valueItem.setWordWrap(True)
            valueItem.setContentsMargins(10,0,0,0)
            self.setCellWidget(row, 1, valueItem)
            row += 1
            self.resizeRowsToContents()

    def _initStyle(self) -> None:
        """Initialize the table style"""
        self.verticalHeader().hide()
        self.horizontalHeader().setStyleSheet(STYLE_DATA.StyleSheet.TABLE_HEADER)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.horizontalHeader().setFixedHeight(45)
        self.setObjectName("FileTable")
        self.setStyleSheet(f"#FileTable{STYLE_DATA.StyleSheet.FILE_TABLE}")
        for i in range(self.columnCount()):
            self.horizontalHeader().setSectionResizeMode(
                i, QHeaderView.ResizeMode.Fixed
            )
        self.setFixedWidth(DIMENSION.INSTRUCTION_TABLE_WIDTH)
        self.setColumnWidth(0, DIMENSION.INSTRUCTION_OPTION_WIDTH)
        self.setColumnWidth(1, DIMENSION.INSTRUCTION_TEXT_WIDTH)
        
        self.verticalScrollBar().setStyleSheet(STYLE_DATA.StyleSheet.SCROLL_BAR)
        self.horizontalScrollBar().setStyleSheet(STYLE_DATA.StyleSheet.SCROLL_BAR)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setTextElideMode(Qt.TextElideMode.ElideMiddle)
        font = QFont(STYLE_DATA.FontFamily.OTHER, STYLE_DATA.FontSize.TABLE_ROW)
        self.setFont(font)
        self.setTextElideMode(Qt.TextElideMode.ElideMiddle)

    def colorChange(self):
        self.setStyleSheet(f"#FileTable{STYLE_DATA.StyleSheet.FILE_TABLE}")
        self.verticalScrollBar().setStyleSheet(STYLE_DATA.StyleSheet.SCROLL_BAR)
        self.horizontalScrollBar().setStyleSheet(STYLE_DATA.StyleSheet.SCROLL_BAR)
        self.horizontalHeader().setStyleSheet(STYLE_DATA.StyleSheet.TABLE_HEADER)

    def fontChange(self, font=None):
        font = QFont(STYLE_DATA.FontFamily.OTHER, STYLE_DATA.FontSize.TABLE_ROW)
        self.setFont(font)


class TextDisplayDialog(QDialog):
    def __init__(self, instructions) -> None:
        super().__init__()
        mainDisplay = DictionaryTableWidget(instructions)
        layout = QVBoxLayout()
        label = Label(
            "Tips and Hints", STYLE_DATA.FontSize.HEADER3, STYLE_DATA.FontFamily.MAIN
        )
        self.setLayout(layout)
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(mainDisplay, alignment=Qt.AlignmentFlag.AlignCenter)
        initPrimaryColorBackground(self)

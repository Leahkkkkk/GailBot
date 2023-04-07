import markdown
from .Label import Label
from gbLogger import makeLogger
from view.config.Style import  FontSize, StyleSheet, STYLE_DICT
from view.Signals import GlobalStyleSignal
from .Background import initPrimaryColorBackground
from PyQt6.QtGui import  QTextDocument
from PyQt6.QtWidgets import QTextEdit, QWidget, QGridLayout
from typing import List, Dict
from PyQt6.QtCore import Qt

STYLE_SHEET = StyleSheet
def changecolor(colormode):
    global STYLE_SHEET
    STYLE_SHEET = STYLE_DICT[colormode]
GlobalStyleSignal.changeColor.connect(changecolor)
class MarkdownDisplay(QTextEdit):
    def __init__(self, filePath):
        super().__init__()
        self.logger = makeLogger("F")
        with open(filePath, 'r') as f:
            markdownText = f.read()
        markdownText = "<center> <h1>Documentation</h1></center> \n" + markdownText 
        htmlText = markdown.markdown(markdownText)
        document = QTextDocument()
        document.setHtml(htmlText)
        self.setDocument(document)
        self.setReadOnly(True)
        initPrimaryColorBackground(self)
        self.setStyleSheet(STYLE_SHEET.basic)
        self.setMinimumHeight(350)
        self.verticalScrollBar().setStyleSheet(STYLE_SHEET.SCROLL_BAR)
        GlobalStyleSignal.changeColor.connect(self.colorChange)
    
    def colorChange(self, colormode):
        self.verticalScrollBar().setStyleSheet(STYLE_DICT[colormode].SCROLL_BAR)
        self.setStyleSheet(STYLE_DICT[colormode].basic)
class TextDisplay(QWidget):
    def __init__(self, data : Dict[str, str]):
        super().__init__()
        self._layout = QGridLayout()
        self.setLayout(self._layout)
        row = 0 
        for key, value in data.items():
            caption = Label(key, FontSize.HEADER3)
            content = Label(value, FontSize.BODY)
            self._layout.addWidget(caption, row, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
            self._layout.addWidget(content, row, 1, alignment=Qt.AlignmentFlag.AlignLeft)
            row += 1
        initPrimaryColorBackground(self)
        self.setStyleSheet(STYLE_SHEET.basic)
        GlobalStyleSignal.changeColor.connect(self.colorChange)

    def colorChange(self, colormode):
        self.setStyleSheet(STYLE_DICT[colormode].basic)
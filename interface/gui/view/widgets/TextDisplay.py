import markdown
from .Label import Label
from view.config.Style import FontFamily, FontSize
from PyQt6.QtGui import  QTextDocument
from PyQt6.QtWidgets import QTextEdit, QWidget, QGridLayout
from typing import List, Dict

class MarkdownDisplay(QTextEdit):
    def __init__(self, filePath):
        super().__init__()
        with open(filePath, 'r') as f:
            markdownText = f.read()
        htmlText = markdown.markdown(markdownText)
        document = QTextDocument()
        document.setHtml(htmlText)
        self.setDocument(document)
        self.setReadOnly(True)

class TextDisplay(QWidget):
   def __init__(self, data : Dict[str, str]):
        super().__init__()
        self._layout = QGridLayout()
        self.setLayout(self._layout)
        row = 0 
        for key, value in data.items():
            caption = Label(key, FontSize.HEADER3)
            content = Label(value, FontSize.BODY)
            self._layout.addWidget(caption, row, 0)
            self._layout.addWidget(content, row, 1)
            row += 1
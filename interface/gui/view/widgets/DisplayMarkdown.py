import markdown
from PyQt6.QtGui import  QTextDocument
from PyQt6.QtWidgets import QTextEdit

class DisplayMarkDown(QTextEdit):
    def __init__(self, filePath):
        super().__init__()
        with open(filePath, 'r') as f:
            markdownText = f.read()
        htmlText = markdown.markdown(markdownText)
        document = QTextDocument()
        document.setHtml(htmlText)
        self.setDocument(document)
        self.setReadOnly(True)
      
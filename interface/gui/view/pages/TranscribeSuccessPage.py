from PyQt6.QtWidgets import *
from PyQt6 import QtCore

""" class for trancription success page """
class TranscribeSuccessPage(QWidget):
    """ initialize class """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._initWidget()
        self._initLayout()
    """ intialize widgets """
    def _initWidget(self):
        self.label = QLabel("Transcribe Successful")
        self.moreBtn = QPushButton("Transcribe More File")
        self.returnBtn = QPushButton("Return to Home")
        self.quitBtn = QPushButton("Quit Gailbot")
        self.postSetBtn = QPushButton("Post Transcribtion Setting")
    """ initialize page layout """
    def _initLayout(self):
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addWidget(self.postSetBtn)
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.moreBtn)
        self.verticalLayout.addWidget(self.returnBtn)
        self.verticalLayout.addWidget(self.quitBtn)
        
        

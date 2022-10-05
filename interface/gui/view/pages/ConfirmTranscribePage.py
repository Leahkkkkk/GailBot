from PyQt6.QtWidgets import *
from PyQt6 import QtCore

""" class for confirm transcription page """
class ConfirmTranscribePage(QWidget):
    """ initliaze class """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._initWidget()
        self._initLayout()
    """ initlialize widget """
    def _initWidget(self):
        self.label = QLabel("Confirm Transcribe")
        self.confirmBtn = QPushButton("Confirm")
        self.cancelBtn = QPushButton("Cancel")
    """ initialize layout"""
    def _initLayout(self):
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.confirmBtn)
        self.verticalLayout.addWidget(self.cancelBtn)
        
 
        
    
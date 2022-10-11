'''
File: TranscribeSuccessPage.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 11:11:31 am
Modified By:  Siara Small  & Vivian Li
-----
'''
from view.widgets import (
    FileTable,
    Button,
    Label
)

from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget
)
from PyQt6 import QtCore

class TranscribeSuccessPage(QWidget):
    """ class for trancription success page """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._initWidget()
        self._initLayout()
        
    def _initWidget(self):
        """ intialize widgets """
        self.label = QLabel("Transcribe Successful")
        self.fileTable = FileTable.successTable()
        self.moreBtn = QPushButton("Transcribe More File")
        self.returnBtn = QPushButton("Return to Home")
        self.quitBtn = QPushButton("Quit Gailbot")
        self.postSetBtn = QPushButton("Post Transcribtion Setting")
        
    def _initLayout(self):
        """ initialize page layout """
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addWidget(self.postSetBtn)
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.fileTable)
        self.verticalLayout.addWidget(self.moreBtn)
        self.verticalLayout.addWidget(self.returnBtn)
        self.verticalLayout.addWidget(self.quitBtn)
        
        

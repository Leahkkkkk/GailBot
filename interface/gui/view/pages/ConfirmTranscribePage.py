'''
File: ConfirmTranscribePage.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 11:05:38 am
Modified By:  Siara Small  & Vivian Li
-----
'''

from stat import filemode
from view.style import Background
from view.widgets import ( Label, 
                           Button, 
                           FileTable ) 

from PyQt6.QtWidgets import (
    QWidget, 
    QLabel, 
    QPushButton, 
    QVBoxLayout
)

class ConfirmTranscribePage(QWidget):
    """ Confirm transcription page """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._initWidget()
        self._initLayout()
        self._initStyle()
    
    def _initWidget(self):
        """ initlialize widget """
        self.label = QLabel("Confirm Transcribe")
        self.fileTable = FileTable.confirmTable(self)
        self.confirmBtn = QPushButton("Confirm")
        self.cancelBtn = QPushButton("Cancel")
    
    def _initLayout(self):
        """ initialize layout"""
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.fileTable)
        self.verticalLayout.addWidget(self.confirmBtn)
        self.verticalLayout.addWidget(self.cancelBtn)
    
    def _initStyle(self):
        Background.initBackground(self)
        
 
        
    
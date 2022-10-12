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
from view.style.styleValues import FontFamily, FontSize, Color
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

from PyQt6 import QtCore
from PyQt6.QtCore import Qt

class ConfirmTranscribePage(QWidget):
    """ Confirm transcription page """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._initWidget()
        self._initLayout()
        self._initStyle()
    
    def _initWidget(self):
        """ initlialize widget """
        self.label = Label.Label("Confirm Transcription", FontSize.HEADER1, FontFamily.MAIN)
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.fileTable = FileTable.confirmTable(self)
        self.confirmBtn = Button.ColoredBtn("Confirm", Color.GREEN)
        self.cancelBtn = Button.ColoredBtn("Cancel", Color.ORANGE)
    
    def _initLayout(self):
        """ initialize layout"""
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.fileTable)
        self.verticalLayout.addWidget(self.confirmBtn, 4, 
                                      alignment = Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout.addWidget(self.cancelBtn, 4, 
                                      alignment = Qt.AlignmentFlag.AlignHCenter)
    
    def _initStyle(self):
        Background.initBackground(self)
        self.confirmBtn.setMinimumSize(QtCore.QSize(150,30))
        self.cancelBtn.setMinimumSize(QtCore.QSize(150,30))
        
 
        
    
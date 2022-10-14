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
                           FileTable,
                           TableWidgets) 


from PyQt6.QtWidgets import (
    QWidget, 
    QLabel, 
    QPushButton, 
    QVBoxLayout,
    QHBoxLayout
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
        self.showFileDetail = True
        
    
    def _initWidget(self):
        """ initlialize widget """
        self.label = Label.Label("Confirm Files and Settings", 
                                 FontSize.HEADER2, 
                                 FontFamily.MAIN)
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.fileTable = FileTable.confirmTable(self)
        self.fileTable.setFixedHeight(65)
        self.fileInfo = TableWidgets.FullFileDetailWidget()
        self.fileInfo.setMaximumHeight(700)
        self.bottomButton = QWidget()
        self.confirmBtn = Button.ColoredBtn("Confirm", Color.GREEN)
        self.cancelBtn = Button.ColoredBtn("Cancel", Color.ORANGE)
    
    def _initLayout(self):
        """ initialize layout"""
        self.verticalLayout = QVBoxLayout()
        self.horizontalLayout = QHBoxLayout()
        self.bottomButton.setLayout(self.horizontalLayout)
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addWidget(self.label)
        self.label.setContentsMargins(0,20,0,20)
        self.verticalLayout.addWidget(self.fileTable,
                                      alignment = Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        
        self.horizontalLayout.addWidget(self.confirmBtn, 
                                      alignment = Qt.AlignmentFlag.AlignRight)
        
        self.horizontalLayout.addWidget(self.cancelBtn, 
                                      alignment = Qt.AlignmentFlag.AlignHCenter)
        
        self.bottomButton.setContentsMargins(0,0,0,0)
        
        self.verticalLayout.addWidget(self.fileInfo, 8,
                                      alignment = Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        
        self.verticalLayout.addWidget(self.bottomButton,
                                      alignment=Qt.AlignmentFlag.AlignHCenter)
    
    def _initStyle(self):
        Background.initBackground(self)
        self.confirmBtn.setMinimumSize(QtCore.QSize(150,30))
        self.cancelBtn.setMinimumSize(QtCore.QSize(150,30))
    
    def toggleFileDetail(self):
        if self.showFileDetail:
            self.fileInfo.hide()
        else:
            self.fileInfo.show()
        
        self.showFileDetail = not self.showFileDetail
        
 
        
    
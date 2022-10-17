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

from view.style.styleValues import FontFamily, FontSize, Color
from view.style.Background import initImgBackground
from view.widgets import ( Label, 
                           Button, 
                           TableWidgets,
                           FileTable) 


from PyQt6.QtWidgets import (
    QWidget, 
    QLabel, 
    QPushButton, 
    QVBoxLayout,
    QHBoxLayout
)

from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QObject, pyqtSignal

class Signal(QObject):
    transcribeFile = pyqtSignal(dict)


class ConfirmTranscribePage(QWidget):
    """ Confirm transcription page """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._initWidget()
        self._initLayout()
        self._initStyle()
        self.showFileDetail = True
        self.signal = Signal()
    
    def toggleFileDetail(self):
        if self.showFileDetail:
            self.fileInfo.hide()
        else:
            self.fileInfo.show()
        
        self.showFileDetail = not self.showFileDetail
        
    def _initWidget(self):
        """ initlialize widget """
        self.label = Label.Label("Confirm Files and Settings", 
                                 FontSize.HEADER2, 
                                 FontFamily.MAIN)
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.fileTable = FileTable.FileTable(FileTable.ConfirmHeader, {}, {"setting"})
        self.fileTable.resizeCol(FileTable.ConfirmHeaderDimension)
        self.fileInfo = TableWidgets.FullFileDetailWidget()
        self.fileInfo.setMaximumHeight(700)
        self.bottomButton = QWidget()
        self.confirmBtn = Button.ColoredBtn("Confirm", Color.GREEN)
        self.cancelBtn = Button.ColoredBtn("Cancel", Color.ORANGE)
        self.confirmBtn.clicked.connect(self._sendTranscribeSignal)
    
    def _initLayout(self):
        """ initialize layout"""
        self.verticalLayout = QVBoxLayout()
        self.horizontalLayout = QHBoxLayout()
        self.bottomButton.setLayout(self.horizontalLayout)
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addWidget(self.label)
        self.label.setContentsMargins(0,20,0,50)
        self.verticalLayout.addWidget(self.fileTable,
                                      alignment = Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        
        self.horizontalLayout.addWidget(self.confirmBtn, 
                                      alignment = Qt.AlignmentFlag.AlignRight)
        
        self.horizontalLayout.addWidget(self.cancelBtn, 
                                      alignment = Qt.AlignmentFlag.AlignHCenter)
        
        self.bottomButton.setContentsMargins(0,0,0,0)
        
        self.verticalLayout.addWidget(self.fileInfo, 8,
                                      alignment = Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.verticalLayout.addStretch()
        
        self.verticalLayout.addWidget(self.bottomButton,
                                      alignment=Qt.AlignmentFlag.AlignHCenter)
    
    def _initStyle(self):
        initImgBackground(self,"backgroundConfirmPage.png")
        self.confirmBtn.setMinimumSize(QtCore.QSize(150,30))
        self.cancelBtn.setMinimumSize(QtCore.QSize(150,30))
    
  
    def _sendTranscribeSignal(self):
        self.signal.transcribeFile.emit(self.fileTable.filedata)
   
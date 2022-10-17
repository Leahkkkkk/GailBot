import os

from view.components import MsgBox
from view.widgets import (
    Label,   
    Button)
from util import Path
from view.widgets import Button
from view.style.styleValues import Color, FontSize, Dimension, FontFamily
from view.style.Background import initImgBackground


from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QMovie
from PyQt6 import QtCore
from PyQt6.QtCore import Qt

""" class for transcription in progress page """
class TranscribeProgressPage(QWidget):
    """ initialize class """
    def __init__(self, parent, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._initWidget()
        self._initstyle()
        self._initLayout()
        self._connectSignal()
        self.parent = parent
      
    def loadStart(self):
        """ start loading icon movie """
        self.IconImg.start()
        
    def loadStop(self):
        """ stop loading icon movie """
        self.IconImg.stop()
        
    def _initWidget(self):
        """ initialize widgets """
        self.label = Label.Label("Transcription in Progress",
                                 FontSize.HEADER1, 
                                 FontFamily.MAIN)
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.loadIcon = QLabel()
        self.IconImg = QMovie(os.path.join(Path.getProjectRoot(), "view/asset/gbloading.gif"))
        self.loadIcon.setMovie(self.IconImg)
        self.loadStart()
       
        self.Formatting = Label.Label("Formatting file headers...",
                                      FontSize.SMALL,
                                      FontFamily.OTHER)
        self.Formatting.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.InProgress = Label.Label("Files in progress:",
                                        FontSize.BODY,
                                        FontFamily.OTHER)
        # self.fileTable = FileTable.progressTable()
        self.cancelBtn = Button.ColoredBtn("Cancel", Color.ORANGE, FontSize.BTN)
        
    def _initstyle(self):
        """ styles loading icon movie """
        self.loadIcon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.loadIcon.setFixedSize(QtCore.QSize(80, 80))
        self.loadIcon.setScaledContents(True)
        self.cancelBtn.setMinimumSize(QtCore.QSize(130, 30))
        self.cancelBtn.setMinimumSize(Dimension.BGBUTTON)
        initImgBackground(self, "backgroundConfirmPage.png")
        
        
    def _initLayout(self):
        """ intiializes layout """
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addWidget(self.label)
        self.label.setContentsMargins(0,20,0,0)
        self.verticalLayout.addWidget(self.loadIcon, 
                                      alignment = Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.verticalLayout.addWidget(self.Formatting, alignment =Qt.AlignmentFlag.AlignTop)
        self.verticalLayout.addWidget(self.InProgress, alignment =Qt.AlignmentFlag.AlignTop)
        # self.verticalLayout.addWidget(self.fileTable, 
        #                               alignment= Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(self.cancelBtn, 
                                      alignment = Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout.setSpacing(10)
        self.InProgress.setContentsMargins(80,0,0,0)
        self.loadIcon.setContentsMargins(0,0,0,0)
        # self.fileTable.setMaximumHeight(300)
        

    def _connectSignal(self):
        """ connects signal """
        self.cancelBtn.clicked.connect(self._confirm)
        
    def _confirm(self):
        """ handles confirm transcription message box """
        self.confirmCancel = MsgBox.ConfirmBox("Confirm cancel?", 
                                               self.parent.confirmCancel)
        

    
import os

from view.components import MsgBox
from view.widgets import (
    Label, 
    FileTable, 
    ToggleView, 
    Button)
from util import Path
from view.widgets import Button
from view.style.styleValues import Color, FontSize, Dimension, FontFamily

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
        # self.loadIcon.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.loadStart()
       
        self.Formatting = Label.Label("Formatting file headers...",
                                      FontSize.SMALL,
                                      FontFamily.OTHER)
        self.Formatting.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.InProgress = Label.Label("Files in progress:",
                                        FontSize.HEADER3,
                                        FontFamily.OTHER)
        self.fileTable = FileTable.progressTable()
        self.cancelBtn = Button.ColoredBtn("Cancel", Color.ORANGE, FontSize.BTN)
        
    def _initstyle(self):
        """ styles loading icon movie """
        #TODO: fix alignment of loading movie
        self.loadIcon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.loadIcon.setMinimumSize(QtCore.QSize(150, 150))
        self.loadIcon.setMaximumSize(QtCore.QSize(150, 150))
        self.loadIcon.setScaledContents(True)
        self.cancelBtn.setMinimumSize(QtCore.QSize(130, 30))
        
    def _initLayout(self):
        """ intiializes layout """
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.loadIcon, alignment = Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout.addWidget(self.Formatting)
        self.verticalLayout.addWidget(self.InProgress)
        self.verticalLayout.addWidget(self.fileTable)
        self.verticalLayout.addWidget(self.cancelBtn, 4, 
                                      alignment = Qt.AlignmentFlag.AlignHCenter)
    def _initStyle(self):
        """ initialize style """
        self.cancelBtn.setMinimumSize(Dimension.BGBUTTON)
        
    def _connectSignal(self):
        """ connects signal """
        self.cancelBtn.clicked.connect(self._confirm)
        
    def _confirm(self):
        """ handles confirm transcription message box """
        self.confirmCancel = MsgBox.ConfirmBox("Confirm cancel?", 
                                               self.parent.confirmCancel)
        

    
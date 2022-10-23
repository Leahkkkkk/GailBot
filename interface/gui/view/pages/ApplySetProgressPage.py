'''
File: ApplySetProgressPage.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 11:04:03 am
Modified By:  Siara Small  & Vivian Li
-----
'''
import os

from util import Path

from view.widgets import Label, Button, FileTable
from view.style.styleValues import Color, FontSize, FontFamily
from view.style.Background import initImgBackground
from view.style.styleValues import Color, FontSize, FontFamily, Dimension
from view.components import MsgBox

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea
from PyQt6.QtGui import QMovie
from PyQt6 import QtCore
from PyQt6.QtCore import Qt


class ApplySetProgressPage(QWidget):
    """ apply settings in progress page """
    def __init__(self, parent, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._initWidget()
        self._initLayout()
        self._initStyle()
        self._connectSignal()
        self.parent = parent

    def loadStart(self):
        """ start loading icon movie """
        self.IconImg.start()
        
    def loadStop(self):
        """ stop loading icon movie """
        self.IconImg.stop()
    
    def _initWidget(self):
        """ initialize widget """
        self.label = Label.Label("Applying Settings", 
                                 FontSize.HEADER1, 
                                 FontFamily.MAIN)
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.loadIcon = QLabel()
        self.IconImg = QMovie(os.path.join(Path.getProjectRoot(), "view/asset/gbloading.gif"))
        self.loadIcon.setMovie(self.IconImg)
        self.loadStart()
        self.setLoadingText("Formatting file headers...")
        self.loadingText.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.InProgress = Label.Label("Files in progress:", 
                                        FontSize.HEADER3,
                                        FontFamily.OTHER)
        self.cancelBtn = Button.ColoredBtn("Cancel", Color.ORANGE, FontSize.BTN)
        self.fileTable = FileTable.FileTable(FileTable.ProgressHeader, {}, {})
        self.fileTable.resizeCol(FileTable.ProgressDimension)
        
    def _initLayout(self):
        """ initialize vertical layout """
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addStretch(1.2)
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addStretch(1.8)
        self.verticalLayout.addWidget(self.loadIcon, alignment = Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout.addWidget(self.loadingText)
        self.verticalLayout.addWidget(self.InProgress)
        self.InProgress.setContentsMargins(80,0,0,0)
        self.verticalLayout.addWidget(self.fileTable, stretch=5,
                                      alignment= Qt.AlignmentFlag.AlignCenter|Qt.AlignmentFlag.AlignTop)
        self.verticalLayout.addWidget(self.cancelBtn,
                                      alignment = Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        
        
    def _initStyle(self):
        """ initialize style """
        """ styles loading icon movie """
        self.loadIcon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.loadIcon.setFixedSize(QtCore.QSize(80, 80))
        self.loadIcon.setScaledContents(True)
        """styles other"""
        initImgBackground(self, "backgroundSubPages.png")
        self.cancelBtn.setMinimumSize(QtCore.QSize(150,30))
        self.cancelBtn.setMinimumSize(Dimension.BGBUTTON)

    def _connectSignal(self):
        """ connects signal """
        self.cancelBtn.clicked.connect(self._confirm)
        
    def _confirm(self):
        """ handles confirm transcription message box """
        self.confirmCancel = MsgBox.ConfirmBox("Confirm cancellation?", 
                                               self.parent.confirmCancel)

    def setLoadingText(self, text):
        self.loadingText = Label.Label(text,
                                      FontSize.SMALL,
                                      FontFamily.OTHER)
        

    
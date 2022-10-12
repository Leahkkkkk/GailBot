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
from view.style import Background

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea
from PyQt6.QtGui import QMovie
from PyQt6 import QtCore
from PyQt6.QtCore import Qt


class ApplySetProgressPage(QWidget):
    """ apply settings in progress page """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._initWidget()
        self._initLayout()
        self._initStyle()

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
        # self.loadIcon.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.loadStart()
        self.Formatting = QLabel("Formatting file headers...")
        self.Formatting.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.InProgress = Label.Label("Files in progress:", 
                                        FontSize.HEADER3,
                                        FontFamily.OTHER)
        self.fileTable = FileTable.progressTable()
        self.cancelBtn = Button.ColoredBtn("Cancel", Color.ORANGE, FontSize.BTN)
        
    def _initLayout(self):
        """ initialize vertical layout """
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.loadIcon, alignment = Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout.addWidget(self.Formatting)
        self.verticalLayout.addWidget(self.InProgress)
        self.verticalLayout.addWidget(self.fileTable, stretch=5,
                                      alignment= Qt.AlignmentFlag.AlignCenter|Qt.AlignmentFlag.AlignTop)
        self.verticalLayout.addWidget(self.cancelBtn,
                                      alignment = Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        
        
    def _initStyle(self):
        """ initialize style """
        """ styles loading icon movie """
        #TODO: fix alignment of loading movie
        self.loadIcon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.loadIcon.setFixedSize(QtCore.QSize(80, 80))
        self.loadIcon.setScaledContents(True)
        """styles other"""
        Background.initBackground(self)
        self.cancelBtn.setMinimumSize(QtCore.QSize(150,30))
        

    
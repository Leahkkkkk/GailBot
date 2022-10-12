'''
File: ApplySetSuccessPage.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 11:05:10 am
Modified By:  Siara Small  & Vivian Li
-----
'''

from view.widgets import (
    FileTable,
    Button,
    Label
)
from view.style import Background

from view.style.styleValues import FontFamily, FontSize, Color
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout

from PyQt6 import QtCore
from PyQt6.QtCore import Qt

class ApplySetSuccessPage(QWidget):
    """ apply settings successful page """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._initWidget()
        self._initHorizontalLayout()
        self._initLayout()
        self._initStyle()
        
    def _initWidget(self):
        """ initialize widget """ 
        self.label = Label.Label("Settings Successfully Applied", 
                                FontSize.HEADER1,
                                FontFamily.MAIN)
        self.filesAndLocations = Label.Label("Files and locations:",
                                FontSize.HEADER3,
                                FontFamily.OTHER)
        self.fileTable = FileTable.successTable()
        self.moreBtn = Button.ColoredBtn("Process more files", Color.GREEN)
        self.returnBtn = Button.ColoredBtn("Return to main menu", Color.BLUEMEDIUM)
        self.quitBtn = Button.ColoredBtn("Quit Gailbot", Color.ORANGE)

    def _initLayout(self):
        """ initalize layout """
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.filesAndLocations)
        self.verticalLayout.addWidget(self.fileTable)
        self.verticalLayout.addWidget(self.horizontal)
        self.verticalLayout.addWidget(self.quitBtn, 4, 
                                      alignment = Qt.AlignmentFlag.AlignHCenter)

    def _initHorizontalLayout(self):
        #TODO: make buttons closer together
        self.horizontal = QWidget()
        self.horizontalLayout = QHBoxLayout()
        self.horizontal.setLayout(self.horizontalLayout)
        self.horizontalLayout.addWidget(self.moreBtn)
        self.horizontalLayout.addWidget(self.returnBtn)

    def _initStyle(self):
        """ initalize style """   
        Background.initBackground(self)
        self.moreBtn.setMinimumSize(QtCore.QSize(150,30))
        self.returnBtn.setMinimumSize(QtCore.QSize(150,30))
        self.quitBtn.setMinimumSize(QtCore.QSize(150,30))

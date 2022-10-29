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

import tomli

from view.widgets import (
    Button,
    Label,
    FileTable
)

from view.Signals import FileSignals
from view.style.styleValues import Color, FontSize, Dimension, FontFamily
from view.style.Background import initImgBackground
from view.Text.TranscribeSuccessPageText import TranscribeSuccessText

from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget
)

from PyQt6 import QtCore

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QMovie
from PyQt6 import QtCore
from PyQt6.QtCore import Qt

class TranscribeSuccessPage(QWidget):
    """ class for trancription success page """
    def __init__(self, signal:FileSignals, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.signal = signal
        self._initConfig()
        self._initWidget()
        self._initStyle()
        self._initLayout()
        
    def _initWidget(self):
        """ intialize widgets """
        self.label = Label.Label(TranscribeSuccessText.mainLabelText,
                                        self.config["fontSizes"]["HEADER1"],
                                        FontFamily.MAIN)
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.transcribedFiles = Label.Label(TranscribeSuccessText.transcribedFilesText,
                                        self.config["fontSizes"]["HEADER3"],
                                        FontFamily.OTHER)
        self.transcribedFiles.setContentsMargins(30,0,0,0)
        self.moreBtn = Button.ColoredBtn(TranscribeSuccessText.moreBtnText, self.config["colors"]["GREEN"])
        self.returnBtn = Button.ColoredBtn(TranscribeSuccessText.returnBtnText, self.config["colors"]["BLUEMEDIUM"])
        self._initHorizontalLayout()
        self.fileTable = FileTable.FileTable(
            FileTable.SuccessHeader, 
            self.signal,
            {}, 
            {})
        self.fileTable.resizeCol(FileTable.SuccessDimension)
        
    def _initLayout(self):
        """ initialize page layout """
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.label.setContentsMargins(0,30,0,20)
        """ add widget to layout """
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.transcribedFiles)
        self.transcribedFiles.setContentsMargins(80,0,0,0)
        self.verticalLayout.addWidget(self.fileTable,alignment = Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(self.horizontal)
        self.verticalLayout.setSpacing(20)

    def _initHorizontalLayout(self):
        #TODO: make buttons closer together
        self.horizontal = QWidget()
        self.horizontalLayout = QHBoxLayout()
        self.horizontal.setLayout(self.horizontalLayout)
        self.horizontalLayout.addWidget(self.moreBtn)
        self.horizontalLayout.addWidget(self.returnBtn)

    def _initStyle(self):
        self.moreBtn.setMinimumSize(QtCore.QSize(150,30))
        self.returnBtn.setMinimumSize(QtCore.QSize(150,30))
        initImgBackground(self, "backgroundConfirmPage.png")

    def _initConfig(self):
        with open("controller/interface.toml", mode="rb") as fp:
            self.config = tomli.load(fp)
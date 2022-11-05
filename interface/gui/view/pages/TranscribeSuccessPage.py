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

from view.widgets import (
    Button,
    Label,
    FileTable
)

from util.Style import Color,  FontSize, Dimension
from util.Text import TranscribeSuccessText as Text
from view.Signals import FileSignals
from view.style.styleValues import FontFamily

from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QWidget
)

from PyQt6 import QtCore

from PyQt6.QtWidgets import QVBoxLayout, QWidget
from PyQt6 import QtCore
from PyQt6.QtCore import Qt


SuccessHeader = ["Type",
                 "Name",
                 "Status",
                 "Output"]
SuccessDimension = [0.17, 0.35, 0.25, 0.23]

class TranscribeSuccessPage(QWidget):
    """ class for trancription success page """
    def __init__(self, signal:FileSignals, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.signal = signal
        self._initWidget()
        self._initStyle()
        self._initLayout()
        
    def _initWidget(self):
        """ intialize widgets """
        self.label = Label.Label(
            Text.mainLabelText,
            FontSize.HEADER2,
            FontFamily.MAIN)
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.transcribedFiles = Label.Label(
            Text.transcribedFilesText, FontSize.HEADER3, FontFamily.MAIN)
        self.transcribedFiles.setContentsMargins(30,0,0,0)
        self.moreBtn = Button.ColoredBtn(
            Text.moreBtnText, Color.GREEN)
        self.returnBtn = Button.ColoredBtn(
            Text.returnBtnText, Color.BLUEMEDIUM)
        self._initHorizontalLayout()
        self.fileTable = FileTable.FileTable(
            SuccessHeader, self.signal)
        self.fileTable.resizeCol(SuccessDimension)
        
    def _initLayout(self):
        """ initialize page layout """
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.label.setContentsMargins(0,30,0,20)
        """ add widget to layout """
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.transcribedFiles)
        self.transcribedFiles.setContentsMargins(80,0,0,0)
        self.verticalLayout.addWidget(
            self.fileTable,alignment = Qt.AlignmentFlag.AlignHCenter)
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
        self.moreBtn.setMinimumSize(
            QtCore.QSize(Dimension.BTNWIDTH, Dimension.BTNHEIGHT))
        self.returnBtn.setMinimumSize(
            QtCore.QSize(Dimension.BTNWIDTH, Dimension.BTNHEIGHT))


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

from util.Style import (
    Color, 
    Dimension, 
    FileTableDimension
)
from util.Style import FontSize as FS
from util.Text import TranscribeSuccessText as Text
from util.Text import FileTableHeader
from view.widgets import (
    Button,
    Label,
    FileTable
)
from view.style.Background import addLogo
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



class TranscribeSuccessPage(QWidget):
    """ class for trancription success page """
    def __init__(self, signal:FileSignals, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.signal = signal
        self._initWidget()
        self._initStyle()
        self._initLayout()
        
    def _initWidget(self):
        """ intializes widgets on the page """
        self.label = Label.Label(
            Text.mainLabelText,
            FS.HEADER2,
            FontFamily.MAIN)
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.transcribedFiles = Label.Label(
            Text.transcribedFilesText, FS.HEADER3, FontFamily.MAIN)
        self.transcribedFiles.setContentsMargins(30,0,0,0)
        self.moreBtn = Button.ColoredBtn(
            Text.moreBtnText, Color.GREEN)
        self.returnBtn = Button.ColoredBtn(
            Text.returnBtnText, Color.BLUEMEDIUM)
        self._initHorizontalLayout()
        self.fileTable = FileTable.FileTable(
            FileTableHeader.successPage, self.signal)
        self.fileTable.resizeCol(FileTableDimension.successPage)
        
    def _initLayout(self):
        """ initializes page layout """
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        addLogo(self.verticalLayout)
        """ adds widgets to the vertical layout """
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.transcribedFiles)
        self.verticalLayout.addWidget(
            self.fileTable,alignment = Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout.addWidget(self.horizontal)
        self.verticalLayout.setSpacing(40)
        self.verticalLayout.addStretch

    def _initHorizontalLayout(self):
        """ initializes the horizontal layout of buttons to be added to the vertical layout """
        #TODO: make buttons closer together
        self.horizontal = QWidget()
        self.horizontalLayout = QHBoxLayout()
        self.horizontal.setLayout(self.horizontalLayout)
        self.horizontalLayout.addWidget(self.moreBtn)
        self.horizontalLayout.addWidget(self.returnBtn)

    def _initStyle(self):
        """ initializes the style of the buttons on the page """
        self.moreBtn.setMinimumSize(
            QtCore.QSize(Dimension.BTNWIDTH, Dimension.BTNHEIGHT))
        self.returnBtn.setMinimumSize(
            QtCore.QSize(Dimension.BTNWIDTH, Dimension.BTNHEIGHT))


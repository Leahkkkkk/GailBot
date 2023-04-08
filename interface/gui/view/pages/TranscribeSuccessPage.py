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

from view.config.Style import (
    STYLE_DATA,
    FileTableDimension
)
from view.config.Text import TranscribeSuccessText as Text
from view.config.Text import FileTableHeader
from view.widgets import (
    ColoredBtn,
    Label,
    FileTable
)
from view.widgets.Background import addLogo
from view.Signals import FileSignals
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QWidget
)
from PyQt6 import QtCore
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from PyQt6 import QtCore
from PyQt6.QtCore import Qt

right = Qt.AlignmentFlag.AlignRight
left = Qt.AlignmentFlag.AlignLeft

class TranscribeSuccessPage(QWidget):
    """ class for transcription success page """
    def __init__(self, signal:FileSignals, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.signal = signal
        self._initWidget()
        self._initStyle()
        self._initLayout()
        
    def _initWidget(self):
        """ initializes widgets on the page """
        self.label = Label(
            Text.mainLabelText, STYLE_DATA.FontSize.HEADER2, STYLE_DATA.FontFamily.MAIN)
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.moreBtn = ColoredBtn(
            Text.moreBtnText, STYLE_DATA.Color.SECONDARY_BUTTON)
        self.returnBtn = ColoredBtn(
            Text.returnBtnText, STYLE_DATA.Color.PRIMARY_BUTTON)
        self._initHorizontalLayout()
        self.fileTable = FileTable(
            FileTableHeader.successPage, self.signal)
        self.fileTable.resizeCol(FileTableDimension.successPage)
        
    def _initLayout(self):
        """ initializes page layout """
        self.verticalLayout = QVBoxLayout()
        self.container = QWidget()
        self.containerLayout = QVBoxLayout()
        self.container.setFixedWidth(STYLE_DATA.Dimension.TABLECONTAINERWIDTH)
        self.container.setLayout(self.containerLayout)
        self.containerLayout.addWidget(self.fileTable)
        self.setLayout(self.verticalLayout)
        addLogo(self.verticalLayout)
        """ adds widgets to the vertical layout """
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(
            self.container,alignment = Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout.addWidget(self.horizontal)
        self.verticalLayout.setSpacing( STYLE_DATA.Dimension.LARGE_SPACING)

    def _initHorizontalLayout(self):
        """ initializes the horizontal layout of buttons to 
            be added to the vertical layout """
        self.horizontal = QWidget()
        self.horizontalLayout = QHBoxLayout()
        self.horizontal.setLayout(self.horizontalLayout)
        self.horizontalLayout.addWidget(self.moreBtn, alignment = right)
        self.horizontalLayout.addWidget(self.returnBtn, alignment = left)
        self.horizontalLayout.setSpacing( STYLE_DATA.Dimension.LARGE_SPACING)

    def _initStyle(self):
        """ initializes the style of the buttons on the page """
        self.moreBtn.setMinimumSize(
            QtCore.QSize(STYLE_DATA.Dimension.BTNWIDTH,  STYLE_DATA.Dimension.BTNHEIGHT))
        self.returnBtn.setMinimumSize(
            QtCore.QSize(STYLE_DATA.Dimension.BTNWIDTH, STYLE_DATA.Dimension.BTNHEIGHT))
        STYLE_DATA.signal.changeFont.connect(self.fontchange)

    def fontchange(self):
        self.label.fontChange(STYLE_DATA.FontSize.HEADER2)

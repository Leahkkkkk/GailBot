'''
File: TranscribeProgressPage.py
Project: GailBot GUI
File Created: Friday, 4th November 2022 1:01:27 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Saturday, 5th November 2022 7:06:45 pm
Modified By:  Siara Small  & Vivian Li
-----
'''

import os
from typing import Tuple
from view.config.Style import (
    STYLE_DATA,
    FileTableDimension 
)
from view.config.Text import TranscribeProgressText as Text
from view.config.Text import FileTableHeader
from config_frontend import PROJECT_ROOT
from gbLogger import makeLogger
from view.pages.BasicPage import BasicPage
from view.Signals import FileSignals
from view.widgets import (
    Label,   
    ColoredBtn,
    FileTable
)


from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QMovie, QFont
from PyQt6 import QtCore
from PyQt6.QtCore import Qt

top = Qt.AlignmentFlag.AlignTop
center = Qt.AlignmentFlag.AlignHCenter


class TranscribeProgressPage(BasicPage):
    """ class for transcription in progress page """
    def __init__(
        self, 
        signals: FileSignals, 
        * args, 
        **kwargs) -> None:
        """ initializes class """
        super().__init__(*args, **kwargs)
        self.signals = signals
        self.logger = makeLogger("F")
        self._initWidget()
        self._initstyle()
        self._initLayout()
        self._connectSignal()
      
    def loadStart(self):
        """ start loading icon movie """
        self.IconImg.start()
        
    def loadStop(self):
        """ stop loading icon movie """
        self.IconImg.stop()
        
    def _initWidget(self):
        """ initialize widgets """
        self.label = Label(Text.mainLabelText, STYLE_DATA.FontSize.HEADER2, STYLE_DATA.FontFamily.MAIN)
        self.label.setAlignment(center)
        self.loadIcon = QLabel()
        self.IconImg = QMovie(
            os.path.join(PROJECT_ROOT, STYLE_DATA.Asset.transcribing))
        self.loadIcon.setMovie(self.IconImg)
        self.loadStart()
        self.loadingText = Label(Text.loadingText, STYLE_DATA.FontSize.SMALL, STYLE_DATA.FontFamily.OTHER)
        self.loadingText.setAlignment(center)
        # self.cancelBtn = ColoredBtn(Text.cancelText, STYLE_DATA.Color.GREYDARK, STYLE_DATA.FontSize.BTN)
        self.fileTable = FileTable(
            FileTableHeader.transcribePage, self.signals)
        self.fileTable.resizeCol(FileTableDimension.transcribePage)
    
    def _initstyle(self):
        """ styles loading icon movie """
        self.loadIcon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.loadIcon.setFixedSize(
            QtCore.QSize(STYLE_DATA.Dimension.LARGE_ICON, STYLE_DATA.Dimension.LARGE_ICON))
        self.loadIcon.setScaledContents(True)
    
    def changeColor(self):
        super().changeColor()
    
    def changefont(self, fontmode = None):
        self.label.fontChange(STYLE_DATA.FontSize.HEADER2)
        self.loadingText.fontChange(STYLE_DATA.FontSize.SMALL)
        # self.cancelBtn.fontChange(STYLE_DATA.FontSize.BTN)
   
    def _initLayout(self):
        """ initialize layout """
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.addWidget(self.logoContainer, alignment=
                                      self.logopos)
        self.container = QWidget()
        self.containerLayout = QVBoxLayout()
        self.container.setFixedWidth(STYLE_DATA.Dimension.TABLECONTAINERWIDTH)
        self.container.setLayout(self.containerLayout)
        self.containerLayout.addWidget(self.fileTable)
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addWidget(self.label)
        self.label.setContentsMargins(0, STYLE_DATA.Dimension.MEDIUM_SPACING, 0, 0)
        self.verticalLayout.addWidget(self.loadIcon, 
                                      alignment = center|top)
        self.verticalLayout.addWidget(self.loadingText, alignment = top)
        self.verticalLayout.addWidget(self.container, alignment = top|center)
        self.verticalLayout.addStretch()
        
         
    def _connectSignal(self):
        """ connects signal. change enableCancel to true when backend functionality allows for it. """
        # self.cancelBtn.setDisabled(True)
        self.signals.progressChanged.connect(self.editFileProgess)
        STYLE_DATA.signal.changeFont.connect(self.changefont)
        STYLE_DATA.signal.changeColor.connect(self.changeColor)
        
    def setLoadingText(self, text):
        """ functionality to be able to dynamically change the text under the loading icon 
        
        Args: 
            text (str): the message to display under the loading icon
        """
        self.loadingText = Label(text, STYLE_DATA.FontSize.SMALL, STYLE_DATA.FontFamily.OTHER)

    def cancelGailBot(self):
        """ simulates the cancellation of gailbot- will rely on backend functionality when complete """
        self.signals.cancel.emit()
        
    def editFileProgess(self, progress: Tuple[str, str]):
        """ change the display of file progress on the table

        Args:
            progress (str): the message to show the file progress
        """
        self.logger.info("change file progress status")
        self.fileTable.showOneFileProgress(progress)
    
    
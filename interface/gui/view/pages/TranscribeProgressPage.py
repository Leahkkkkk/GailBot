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
    Color, 
    FontSize, 
    Asset
)
from view.config.Text import TranscribeProgressText as Text
from view.config.Text import FileTableHeader
from view.config.Style import (
    Dimension, 
    FileTableDimension, 
    FontFamily
)
from config_frontend import PROJECT_ROOT
from gbLogger import makeLogger
from view.widgets.Background import addLogo
from view.Signals import FileSignals
from view.widgets import MsgBox
from view.widgets import (
    Label,   
    Button,
    FileTable
)
from view.widgets import Button


from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QMovie
from PyQt6 import QtCore
from PyQt6.QtCore import Qt

top = Qt.AlignmentFlag.AlignTop
center = Qt.AlignmentFlag.AlignHCenter


class TranscribeProgressPage(QWidget):
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
        self.label = Label.Label(
            Text.mainLabelText, FontSize.HEADER2, FontFamily.MAIN)
        self.label.setAlignment(center)
        self.loadIcon = QLabel()
        self.IconImg = QMovie(
            os.path.join(PROJECT_ROOT, Asset.transcribing))
        self.loadIcon.setMovie(self.IconImg)
        self.loadStart()
        self.loadingText = Label.Label(
            Text.loadingText,FontSize.SMALL, FontFamily.OTHER)
        self.loadingText.setAlignment(center)
        self.cancelBtn = Button.ColoredBtn(
            Text.cancelText, 
            Color.GREYDARK, 
            FontSize.BTN)
        self.fileTable = FileTable.FileTable(
            FileTableHeader.transcribePage, self.signals)
        self.fileTable.resizeCol(FileTableDimension.transcribePage)
        
    def _initstyle(self):
        """ styles loading icon movie """
        self.loadIcon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.loadIcon.setFixedSize(
            QtCore.QSize(Dimension.LARGE_ICON, Dimension.LARGE_ICON))
        self.loadIcon.setScaledContents(True)
        
    def _initLayout(self):
        """ initialize layout """
        self.verticalLayout = QVBoxLayout()
        self.container = QWidget()
        self.containerLayout = QVBoxLayout()
        self.container.setFixedWidth(Dimension.TABLECONTAINERWIDTH)
        self.container.setLayout(self.containerLayout)
        self.containerLayout.addWidget(self.fileTable)
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        addLogo(self.verticalLayout)
        self.verticalLayout.addWidget(self.label)
        self.label.setContentsMargins(0, Dimension.MEDIUM_SPACING, 0, 0)
        self.verticalLayout.addWidget(self.loadIcon, 
                                      alignment = center|top)
        self.verticalLayout.addWidget(self.loadingText, alignment = top)
        self.verticalLayout.addWidget(self.container, alignment = top|center)
        self.verticalLayout.addStretch()
        #NOTE: disable cancel function 
        # self.verticalLayout.addWidget(self.cancelBtn, 
        #                               alignment = center)
        self.verticalLayout.addStretch()
        
    def _connectSignal(self):
        """ connects signal. change enableCancel to true when backend functionality allows for it. """
        enableCancel = False
        self.cancelBtn.setDisabled(True)
        self.signals.progressChanged.connect(self.editFileProgess)
    
    def setLoadingText(self, text):
        """ functionality to be able to dynamically change the text under the loading icon 
        
        Args: 
            text (str): the message to display under the loading icon
        """
        self.loadingText = Label.Label(text,
                                      FontSize.SMALL,
                                      FontFamily.OTHER)

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
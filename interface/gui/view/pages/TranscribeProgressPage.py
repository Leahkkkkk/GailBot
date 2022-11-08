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

from util.Style import (
    Color, 
    FontSize, 
    Asset
)
from util.Text import TranscribeProgressText as Text
from util.Text import FileTableHeader
from util.Style import Dimension, FileTableDimension
from util.Logger import makeLogger
from util import Path
from view.style.Background import addLogo
from view.Signals import FileSignals
from view.widgets import MsgBox
from view.widgets import (
    Label,   
    Button,
    FileTable)
from view.widgets import Button
from view.style.styleValues import (
    FontFamily
)

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
            os.path.join(Path.getProjectRoot(), Asset.transcribing))
        self.loadIcon.setMovie(self.IconImg)
        self.loadStart()
       
        self.loadingText = Label.Label(
            Text.loadingText,FontSize.SMALL, FontFamily.OTHER)
        self.loadingText.setAlignment(center)
        self.InProgress = Label.Label(
            Text.inProgressText, FontSize.HEADER3, FontFamily.MAIN)
        self.cancelBtn = Button.ColoredBtn(
            Text.cancelText, 
            Color.LOW_CONTRAST, 
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
        """ intiializes layout """
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        addLogo(self.verticalLayout)
        self.verticalLayout.addWidget(self.label)
        self.label.setContentsMargins(0, Dimension.MEDIUM_SPACING, 0, 0)
        self.verticalLayout.addWidget(self.loadIcon, 
                                      alignment = center|top)
        self.verticalLayout.addWidget(self.loadingText, alignment = top)
        self.verticalLayout.addWidget(self.InProgress, alignment = top)
        self.verticalLayout.addWidget(self.fileTable, 
                                      alignment= center|top)
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(self.cancelBtn, 
                                      alignment = center)
        self.InProgress.setContentsMargins(Dimension.LARGE_SPACING, 0, 0, 0)
        self.verticalLayout.setSpacing(Dimension.MEDIUM_SPACING)
        self.verticalLayout.addStretch()
        
    def _connectSignal(self):
        """ connects signal. change enableCancel to true when backend functionality allows for it. """
        enableCancel = False
        if (enableCancel):
            self.cancelBtn.clicked.connect(self._confirm)
        self.signals.progressChanged.connect(self.editFileProgess)
        
    def _confirm(self):
        """ pulls up message box that prompts user to confirm cancellation """
        self.confirmCancel = MsgBox.ConfirmBox( 
            Text.loggerMsg, self.cancelGailBot)
    
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
        self.logger.info(Text.loggerMsg)
        self.signals.cancel.emit()
        
    def editFileProgess(self, progress: str):
        """ change the display of file progress on the table

        Args:
            progress (str): the message to show the file progress
        """
        self.logger.info("change file progress status")
        self.fileTable.changeAllFileProgress(progress)
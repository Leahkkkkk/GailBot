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

from util.Style import (Color, FontSize)
from util.Text import TranscribeProgressText as Text
from util.Logger import makeLogger
from view.Signals import FileSignals
from view.widgets import MsgBox
from view.widgets import (
    Label,   
    Button,
    FileTable)
from util import Path
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

ProgressHeader = ["Type",
                  "Name",
                  "Progress"]
ProgressDimension = [0.2, 0.55, 0.25]

logger = makeLogger("Frontend")

""" class for transcription in progress page """
class TranscribeProgressPage(QWidget):
    """ initialize class """
    def __init__(
        self, 
        signals: FileSignals, 
        * args, 
        **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.signals = signals
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
            os.path.join(Path.getProjectRoot(), "view/asset/gbloading.gif"))
        self.loadIcon.setMovie(self.IconImg)
        self.loadStart()
       
        self.loadingText = Label.Label(
            Text.loadingText,FontSize.SMALL, FontFamily.OTHER)
        self.loadingText.setAlignment(center)
        self.InProgress = Label.Label(
            Text.inProgressText, FontSize.HEADER3, FontFamily.MAIN)
        self.cancelBtn = Button.ColoredBtn(
            Text.cancelText, 
            Color.GREYLIGHT, 
            FontSize.BTN)
        self.fileTable = FileTable.FileTable(ProgressHeader, self.signals)
        self.fileTable.resizeCol(ProgressDimension)
        
    def _initstyle(self):
        """ styles loading icon movie """
        self.loadIcon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.loadIcon.setFixedSize(QtCore.QSize(80, 80))
        self.loadIcon.setScaledContents(True)
        
    def _initLayout(self):
        """ intiializes layout """
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addWidget(self.label)
        self.label.setContentsMargins(0, 20, 0, 0)
        self.verticalLayout.addWidget(self.loadIcon, 
                                      alignment = center|top)
        self.verticalLayout.addWidget(self.loadingText, alignment = top)
        self.verticalLayout.addWidget(self.InProgress, alignment = top)
        self.verticalLayout.addWidget(self.fileTable, 
                                      alignment= center|top)
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(self.cancelBtn, 
                                      alignment = center)
        self.verticalLayout.setSpacing(30)
        self.InProgress.setContentsMargins(80, 0, 0, 0)
        self.loadIcon.setContentsMargins(0, 0, 0, 0)
        self.fileTable.setMaximumHeight(300)
        
    def _connectSignal(self):
        """ connects signal. change enableCancel to true when backend functionality allows for it. """
        enableCancel = False
        if (enableCancel):
            self.cancelBtn.clicked.connect(self._confirm)
        self.signals.progressChanged.connect(self.editFileProgess)
        
    def _confirm(self):
        self.confirmCancel = MsgBox.ConfirmBox( 
            Text.loggerMsg, self.cancelGailBot)
    
    def setLoadingText(self, text):
        self.loadingText = Label.Label(text,
                                      FontSize.SMALL,
                                      FontFamily.OTHER)

    def cancelGailBot(self):
        logger.info(Text.loggerMsg)
        self.signals.cancel.emit()
        
    def editFileProgess(self, progress: str):
        """ change the display of file progress on the table

        Args:
            progress (str): the message to show the file progress
        """
        logger.info("change file progress status")
        self.fileTable.changeAllFileProgress(progress)
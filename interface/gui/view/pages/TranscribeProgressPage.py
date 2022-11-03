import os

from util.Config import (
    Color, 
    FontSize, 
    TranscribeProgressText
)
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
    Dimension, 
    FontFamily
)
from view.style.Background import initImgBackground

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QMovie
from PyQt6 import QtCore
from PyQt6.QtCore import Qt


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
        self.label = Label.Label(TranscribeProgressText.mainLabelText,
                                 FontSize.HEADER1, 
                                 FontFamily.MAIN)
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.loadIcon = QLabel()
        self.IconImg = QMovie(os.path.join(Path.getProjectRoot(), "view/asset/gbloading.gif"))
        self.loadIcon.setMovie(self.IconImg)
        self.loadStart()
       
        self.loadingText = Label.Label(TranscribeProgressText.loadingText,
                                      FontSize.SMALL,
                                      FontFamily.OTHER)
        self.loadingText.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.InProgress = Label.Label(TranscribeProgressText.inProgressText,
                                        FontSize.HEADER3,
                                        FontFamily.MAIN)
        self.cancelBtn = Button.ColoredBtn(
            TranscribeProgressText.cancelText, 
            Color.ORANGE, 
            FontSize.BTN)
        self.fileTable = FileTable.FileTable(ProgressHeader, self.signals)
        self.fileTable.resizeCol(ProgressDimension)
        
    def _initstyle(self):
        """ styles loading icon movie """
        self.loadIcon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.loadIcon.setFixedSize(QtCore.QSize(80, 80))
        self.loadIcon.setScaledContents(True)
        self.cancelBtn.setMinimumSize(QtCore.QSize(130, 30))
        self.cancelBtn.setMinimumSize(Dimension.BGBUTTON)
        initImgBackground(self, TranscribeProgressText.backgroundImg)
        
    def _initLayout(self):
        """ intiializes layout """
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addWidget(self.label)
        self.label.setContentsMargins(0, 20, 0, 0)
        self.verticalLayout.addWidget(self.loadIcon, 
                                      alignment = Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.verticalLayout.addWidget(self.loadingText, alignment = Qt.AlignmentFlag.AlignTop)
        self.verticalLayout.addWidget(self.InProgress, alignment = Qt.AlignmentFlag.AlignTop)
        self.verticalLayout.addWidget(self.fileTable, 
                                      alignment= Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(self.cancelBtn, 
                                      alignment = Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout.setSpacing(30)
        self.InProgress.setContentsMargins(80, 0, 0, 0)
        self.loadIcon.setContentsMargins(0, 0, 0, 0)
        self.fileTable.setMaximumHeight(300)
        
    def _connectSignal(self):
        """ connects signal """
        self.cancelBtn.clicked.connect(self._confirm)
        
    def _confirm(self):
        self.confirmCancel = MsgBox.ConfirmBox(
            TranscribeProgressText.loggerMsg, self.cancelGailBot)
    
    def setLoadingText(self, text):
        self.loadingText = Label.Label(text,
                                      FontSize.SMALL,
                                      FontFamily.OTHER)

    def cancelGailBot(self):
        logger.info(TranscribeProgressText.loggerMsg)
        self.signals.cancel.emit()
'''
File: ConfirmTranscribePage.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 11:05:38 am
Modified By:  Siara Small  & Vivian Li
-----
Description: implementation of Confirm Transcription Page
'''
from util.Style import (
    Color, 
    FontSize, 
    FileTableDimension,
    FontFamily,
    Dimension)
from util.Text import ConfirmTranscribeText as Text
from util.Text import FileTableHeader 
from util.Logger import makeLogger
from view.Signals import FileSignals
from view.widgets.Background import addLogo
from view.widgets import ( 
    Label, 
    Button, 
    FileTable) 

from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout,
    QHBoxLayout
)
from PyQt6.QtCore import Qt 

center = Qt.AlignmentFlag.AlignHCenter
top = Qt.AlignmentFlag.AlignTop
right = Qt.AlignmentFlag.AlignRight

class ConfirmTranscribePage(QWidget):
    """ Confirm transcription page """
    def __init__(self, signal:FileSignals, *args, **kwargs) -> None:
        """ initializes page """
        super().__init__(*args, **kwargs)
        self.signal = signal
        self.logger = makeLogger("F")
        self._initWidget()
        self._initLayout()
        self._connectSignal()
    
    def _connectSignal(self):
        """ connects signals upon button clicks """
        self.confirmBtn.clicked.connect(self._sendTranscribeSignal)
        self.logger.info("")

    def _initWidget(self):
        """ initializes widgets """
        self.logger.info("")
        self.label = Label.Label(Text.confirmLabel, 
                                 FontSize.HEADER2, 
                                 FontFamily.MAIN)
        self.label.setAlignment(center)
        
        self.fileTable = FileTable.FileTable(
            FileTableHeader.confirmPage,
            self.signal,
            tableWidgetsSet={FileTable.TableWidget.PROFILE_DETAIL})
        
        self.fileTable.resizeCol(FileTableDimension.confirmPage)
        self.bottomButton = QWidget()
        self.confirmBtn = Button.ColoredBtn(Text.confirm, Color.SECONDARY_BUTTON)
        self.cancelBtn = Button.ColoredBtn(Text.cancel, Color.CANCEL_QUIT)
        
    def _initLayout(self):
        """ initializes layout"""
        self.logger.info("")
        self.verticalLayout = QVBoxLayout()
        self.horizontalLayout = QHBoxLayout()
        self.bottomButton.setLayout(self.horizontalLayout)
        self.setLayout(self.verticalLayout)
        """ adds widgets to layout """
        addLogo(self.verticalLayout)
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(
            self.fileTable, alignment = center|top)
        self.horizontalLayout.addWidget(
            self.confirmBtn, alignment = right)
        self.horizontalLayout.addWidget(
            self.cancelBtn, alignment = center)
        self.bottomButton.setContentsMargins(0,0,0,0)
        self.verticalLayout.addWidget(self.bottomButton, alignment=center)
        self.horizontalLayout.setSpacing(Dimension.LARGE_SPACING)
        
    def _sendTranscribeSignal(self):
        """sends a signal with a set of file keys that will be transcribed """
        self.logger.info(self.fileTable.transferList)
        self.signal.transcribe.emit(self.fileTable.transferList)
        self.fileTable.transferState()


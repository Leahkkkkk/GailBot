'''
File: ConfirmTranscribePage.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 11:05:38 am
Modified By:  Siara Small  & Vivian Li
-----
'''
from util.Config import (
    Color, 
    FontSize, 
    FileTableHeader, 
    FileTableDimension, 
    Asset)
from util.Config import ConfirmTranscribeText as Text

from view.Signals import FileSignals
from view.style.styleValues import FontFamily
from view.style.Background import initImgBackground
from view.widgets import ( Label, 
                           Button, 
                           FileTable) 
from util.Logger import makeLogger

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
        super().__init__(*args, **kwargs)
        self.signal = signal
        self.logger = makeLogger("Frontend")
        self._initWidget()
        self._initLayout()
        self._initStyle()
        self._connectSignal()
    
    def _connectSignal(self):
        self.confirmBtn.clicked.connect(self._sendTranscribeSignal)

    def _initWidget(self):
        """ initlialize widget """
        self.label = Label.Label(Text.confirmLabel, 
                                 FontSize.HEADER2, 
                                 FontFamily.MAIN)
        self.label.setAlignment(center)
        
        self.fileTable = FileTable.FileTable(
            FileTableHeader.confirmPage,
            self.signal,
            rowWidgets={"details"})
        
        self.fileTable.resizeCol(FileTableDimension.confirmPage)
        self.bottomButton = QWidget()
        self.confirmBtn = Button.ColoredBtn(Text.confirm, Color.GREEN)
        self.cancelBtn = Button.ColoredBtn(Text.cancel, Color.ORANGE)
        
    def _initLayout(self):
        """ initialize layout"""
        self.verticalLayout = QVBoxLayout()
        self.horizontalLayout = QHBoxLayout()
        self.bottomButton.setLayout(self.horizontalLayout)
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(
            self.fileTable, alignment = center|top)
        self.horizontalLayout.addWidget(
            self.confirmBtn, alignment = right)
        self.horizontalLayout.addWidget(
            self.cancelBtn, alignment = center)
        self.bottomButton.setContentsMargins(0,0,0,0)
        self.verticalLayout.addWidget(self.bottomButton, alignment=center)
    
    def _initStyle(self):
        initImgBackground(self,Asset.subPageBackgorund)
        
    def _sendTranscribeSignal(self):
        """send a signal with a set of file keys that will be transcribed """
        self.logger.info("here")
        self.logger.info(self.fileTable.transferList)
        self.signal.transcribe.emit(self.fileTable.transferList)
        self.fileTable.transferState()


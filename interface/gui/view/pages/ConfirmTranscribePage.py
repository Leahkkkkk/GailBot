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
from view.config.Style import (
    FileTableDimension,
    FontFamily,
    STYLE_DATA)

from view.config.Text import ConfirmTranscribeText as Text
from view.config.Text import FileTableHeader 
from gbLogger import makeLogger
from view.Signals import FileSignals, GlobalStyleSignal
from view.widgets.Background import addLogo
from view.widgets import ( 
    Label, 
    ColoredBtn,
    FileTable,
    TableWidget) 

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
        GlobalStyleSignal.changeColor.connect(self.colorChange) 
        GlobalStyleSignal.changeFont.connect(self.fontSizeChange)
         
    def _initWidget(self):
        """ initializes widgets """
        self.logger.info("")
        self.label = Label(Text.confirmLabel, 
                                 STYLE_DATA.FontSize.HEADER2, 
                                 FontFamily.MAIN)
        self.label.setAlignment(center)
        
        self.fileTable = FileTable(
            FileTableHeader.confirmPage,
            self.signal,
            tableWidgetsSet={TableWidget.PROFILE_DETAIL})
        
        self.fileTable.resizeCol(FileTableDimension.confirmPage)
        self.bottomButton = QWidget()
        self.confirmBtn = ColoredBtn(Text.confirm, STYLE_DATA.Color.SECONDARY_BUTTON)
        self.cancelBtn = ColoredBtn(Text.cancel, STYLE_DATA.Color.CANCEL_QUIT)
    
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
        self.horizontalLayout.setSpacing(STYLE_DATA.Dimension.LARGE_SPACING)
        
    def _sendTranscribeSignal(self):
        """sends a signal with a set of file keys that will be transcribed """
        self.logger.info(self.fileTable.transferList)
        self.fileTable.transferAll()
        self.signal.transcribe.emit(list(self.fileTable.transferList))
        self.fileTable.transferState()
    
    

    def colorChange(self, colormode = None ):
        """ called when color is changed """
        self.confirmBtn.colorChange(STYLE_DATA.Color.SECONDARY_BUTTON)
        self.cancelBtn.colorChange(STYLE_DATA.Color.CANCEL_QUIT)

    ## controlling font
    def fontSizeChange(self, fontmode = None ):
        """ called when font size is changed """
        self.label.fontChange(STYLE_DATA.FontSize.HEADER2)
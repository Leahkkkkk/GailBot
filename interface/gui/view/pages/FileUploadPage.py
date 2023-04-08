'''
File: FileUploadPage.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 11:08:37 am
Modified By:  Siara Small  & Vivian Li
-----
Description: implementation of file upload page 
'''

from typing import List

from view.config.Style import STYLE_DATA, FileTableDimension
from view.config.Text import FileTableHeader
from view.config.Text import FileUploadPageText as Text 
from view.config.Style import buttonStyle
from view.Signals import GlobalStyleSignal
from gbLogger import makeLogger
from view.Signals import FileSignals
from view.widgets import (
    Label, 
    ColoredBtn, 
    IconBtn, 
    FileTable, 
    TableWidget, 
    ConfirmBox, 
    addLogo)

from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout,
    QHBoxLayout,
    QVBoxLayout,
)
from PyQt6.QtCore import Qt, QSize

center = Qt.AlignmentFlag.AlignHCenter
left   = Qt.AlignmentFlag.AlignLeft
right  = Qt.AlignmentFlag.AlignRight
top    =  Qt.AlignmentFlag.AlignTop

class FileUploadPage(QWidget):
    """ implement the file upload table
    
    Constructor Args:
    1. profileNames: a list of profiles that is currently available in the 
                     profile database, so that user can select a different 
                     profile of the file through the file table
    2. signals:      a FileSignals object that support the communication 
                     to the file database
    """
    def __init__(
        self, 
        signal: FileSignals, 
        *args, 
        **kwargs) -> None:
        """ initializes file upload page """
        super().__init__(*args, **kwargs)
        self.signal = signal
        self.logger = makeLogger("F")
        self._initWidget()
        self._initLayout()
        self._initStyle()
        self._connectSignal()
    
    def initAvailableProfiles(self, profiles: List[str]):
        """ initialize a list of available profiles to file table """
        self.fileTable.initProfiles(profiles)
    
    def _connectSignal(self):
        """ connects signals to different functions upon button clicks """
        self.logger.info("")
        self.uploadFileBtn.clicked.connect(self.fileTable.uploadFile)
        self.transcribeBtn.clicked.connect(self.fileTable.transferState) 
        self.removeAll.clicked.connect(self._confirmRemove)
        self.fileTable.viewSignal.nonZeroFile.connect(self._allowTranscribe)
        self.fileTable.viewSignal.ZeroFile.connect(self._disallowTranscribe)
        self._disallowTranscribe()
        GlobalStyleSignal.changeColor.connect(self.colorChange)
        
    def _initWidget(self):
        """ initializes widgets """
        self.logger.info("")
        self.label = Label(Text.header, STYLE_DATA.FontSize.HEADER2, STYLE_DATA.FontFamily.MAIN)
        self.gotoMainBtn = IconBtn(
            STYLE_DATA.Asset.arrowImg, Text.returnMainText) 
        self.uploadFileBtn = ColoredBtn(
            Text.uploadBtnText, STYLE_DATA.Color.PRIMARY_BUTTON, STYLE_DATA.FontSize.BTN)
        self.transcribeBtn = ColoredBtn(
            Text.transcribeBtnText, STYLE_DATA.Color.SECONDARY_BUTTON, STYLE_DATA.FontSize.BTN)
        self.settingBtn = ColoredBtn(
            Text.settingBtnText, STYLE_DATA.Color.PRIMARY_BUTTON, STYLE_DATA.FontSize.SETTINGICON)
        self.settingBtn.setFixedSize(
            QSize(STYLE_DATA.Dimension.ICONBTN, STYLE_DATA.Dimension.ICONBTN))
        self.removeAll = ColoredBtn(
            Text.removeBtnText, STYLE_DATA.Color.PRIMARY_BUTTON, STYLE_DATA.FontSize.BTN)
        # self.recordBtn = ColoredBtn(
        #     Text.recordBtnText, Color.PRIMARY_BUTTON, FontSize.BTN)
        
        self.fileTable = FileTable(
            FileTableHeader.fileUploadPage, 
            self.signal,
            {TableWidget.CHECK, 
             TableWidget.PROFILE_DETAIL, 
             TableWidget.CHANGE_PROFILE, 
             TableWidget.REMOVE},
            showSelectHighlight=True)
        self.fileTable.resizeCol(FileTableDimension.fileUploadPage)
        
    def _initLayout(self):
        """ initializes layout """
        self.logger.info("")
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        """ adds widget to layout """
        addLogo(self.verticalLayout)
        self.verticalLayout.addWidget(self.gotoMainBtn, alignment = left)
        self.verticalLayout.addWidget(self.label, alignment = center)
        
        self.middleLayout = QVBoxLayout()
        self.fileTableContainer = QWidget(self)
        self.fileTableContainer.setFixedWidth(STYLE_DATA.Dimension.TABLECONTAINERWIDTH)
        self.fileTableContainer.setLayout(self.middleLayout)
        
        self.middleLayout.addWidget(self.settingBtn, alignment = right|top)
        self.middleLayout.addWidget(self.fileTable,  alignment = center)
        self.middleLayout.addStretch()
        
        self.addFileBtnContainer = QWidget(self)
        self.containerLayout = QHBoxLayout()
        self.containerLayout.setSpacing(STYLE_DATA.Dimension.LARGE_SPACING)
        self.addFileBtnContainer.setLayout(self.containerLayout)
        
        self.containerLayout.addWidget(self.uploadFileBtn, alignment = center)
        self.containerLayout.addWidget(self.removeAll, alignment = center)
        self.verticalLayout.addWidget (self.fileTableContainer, alignment = center)
        self.verticalLayout.addWidget (self.addFileBtnContainer, alignment = center)
        
        self.verticalLayout.addWidget(self.transcribeBtn, alignment = center)
        # self.containerLayout.addWidget(self.recordBtn,
        #                                alignment = center)
        
    def _initStyle(self):
        """ initializes the style """
        self.logger.info("")
        self.gotoMainBtn.setFixedSize(
            QSize(STYLE_DATA.Dimension.LBTNWIDTH, STYLE_DATA.Dimension.BTNHEIGHT))
        self.gotoMainBtn.setStyleSheet(STYLE_DATA.StyleSheet.goToMain)

    def colorChange(self, colormode):
        self.gotoMainBtn.setStyleSheet(STYLE_DATA.StyleSheet.goToMain)
        self.settingBtn.colorChange(STYLE_DATA.Color.PRIMARY_BUTTON)
        self.removeAll.colorChange(STYLE_DATA.Color.PRIMARY_BUTTON)
    
    def _allowTranscribe(self):
        """ activates the transcribe button """
        self.logger.info("")
        self.transcribeBtn.setEnabled(True)
        self.transcribeBtn.setStyleSheet(buttonStyle.ButtonActive)
        
    def _disallowTranscribe(self):
        """ deactivates the transcribe button """
        self.logger.info("")
        self.transcribeBtn.setDisabled(True)
        self.transcribeBtn.setStyleSheet(buttonStyle.ButtonInactive)
        
    def _confirmRemove(self):
        """ open pop up message to confirm removal of all files """
        self.logger.info("")
        ConfirmBox(Text.removeWarnText, self.fileTable.removeAll)
    
    
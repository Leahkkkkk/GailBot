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

from view.config.Style import (
    FileTableDimension, 
    Asset, 
    StyleSheet,
    Color, 
    FontSize,
    Dimension,
    FontFamily
)
from view.config.Text import FileTableHeader
from view.config.Text import FileUploadPageText as Text 
from view.config.Style import FontSize as FS
from view.config.Style import buttonStyle
from gbLogger import makeLogger
from view.Signals import FileSignals
from view.widgets import Label, Button
from view.widgets.FileTable import FileTable, TableWidget
from view.widgets.Background import addLogo
from view.widgets import MsgBox

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
        profileNames: List[str],
        signal: FileSignals, 
        *args, 
        **kwargs) -> None:
        """ initializes file upload page """
        super().__init__(*args, **kwargs)
        self.signal = signal
        self.profileNames = profileNames
        self.logger = makeLogger("F")
        self._initWidget()
        self._initLayout()
        self._initStyle()
        self._connectSignal()
        
    def _connectSignal(self):
        """ connects signals to different functions upon button clicks """
        self.logger.info("")
        self.uploadFileBtn.clicked.connect(self.fileTable.uploadFile)
        self.transcribeBtn.clicked.connect(self.fileTable.transferState) 
        self.removeAll.clicked.connect(self._confirmRemove)
        self.fileTable.viewSignal.nonZeroFile.connect(self._allowTranscribe)
        self.fileTable.viewSignal.ZeroFile.connect(self._disallowTranscribe)
        self._disallowTranscribe()
        
    def _initWidget(self):
        """ initializes widgets """
        self.logger.info("")
        self.label = Label.Label(Text.header, FS.HEADER2, FontFamily.MAIN)
        self.gotoMainBtn = Button.iconBtn(
            Asset.arrowImg, Text.returnMainText) 
        # self.recordBtn = Button.ColoredBtn(
        #     Text.recordBtnText, Color.PRIMARY_BUTTON, FontSize.BTN)
        self.uploadFileBtn = Button.ColoredBtn(
            Text.uploadBtnText, Color.PRIMARY_BUTTON, FontSize.BTN)
        self.transcribeBtn = Button.ColoredBtn(
            Text.transcribeBtnText, Color.SECONDARY_BUTTON, FontSize.BTN)
        self.settingBtn = Button.ColoredBtn(
            Text.settingBtnText, Color.PRIMARY_BUTTON, FS.SETTINGICON)
        self.settingBtn.setFixedSize(
            QSize(Dimension.ICONBTN,Dimension.ICONBTN))
        self.removeAll = Button.ColoredBtn(
            Text.removeBtnText, Color.PRIMARY_BUTTON, FontSize.BTN)
        
        self.fileTable = FileTable(
            FileTableHeader.fileUploadPage, 
            self.signal,
            self.profileNames,
            {TableWidget.CHECK, 
             TableWidget.PROFILE_DETAIL, 
             TableWidget.CHANGE_PROFILE, 
             TableWidget.REMOVE},
            transferListColor=Color.HIGHLIGHT)
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
        self.fileTableContainer.setFixedWidth(Dimension.TABLECONTAINERWIDTH)
        self.fileTableContainer.setLayout(self.middleLayout)
        
        self.middleLayout.addWidget(self.settingBtn, alignment = right|top)
        self.middleLayout.addWidget(self.fileTable,  alignment = center)
        self.middleLayout.addStretch()
        
        self.addFileBtnContainer = QWidget(self)
        self.containerLayout = QHBoxLayout()
        self.containerLayout.setSpacing(Dimension.LARGE_SPACING)
        self.addFileBtnContainer.setLayout(self.containerLayout)
        # self.containerLayout.addWidget(self.recordBtn,
        #                                alignment = center)
        
        self.containerLayout.addWidget(self.uploadFileBtn,
                                      alignment = center)
        
        self.containerLayout.addWidget(self.removeAll,
                                        alignment = center)
        self.verticalLayout.addWidget(self.fileTableContainer,
                                      alignment = center)
        self.verticalLayout.addWidget(self.addFileBtnContainer,
                                       alignment = center)
        
        self.verticalLayout.addWidget(self.transcribeBtn,
                                      alignment = center)
        
    def _initStyle(self):
        """ initializes the style """
        self.logger.info("")
        self.gotoMainBtn.setFixedSize(
            QSize(Dimension.LBTNWIDTH,Dimension.BTNHEIGHT))
        self.gotoMainBtn.setStyleSheet(StyleSheet.goToMain)

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
        MsgBox.ConfirmBox(Text.removeWarnText, self.fileTable.removeAll)
    
    
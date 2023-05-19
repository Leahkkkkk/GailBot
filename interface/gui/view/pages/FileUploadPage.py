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
from view.config.InstructionText import INSTRUCTION
from typing import List, Tuple, Dict
from view.config.Style import STYLE_DATA, FileTableDimension
from view.config.Text import FILE_TABLE_HEADER
from view.config.Text import FILEUPLOAD_PAGE as Text 
from view.pages.BasicPage import BasicPage
from gbLogger import makeLogger
from view.signal.signalObject import FileSignal, GBTranscribeSignal
from view.components.FileTable import TableWidget, SourceTable, DATA_FIELD
from view.widgets import (
    Label, 
    ColoredBtn, 
    IconBtn, 
    ConfirmBox) 

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

class FileUploadPage(BasicPage):
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
        *args, 
        **kwargs) -> None:
        """ initializes file upload page """
        self.pageInstruction = INSTRUCTION.FILE_UPLOAD_INS
        super().__init__(*args, **kwargs)
        self.signal = FileSignal
        self.logger = makeLogger()
        self._initWidget()
        self._initLayout()
        self._initStyle()
        self._connectSignal()
    
    def _connectSignal(self):
        """ connects signals to different functions upon button clicks """
        self.logger.info("")
        self.uploadFileBtn.clicked.connect(self.fileTable.uploadFile)
        self.transcribeBtn.clicked.connect(self.sendToConfirm) 
        self.removeAll.clicked.connect(self._confirmRemove)
        self.fileTable.viewSignal.nonZeroFile.connect(self._allowTranscribe)
        self.fileTable.viewSignal.ZeroFile.connect(self._disallowTranscribe)
        self._disallowTranscribe()
        STYLE_DATA.signal.changeColor.connect(self.changeColor)
        STYLE_DATA.signal.changeFont.connect(self.changeFont)
        GBTranscribeSignal.sendToTranscribe.connect(self.removeFromTable)

    def _initWidget(self):
        """ initializes widgets """
        self.logger.info("")
        self.label = Label(Text.HEADER, STYLE_DATA.FontSize.HEADER2, STYLE_DATA.FontFamily.MAIN)
        self.gotoMainBtn = IconBtn(
            STYLE_DATA.Asset.arrowImg, Text.RETURN_MAIN) 
        self.uploadFileBtn = ColoredBtn(
            Text.UPLOAD, STYLE_DATA.Color.PRIMARY_BUTTON, STYLE_DATA.FontSize.BTN)
        self.transcribeBtn = ColoredBtn(
            Text.TRANSCRIBE, STYLE_DATA.Color.SECONDARY_BUTTON, STYLE_DATA.FontSize.BTN)
        self.settingBtn = ColoredBtn(
            Text.SETTING_BTN, STYLE_DATA.Color.PRIMARY_BUTTON, STYLE_DATA.FontSize.SETTINGICON)
        self.settingBtn.setFixedSize(
            QSize(STYLE_DATA.Dimension.ICONBTN, STYLE_DATA.Dimension.ICONBTN))
        self.removeAll = ColoredBtn(
            Text.REMOVE_ALL, STYLE_DATA.Color.PRIMARY_BUTTON, STYLE_DATA.FontSize.BTN)
        
        self.fileTable = SourceTable(
           headers=FILE_TABLE_HEADER.FILE_UPLOAD, 
           signal =self.signal,
           dataKeyToCol={DATA_FIELD.TYPE: 1,
                         DATA_FIELD.NAME: 2, 
                         DATA_FIELD.PROFILE: 3,
                         DATA_FIELD.STATUS: 4, 
                         DATA_FIELD.DATE: 5},
            appliedCellWidget={
             TableWidget.CHECK, 
             TableWidget.PROFILE_DETAIL, 
             TableWidget.CHANGE_PROFILE, 
             TableWidget.REMOVE})
        self.fileTable.resizeCol(FileTableDimension.fileUploadPage)
    
    def _initLayout(self):
        """ initializes layout """
        self.logger.info("")
        self.verticalLayout = QVBoxLayout()
        
        self.setLayout(self.verticalLayout)
        """ adds widget to layout """
        self.verticalLayout.addWidget(self.logoContainer, alignment=self.logopos)
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
        self.addFileBtnContainer.setLayout(self.containerLayout)
        
        self.containerLayout.addWidget(self.uploadFileBtn, alignment = center)
        self.containerLayout.addWidget(self.removeAll, alignment = center)
        self.verticalLayout.addWidget (self.fileTableContainer, alignment = center)
        self.verticalLayout.addWidget (self.addFileBtnContainer, alignment = center)
        self.verticalLayout.addWidget(self.transcribeBtn, alignment = center)
        self.verticalLayout.addWidget(self.instructionBtn, alignment = self.infopos)
        self.verticalLayout.setSpacing(3) 
        
    def _initStyle(self):
        """ initializes the style """
        self.logger.info("")
        self.gotoMainBtn.setFixedSize(
            QSize(STYLE_DATA.Dimension.LBTNWIDTH, STYLE_DATA.Dimension.BTNHEIGHT))
        self.gotoMainBtn.setStyleSheet(STYLE_DATA.StyleSheet.goToMain)

    def changeColor(self):
        """ change the page color in response to the color change signal"""
        super().changeColor()
        self.gotoMainBtn.setStyleSheet(STYLE_DATA.StyleSheet.goToMain)
        self.settingBtn.changeColor(STYLE_DATA.Color.PRIMARY_BUTTON)
        self.uploadFileBtn.changeColor(STYLE_DATA.Color.PRIMARY_BUTTON)
        self.removeAll.changeColor(STYLE_DATA.Color.PRIMARY_BUTTON)
         
    def changeFont(self):
        """ change the page font size in response to the font change signal """
        self.label.changeFont(STYLE_DATA.FontSize.HEADER2)
        self.transcribeBtn.changeFont(STYLE_DATA.FontSize.BTN)
        self.uploadFileBtn.changeFont(STYLE_DATA.FontSize.BTN)
        self.removeAll.changeFont(STYLE_DATA.FontSize.BTN)
    
    def sendToConfirm(self):
        """ send the list of selected file to be transcribed to the confirm page """
        GBTranscribeSignal.sendToConfirm.emit(self.fileTable.getSelectedFile())
        
    
    def removeFromTable(self, files: List[Tuple[str, Dict]]):
        """ remove file from file table """
        for file in files:
            name, data = file 
            self.fileTable.deleteSucceed(name)
    
    def _allowTranscribe(self):
        """ activates the transcribe button """
        self.logger.info("")
        self.transcribeBtn.setEnabled(True)
        self.transcribeBtn.setStyleSheet(STYLE_DATA.buttonStyle.ButtonActive)
        
    def _disallowTranscribe(self):
        """ deactivates the transcribe button """
        self.logger.info("")
        self.transcribeBtn.setDisabled(True)
        self.transcribeBtn.setStyleSheet(STYLE_DATA.buttonStyle.ButtonInactive)
        
    def _confirmRemove(self):
        """ open pop up message to confirm removal of all files """
        self.logger.info("")
        ConfirmBox(Text.REMOVE_CONFIRM, self.fileTable.deleteAll)
    

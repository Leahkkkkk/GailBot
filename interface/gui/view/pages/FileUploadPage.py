'''
File: FileUploadPage.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 11:08:37 am
Modified By:  Siara Small  & Vivian Li
-----
'''

""" 
TODO: add file summary widget 
TODO: add search bar 
""" 

from typing import List

from view.Signals import FileSignals
from view.widgets import Label, Button, FileTable
from view.style.widgetStyleSheet import buttonStyle
from view.style.Background import addLogo
from view.widgets import MsgBox
from util.Style import (
    FileTableDimension, 
    Asset, 
    StyleSheet,
    Color, 
    FontSize,
    Dimension
)
from util.Text import FileTableHeader
from util.Text import FileUploadPageText as Text 
from util.Style import FontSize as FS
from view.style.styleValues import FontFamily


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
    def __init__(
        self, 
        profilekeys: List[str],
        signal: FileSignals, 
        *args, 
        **kwargs) -> None:
        """ file upload page """
        super().__init__(*args, **kwargs)
        self.signal = signal
        self.profilekeys = profilekeys
        self._initWidget()
        self._initLayout()
        self._initStyle()
        self._connectSignal()
        
    def _connectSignal(self):
        """ connect signals to different functions """
        # uploading file
        self.uploadFileBtn.clicked.connect(self.fileTable.uploadFile)
        # load confirm page table with selected file 
        self.transcribeBtn.clicked.connect(self.fileTable.transferState) 
 
        
        # remove all file 
        self.removeAll.clicked.connect(self._confirmRemove)
        # change transcribe button color
        self.fileTable.viewSignal.nonZeroFile.connect(self._allowTranscribe)
        self.fileTable.viewSignal.ZeroFile.connect(self._disallowTranscribe)
        self._disallowTranscribe()
        
    def _initWidget(self):
        """ initialzie widget """
        self.label = Label.Label(Text.header, FS.HEADER2, FontFamily.MAIN)
        self.gotoMainBtn = Button.iconBtn(
            Asset.arrowImg, Text.returnMainText) 
        self.recordBtn = Button.ColoredBtn(
            Text.recordBtnText, Color.BLUEMEDIUM, FontSize.BTN)
        self.uploadFileBtn = Button.ColoredBtn(
            Text.uploadBtnText, Color.BLUEMEDIUM, FontSize.BTN)
        self.transcribeBtn = Button.ColoredBtn(
            Text.transcribeBtnText, Color.GREYLIGHT, FontSize.BTN)
        self.settingBtn = Button.ColoredBtn(
            Text.settingBtnText, Color.BLUEMEDIUM, FS.SETTINGICON)
        self.settingBtn.setFixedSize(
            QSize(Dimension.ICONBTN,Dimension.ICONBTN))
        self.removeAll = Button.ColoredBtn(
            Text.removeBtnText, Color.BLUEMEDIUM, FontSize.BTN)
        self.fileTable = FileTable.FileTable(
            FileTableHeader.fileUploadPage, 
            self.signal,
            self.profilekeys,
            {"check", "delete", "details", "edit"})
        self.fileTable.resizeCol(FileTableDimension.fileUploadPage)
        
        
    def _initLayout(self):
        """ initialize layout """
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
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
        self.addFileBtnContainer.setLayout(self.containerLayout)
        self.containerLayout.addWidget(self.recordBtn,
                                       alignment = center)
        
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
        """ initialize the style """
        self.gotoMainBtn.setFixedSize(
            QSize(Dimension.LBTNWIDTH,Dimension.BTNHEIGHT))
        self.gotoMainBtn.setStyleSheet(StyleSheet.goToMain)

    def _allowTranscribe(self):
        """ activate the transcribe button """
        self.transcribeBtn.setEnabled(True)
        self.transcribeBtn.setStyleSheet(buttonStyle.ButtonActive)
        
    def _disallowTranscribe(self):
        """ deactivate the transcribe button """
        self.transcribeBtn.setDisabled(True)
        self.transcribeBtn.setStyleSheet(buttonStyle.ButtonInactive)
        
    def _confirmRemove(self):
        """ open pop up message to confirm removal of all files """
        confirmPopUp = MsgBox.ConfirmBox(Text.removeWarnText, 
                                         self.fileTable.removeAll)
        
    
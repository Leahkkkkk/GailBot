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
TODO: add "NO files added" text

"""
import tomli 

from view.Signals import FileSignals
from typing import List, Dict
from view.widgets import Label, Button, FileTable
from view.style.styleValues import Color
from view.style.widgetStyleSheet import buttonStyle
from view.widgets import MsgBox



from view.style.styleValues import (
    FontFamily, 
    FontSize, 
    Color, 
    Dimension,
)

from view.style.Background import initImgBackground
from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout,
    QHBoxLayout,
    QVBoxLayout,
    QSpacerItem,
)

from PyQt6.QtCore import Qt, QSize, pyqtSignal,QObject

    
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
        self._initConfig()
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
        # delete all file 
        self.deleteAll.clicked.connect(self._confirmDelete)
        # change transcribe button color
        self.fileTable.signals.nonZeroFile.connect(self._allowTranscribe)
        self.fileTable.signals.ZeroFile.connect(self._disallowTranscribe)
        self._disallowTranscribe()
        
    def _initWidget(self):
        """ initialzie widget """
        self.label = Label.Label("Files to Transcribe", self.config["fontSizes"]["HEADER2"], FontFamily.MAIN)
        self.gotoMainBtn = Button.iconBtn("arrow.png"," Return to Main Menu") 
        self.recordBtn = Button.ColoredBtn("Record live",  self.config["colors"]["BLUEMEDIUM"], self.config["fontSizes"]["BTN"])
        self.uploadFileBtn = Button.ColoredBtn("Add From Device", self.config["colors"]["BLUEMEDIUM"], self.config["fontSizes"]["BTN"])
        self.transcribeBtn = Button.ColoredBtn("Transcribe", self.config["colors"]["GREYMEDIUM1"], self.config["fontSizes"]["BTN"])
       
        self.recordBtn.setFixedSize(Dimension.RBUTTON)
        self.uploadFileBtn.setFixedSize(Dimension.RBUTTON)
        self.transcribeBtn.setFixedSize(Dimension.BGBUTTON)
        self.settingProfile = Button.ColoredBtn("⚙", self.config["colors"]["BLUEMEDIUM"], "35px")
        self.settingProfile.setFixedSize(QSize(40,40))
        self.deleteAll = Button.ColoredBtn("Delete all",
                                            self.config["colors"]["BLUEMEDIUM"],
                                            self.config["fontSizes"]["BTN"])
        self.deleteAll.setContentsMargins(200,0,0,0)
        self.fileTable = FileTable.FileTable(
            FileTable.MainTableHeader, 
            self.signal,
            settings=self.profilekeys)
        self.fileTable.resizeCol(FileTable.MainTableDimension)
        
        
    def _initLayout(self):
        """ initialize layout """
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addWidget(self.gotoMainBtn,
                                      alignment = Qt.AlignmentFlag.AlignLeft)
        self.verticalLayout.addWidget(self.label, 
                                      alignment = Qt.AlignmentFlag.AlignHCenter)
        
        self.verticalLayout.addWidget(self.settingProfile,
                                      alignment=Qt.AlignmentFlag.AlignRight|
                                      Qt.AlignmentFlag.AlignTop)
        self.verticalLayout.addWidget(self.deleteAll,
                                      alignment = Qt.AlignmentFlag.AlignLeft)
        self.verticalLayout.addWidget(self.fileTable, 4,
                                      alignment = Qt.AlignmentFlag.AlignHCenter)
        self.spacer = QSpacerItem(500,70)
        self.verticalLayout.addItem(self.spacer)
        
        self.addFileBtnContainer = QWidget(self)
        self.containerLayout = QHBoxLayout()
        self.addFileBtnContainer.setLayout(self.containerLayout)
        self.containerLayout.setSpacing(60)
        
        self.containerLayout.addWidget(self.uploadFileBtn,
                                      alignment = Qt.AlignmentFlag.AlignHCenter)
        
        self.containerLayout.addWidget(self.recordBtn,
                                       alignment = Qt.AlignmentFlag.AlignHCenter)
        
        self.verticalLayout.addWidget(self.addFileBtnContainer,
                                       alignment = Qt.AlignmentFlag.AlignHCenter)
        
        self.verticalLayout.addWidget(self.transcribeBtn,
                                      alignment = Qt.AlignmentFlag.AlignHCenter)
        

    def _initStyle(self):
        """ initialize the style """
        initImgBackground(self,"backgroundConfirmPage.png")
        self.gotoMainBtn.setFixedSize(QSize(200,40))
        self.gotoMainBtn.setStyleSheet(f"border:none; color:{Color.BLUEMEDIUM}")
        self.deleteAll.setFixedSize(130,30)
    
    def _allowTranscribe(self):
        self.transcribeBtn.setEnabled(True)
        """ TODO : add stylesheet data to separate file """
        self.transcribeBtn.setStyleSheet(buttonStyle.ButtonActive)
        
    
    def _disallowTranscribe(self):
        self.transcribeBtn.setDisabled(True)
        self.transcribeBtn.setStyleSheet(buttonStyle.ButtonInactive)
        
    def _confirmDelete(self):
        confirmPopUp = MsgBox.ConfirmBox("Delete all files?", 
                                         self.fileTable.deleteAll)
        
    def _initConfig(self):
        with open("controller/interface.toml", mode="rb") as fp:
            self.config = tomli.load(fp)
    
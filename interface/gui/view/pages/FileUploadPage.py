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
from typing import List, Dict

from view.widgets import Label, Button, FileTable, TabPages
from view.components import MsgBox
from view.style.styleValues import (
    FontFamily, 
    FontSize, 
    Color, 
    Dimension,
)

from view.style.Background import initImgBackground

from PyQt6.QtWidgets import (
    QWidget, 
    QPushButton, 
    QVBoxLayout,
    QHBoxLayout,
    QTableView, 
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QDialog
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal,QObject

class Signals(QObject):
    """ contain signals in order for Qrunnable object to communicate
        with controller
    """
    gotoSetting = pyqtSignal()
    
class FileUploadPage(QWidget):
    def __init__(self, 
                 nextStep:callable, 
                 fileDate: Dict[str, dict], 
                 settingData: List[str],
                 *args, **kwargs) -> None:
        """ file upload page """
        super().__init__(*args, **kwargs)
        self.nextStep = nextStep
        self.fileDate = fileDate
        self.settingData = settingData
        self._initWidget()
        self._initLayout()
        self._initStyle()
        self.signals = Signals()
        
    def _initWidget(self):
        """ initialzie widget """
        self.label = Label.Label("File to Transcribe", 
                                 FontSize.HEADER2, 
                                 FontFamily.MAIN)
        self.gotoMainBtn = Button.iconBtn("arrow.png"," Return to Main Menu")
        
        self.recordBtn = Button.ColoredBtn("Record live", 
                                           Color.BLUEMEDIUM,
                                           FontSize.BTN)
        
        self.uploadFileBtn = Button.ColoredBtn("Add From Device", 
                                               Color.BLUEMEDIUM, 
                                               FontSize.BTN)
                               

        self.transcribeBtn = Button.ColoredBtn("Transcribe", 
                                               Color.GREYMEDIUM1, 
                                               FontSize.BTN)
       
        self.recordBtn.setFixedSize(Dimension.RBUTTON)
        self.uploadFileBtn.setFixedSize(Dimension.RBUTTON)
        self.transcribeBtn.setFixedSize(Dimension.BGBUTTON)
        
        self.settingProfile = Button.ColoredBtn("⚙", Color.BLUEMEDIUM,"35px")
        self.settingProfile.setFixedSize(QSize(40,40))
      
      
        self.fileTable = FileTable.FileTable(FileTable.MainTableHeader, 
                                             self.fileDate, 
                                             {"delete", "setting", "select"}, 
                                             self.settingData)
        
        self.fileTable.resizeCol(FileTable.MainTableDimension)
        self.transcribeBtn.clicked.connect(self.transcribe)
        self.uploadFileBtn.clicked.connect(self.fileTable.getFile)
        
    
    def goToSettingFun(self):
        self.signals.gotoSetting.emit()
        
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
                                      alignment=Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTop)
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
    
   
    def transcribe(self):
        self.nextStep(self.fileTable.transcribe())
       
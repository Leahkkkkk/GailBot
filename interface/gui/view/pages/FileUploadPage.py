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

from this import d
from xml.etree.ElementTree import TreeBuilder
from view.widgets import Label, Button, FileTable
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
    QTableView, 
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal,QObject

class Signals(QObject):
    """ contain signals in order for Qrunnable object to communicate
        with controller
    """
    gotoSetting = pyqtSignal()
    

            
            
class FileUploadPage(QWidget):
    def __init__(self, nextStep:callable, *args, **kwargs) -> None:
        """ file upload page """
        super().__init__(*args, **kwargs)
        self.nextStep = nextStep
        self.hideBtn = True
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
        self.addFileBtn = Button.ColoredBtn("Add File", 
                                            Color.BLUEMEDIUM,
                                            FontSize.SMALL)
        
        self.recordBtn = Button.ColoredBtn("Record live", 
                                           Color.BLUEMEDIUM,
                                           FontSize.SMALL)
        
        self.uploadFileBtn = Button.ColoredBtn("Add From Device", 
                                               Color.BLUEMEDIUM, 
                                               FontSize.SMALL)
        self.recordBtn.hide()
        self.uploadFileBtn.hide()
        self.transcribeBtn = Button.ColoredBtn("Transcribe", 
                                               Color.GREYMEDIUM1, 
                                               FontSize.BTN)
        self.addFileBtn.setFixedSize(Dimension.MEDIUMBUTTON)
        self.recordBtn.setFixedSize(Dimension.MEDIUMBUTTON)
        self.uploadFileBtn.setFixedSize(Dimension.MEDIUMBUTTON)
        self.transcribeBtn.setFixedSize(Dimension.BGBUTTON)
        self.settingProfile = Button.dropDownButton("Settings Profile", 
                                                    ["Default Settings",
                                                     "Coffee Setting", 
                                                     "Create New Profile"], 
                                                    [self.goToSettingFun, 
                                                     self.goToSettingFun,
                                                     self.goToSettingFun])
        self.fileTable = FileTable.FileTable()
        self.transcribeBtn.clicked.connect(self.transcribe)
        self.addFileBtn.clicked.connect(self._toggleBtn)
    
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
        self.verticalLayout.addWidget(self.fileTable,4,
                                      alignment = Qt.AlignmentFlag.AlignHCenter)
        self.spacer = QSpacerItem(500,70)
        self.verticalLayout.addItem(self.spacer)
        
        self.addFileBtnContainer = QWidget(self)
        self.containerLayout = QVBoxLayout()
        self.addFileBtnContainer.setLayout(self.containerLayout)
        self.containerLayout.setSpacing(2)
        
        
        self.containerLayout.addWidget(self.addFileBtn,
                                      alignment = Qt.AlignmentFlag.AlignHCenter)
        self.containerLayout.addWidget(self.uploadFileBtn,
                                      alignment = Qt.AlignmentFlag.AlignHCenter)
        self.containerLayout.addWidget(self.recordBtn,
                                       alignment = Qt.AlignmentFlag.AlignHCenter)
        self.containerLayout.addStretch()
        
        self.verticalLayout.addWidget(self.addFileBtnContainer,
                                       alignment = Qt.AlignmentFlag.AlignHCenter)
        
        self.verticalLayout.addWidget(self.transcribeBtn,
                                      alignment = Qt.AlignmentFlag.AlignHCenter)
        

    def _initStyle(self):
        """ initialize the style """
        initImgBackground(self,"backgroundConfirmPage.png")
        self.gotoMainBtn.setFixedSize(QSize(200,40))
        self.gotoMainBtn.setStyleSheet(f"border:none; color:{Color.BLUEMEDIUM}")
    
    def _toggleBtn(self):
        if self.hideBtn:
            self.recordBtn.show()
            self.uploadFileBtn.show()
        else:
            self.recordBtn.hide()
            self.uploadFileBtn.hide()
        self.hideBtn = not self.hideBtn
   
    def transcribe(self):
        indices = self.fileTable.selectedIndexes()
        if indices:
            self.nextStep()
        else:
            self.messageBox = MsgBox.WarnBox("No Files Selected")
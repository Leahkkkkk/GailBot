'''
File: TabPages.py
Project: GailBot GUI
File Created: Sunday, 16th October 2022 1:30:32 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Sunday, 16th October 2022 1:49:44 pm
Modified By:  Siara Small  & Vivian Li
-----
'''
import logging 
import datetime
from typing import List, TypedDict
from os import stat

from view.widgets.Button import ColoredBtn, BorderBtn
from view.widgets.Label import Label
from view.style.Background import initBackground
from view.style.styleValues import Color, FontFamily, FontSize
from view.style.widgetStyleSheet import buttonStyle

from PyQt6.QtWidgets import (
    QWidget, 
    QFileDialog, 
    QPushButton, 
    QLineEdit,
    QVBoxLayout, 
    QHBoxLayout,
    QLabel,
    QComboBox)
from PyQt6.QtCore import pyqtSignal, QObject, QSize

class FileData(TypedDict):
    Name: str
    Type: str
    Date: str 
    Size: int 
    Output: str 
    FullPath: str

class OutputPath(TypedDict):
    Output:str

class Profile(TypedDict):
    Profile:str

class Signals(QObject):
    """ contain signals to communicate with the parent tab """
    nextPage = pyqtSignal()
    previousPage = pyqtSignal()
    close = pyqtSignal()


class OpenFile(QWidget):
    """  for user to select file from their directory """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fullName = None 
        self.fileType = None
        self.filePathDisplay = QLineEdit(self)
        self.filePathDisplay.setReadOnly(True)
        self.fileBtn = ColoredBtn("choose file", Color.BLUEMEDIUM)
        self.signals = Signals()
        self.fileBtn.clicked.connect(self._addFile)
        self._initLayout()
    
    def _addFile(self):
        """ open a fle dialog for user to select a file  """
        fileDialog = QFileDialog(self)
        fileFilter = "*.txt *.wav *.png"
        fileDialog.setNameFilter(fileFilter)
        fileDialog.setFileMode(QFileDialog.FileMode.AnyFile)
        filename = fileDialog.getOpenFileName()
        if filename[0] != "":
            self.fullName = filename[0]
            print(filename[0])
            self.fileType = "🔈"
            self.filePathDisplay.setText(filename[0])
            self.signals.nextPage.emit()
        else:
            logging.warn("No File Chosen")

    def _initLayout(self):
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)
        self.layout.addWidget(self.filePathDisplay)
        self.layout.addWidget(self.fileBtn)
        self.fileBtn.setFixedSize(QSize(100,30))
        
    def getFile(self) -> FileData:
        if not self.fullName or not self.fileType:
            logging.error("File is not found")
        
        fullPath = self.fullName
        fileType = self.fileType
        date = datetime.date.today().strftime("%m-%d-%y")    
        temp = str(fullPath)
        patharr = temp.split("/")
        fileName = patharr[-1]
        size = round(stat(fullPath).st_size, 2)
       
        return {"Name": fileName, 
                "Type": fileType, 
                "Date": date, 
                "Size": size, 
                "FullPath": fullPath}


class ChooseSet(QWidget):
    """ for user to choose setting profile """
    def __init__(self, settings: List[str], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        print(settings)
        self.profile = settings[0]
        self.settings = settings
        self.signals = Signals()
        self._initWidget()
        self._initLayout()
        self.setAutoFillBackground(True)
        
    def _initWidget(self):
        self.label = Label("select setting profile", FontSize.HEADER3 )
        self.selectSettings = QComboBox(self)
        self.selectSettings.addItems(self.settings)
        self.selectSettings.setCurrentText("None")
        self.confirmBtn = ColoredBtn("confirm", Color.GREEN)
        self.selectSettings.currentTextChanged.connect(self._updateSettings)
        self.confirmBtn.clicked.connect(self._updatePageState)
    
    def _initLayout(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.selectSettings)
        self.layout.addWidget(self.confirmBtn)
        
    def _updateSettings(self, setting):
        if setting:
            self.profile = setting
            
    def _updatePageState(self):
        if self.profile:
            self.signals.nextPage.emit()
        else:
            logging.warn("the profile is not chosen")
            
    def getProfile(self) -> Profile:
        """ return the selected setting """
        if self.profile:
            return {"Profile": self.profile}
        else:
            logging.warn("the profile is not chosen")
        

class ChooseOutPut(QWidget):
    """ for user to choose output directory  """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.outPath = None
        self.signals = Signals()
        self._iniWidget()
        self._initLayout()
        
    def _iniWidget(self):
        self.chooseDirBtn = ColoredBtn("choose output directory", Color.BLUEMEDIUM)
        self.dirPathText = QLineEdit(self)
        self.dirPathText.setReadOnly(True)
        self.chooseDirBtn.clicked.connect(self._addDir)
        
    def _initLayout(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.dirPathText)
        self.layout.addWidget(self.chooseDirBtn)
    
    def _addDir(self):
        fileDialog = QFileDialog()
        outPath = fileDialog.getExistingDirectory(None, "Select Folder")
        if outPath:
            self.outPath = outPath
            self.signals.close.emit()
            self.dirPathText.setText(outPath)
        else: 
            logging.warn("No ouput directory is chosen")
    
    
    def getOutputPath(self) -> OutputPath:
        """ return the selected output path """
        if not self.outPath:
            logging.error("No output direcory was chosen")
        return {"Output": self.outPath}





        
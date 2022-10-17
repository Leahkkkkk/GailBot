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
from view.style.Background import initBackground

from view.style.Background import Background 
from view.style.styleValues import Color

from PyQt6.QtWidgets import (
    QWidget, 
    QFileDialog, 
    QPushButton, 
    QVBoxLayout, 
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
    nextPage = pyqtSignal(int)
    close = pyqtSignal()

class OpenFile(QWidget):
    """  for user to select file from their directory """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fullName = None 
        self.fileType = None
        self.fileBtn = QPushButton("Choose File")
        self.dirBtn = QPushButton("Choose Directory")
        self.signals = Signals()
        self.fileBtn.clicked.connect(self._addFile)
        self.dirBtn.clicked.connect(self._addDir)
        self._initLayout()
    
    def _addFile(self):
        """ open a fle dialog for user to select a file  """
        fileDialog = QFileDialog(self)
        fileFilter = "*.txt *.wav *.png"
        fileDialog.setNameFilter(fileFilter)
        filename = fileDialog.getOpenFileName()
        print(filename)
        if filename[0] != "":
            self.signals.nextPage.emit(1)
            self.fullName = filename[0]
            print(filename[0])
            self.fileType = "🔈"
        else:
            logging.warn("No File Chosen")
    
    def _addDir(self):
        """ open a file dialog for user to select a folder """
        fileDialog = QFileDialog()
        outPath = fileDialog.getExistingDirectory(None, "Select Folder")
        if outPath != "":
            self.signals.nextPage.emit(1)
            self.fullName = outPath
            self.fileType = "📁"
        else:
            logging.warn("No File Chosen")
            

    def _initLayout(self):
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.layout.addWidget(self.fileBtn)
        self.layout.addWidget(self.dirBtn)
    
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
        self.setFixedSize(QSize(250,250))
        self.profile = settings[0]
        self.settings = settings
        self.signals = Signals()
        self._initWidget()
        self._initLayout()
        
    def _initWidget(self):
        self.label = QLabel("select setting profile", self)
        self.selectSettings = QComboBox(self)
        self.selectSettings.addItems(self.settings)
        self.confirmBtn = QPushButton("confirm", self)
        self.selectSettings.currentTextChanged.connect(self._updateSettings)
        self.confirmBtn.clicked.connect(self._updatePageState)
    
    def _initLayout(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.selectSettings)
        
    def _updateSettings(self, setting):
        if setting:
            self.profile = setting
            
    def _updatePageState(self):
        if self.profile:
            self.signals.nextPage.emit(2)
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
        self.chooseDirBtn = QPushButton("choose output directory")
        self.submitBtn = QPushButton("confirm to add")
        self.chooseDirBtn.clicked.connect(self._addDir)
        self.submitBtn.clicked.connect(self._confirm)
        
    
    def _initLayout(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.chooseDirBtn)
        self.layout.addWidget(self.submitBtn)
    
    def _addDir(self):
        fileDialog = QFileDialog()
        outPath = fileDialog.getExistingDirectory(None, "Select Folder")
        if outPath:
            self.outPath = outPath
        else: 
            logging.warn("No ouput directory is chosen")
    
    def _confirm(self):
        if not self.outPath:
            logging.error("No output path is choosen")
        else:
            self.signals.close.emit()
    
    def getOutputPath(self) -> OutputPath:
        """ return the selected output path """
        if not self.outPath:
            logging.error("No output direcory was chosen")
        return {"Output": self.outPath}
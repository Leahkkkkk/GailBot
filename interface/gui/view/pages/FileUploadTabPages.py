'''
File: TabPages.py
Project: GailBot GUI
File Created: Sunday, 16th October 2022 1:30:32 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Sunday, 16th October 2022 1:49:44 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: implementation of pages for user to upload new files
'''
import logging 
import datetime
import pathlib
from typing import List, TypedDict
import os

from util.Style import Color, FontSize, Dimension
from util.Text import FileUploadPageText as Text
from model.dataBase.fileDB import fileDict
from view.widgets.Button import ColoredBtn
from view.widgets.Label import Label
from view.widgets.TabPage import TabPage

from PyQt6.QtWidgets import (
    QWidget,
    QFileDialog, 
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout,
    QComboBox,
    QAbstractItemView,
    QTableWidget,
    QTableWidgetItem)
from PyQt6.QtCore import QSize, Qt

center = Qt.AlignmentFlag.AlignHCenter


class OutputPath(TypedDict):
    """ class representing the output path of a file or directory """
    Output:str

class Profile(TypedDict):
    """ class representing a profile """
    Profile:str

class OpenFile(TabPage):
    """ implement a page that allow use to upload file or directory 
    
    Public functions: 
    1.  getFile(self) -> List[fileDict]
        return a list of files uploaded by the user
    """
    def __init__(self, *args, **kwargs) -> None:
        """ initializes class """
        super().__init__(*args, **kwargs)
        self._initWidget()
        self._initLayout()
        self._connectSignal()
        self._initStyle()
        self._initDimension()
    
    def getFile(self) -> List[fileDict]:
        """ returns a list of files object that user has selected """
        fileList = []
        for file in self.filePaths:
            fileObj = self._pathToFileObj(file)
            fileList.append(fileObj)
        return fileList
        
    def _initWidget(self):
        """ initializes the widgets """
        self.fileDisplayList = QTableWidget()
        self.filePaths = []
        self.uploadFileBtn = ColoredBtn(
            Text.tabAddfile, 
            Color.PRIMARY_BUTTON)
        self.uploadFolderBtn = ColoredBtn(
            Text.tabAddFolder,
            Color.PRIMARY_BUTTON)
       
    def _initLayout(self):
        """ initializes the layout  """
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.buttonContainer = QWidget()
        self.buttonContainerLayout = QHBoxLayout()
        self.buttonContainer.setLayout(self.buttonContainerLayout)
        self.buttonContainerLayout.addWidget(self.uploadFileBtn)
        self.buttonContainerLayout.addWidget(self.uploadFolderBtn)
        self.mainLayout.addWidget(self.fileDisplayList, alignment=center)
        self.mainLayout.addWidget(self.buttonContainer,alignment=center)
        
    def _connectSignal(self):
        """ connects the signals upon button clicks """
        self.uploadFileBtn.clicked.connect(self._getFiles)
        self.uploadFolderBtn.clicked.connect(self._getFolders)
        
    def _initStyle(self):
        """ initialize the style  """
        self.fileDisplayList.setAlternatingRowColors(True)
        self.fileDisplayList.insertColumn(0)
        self.fileDisplayList.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection)
        self.fileDisplayList.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers)
        self.fileDisplayList.horizontalHeader().hide()
        self.fileDisplayList.verticalHeader().hide()
    
    def _initDimension(self):
        """ initializes the dimensions """
        self.fileDisplayList.setFixedSize(QSize(Dimension.SMALL_TABLE_WIDTH,
                                                Dimension.SMALL_TABLE_HEIGHT))
        
    
    def _pathToFileObj(self, path):  
        """ converts the file path to a file object  """  
        fullPath = path
        date = datetime.date.today().strftime("%m-%d-%y")    
        temp = str(fullPath)
        patharr = temp.split("/")
        size = round(os.stat(fullPath).st_size/1000, 2)
        if os.path.isdir(path):
            fileType = Text.directoryLogo
            fileName = patharr[-2]
        else:
            fileType = pathlib.Path(path).suffix
            if fileType == ".wav":
                fileType = Text.audioLogo
            fileName = patharr[-1]
            
        return {"Name": fileName, 
                "Type": fileType, 
                "Date": date, 
                "Size": f"{size}kb", 
                "FullPath": fullPath}

    def _getFiles (self):
        """ select current file paths """
        dialog = QFileDialog()
        fileFilter = Text.fileFilter
        selectedFiles = dialog.getOpenFileNames(filter = fileFilter)
        if selectedFiles:
            files, types = selectedFiles
            print (selectedFiles)
            self.signals.nextPage.emit()
            self.filePaths = self.filePaths + files
            for file in files:
                self._addFileToFileDisplay(file)
            
    def _getFolders (self):
        """ gets the current directory and displays the selected file """
        dialog = QFileDialog() 
        selectedFolder = dialog.getExistingDirectory()
        if selectedFolder:
            self._addFileToFileDisplay(selectedFolder)

    def _addFileToFileDisplay(self, file):
        """ add the file to the file display table """
        row = self.fileDisplayList.rowCount()
        self.fileDisplayList.insertRow(row)
        newfile = QTableWidgetItem(file)
        self.fileDisplayList.setItem(row, 0, newfile)
        self.fileDisplayList.resizeColumnsToContents()
        self.fileDisplayList.resizeRowsToContents()

class ChooseSet(TabPage):
    """ implement a page for user to choose the setting profile
    
    Public Function:
    1.  getProfile(self) -> Profile
        return the profile chosen by the user 
    
    
    """
    
    def __init__(self, settings: List[str], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        print(settings)
        self.profile = settings[0]
        self.settings = settings
        self._initWidget()
        self._initLayout()
        self.setAutoFillBackground(True)
    
    def getProfile(self) -> Profile:
        """ return the selected setting """
        if self.profile:
            return {"Profile": self.profile}
        else:
            logging.warn("the profile is not chosen")
        
    def _initWidget(self):
        """ initializes the widgets """
        self.label = Label("select setting profile", FontSize.HEADER3)
        self.selectSettings = QComboBox(self)
        self.selectSettings.addItem(Text.selectSetText)
        self.selectSettings.addItems(self.settings)
        self.selectSettings.setCurrentText("None")
        self.selectSettings.currentTextChanged.connect(self._updateSettings)
        self.selectSettings.currentIndexChanged.connect(self._toNextPage)
   
    def _initLayout(self):
        """ initializes the layouts """
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.selectSettings)
        
    def _updateSettings(self, setting):
        """ updates the settings
        Args: setting: new settings value with which to update
        """
        if setting:
            self.profile = setting
            
    def _toNextPage(self, idx):
        """ takes user to the next page in the tab popup """
        if idx != 0:
            self.signals.nextPage.emit()
        else:
            logging.warn("The profile has not been chosen")
            

        
class ChooseOutPut(TabPage):
    """ implement a page for user to choose output directory  
    
    Public Function:
    1.  getOutputPath(self) -> OutputPath 
        return the output path chosen by user
    """
    def __init__(self, *args, **kwargs) -> None:
        """ initializes the class """
        super().__init__(*args, **kwargs)
        self.outPath = None
        self._iniWidget()
        self._initLayout()
    
          
    def getOutputPath(self) -> OutputPath:
        """ returns the selected output path """
        if not self.outPath:
            logging.error("No output direcory is chosen")
        return {"Output": self.outPath}
        
    def _iniWidget(self):
        """ initializes the widgets """
        self.chooseDirBtn = ColoredBtn("...", Color.PRIMARY_BUTTON, FontSize.HEADER2)
        self.chooseDirBtn.setFixedWidth(70)
        self.dirPathText = QLineEdit(self)
        self.dirPathText.setPlaceholderText(Text.chooseOutPutText)
        self.dirPathText.setMinimumHeight(40)
        self.dirPathText.setReadOnly(True)
        self.chooseDirBtn.clicked.connect(self._addDir)
        
    def _initLayout(self):
        """ initializes the layout """
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.dirPathText)
        self.layout.addWidget(self.chooseDirBtn)
    
    def _addDir(self):
        """ adds existing directpry as output directory """
        fileDialog = QFileDialog()
        outPath = fileDialog.getExistingDirectory(None, Text.selectFolderText)
        if outPath:
            self.outPath = outPath
            self.signals.close.emit()
            self.dirPathText.setText(outPath)
        else: 
            logging.warn("No output directory is chosen")

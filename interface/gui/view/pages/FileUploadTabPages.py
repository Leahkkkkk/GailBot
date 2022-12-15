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
from util.Logger import makeLogger
from model.dataBase.FileDatabase import fileDict
from view.widgets.Button import ColoredBtn
from view.widgets.Label import Label
from view.widgets.TabPage import TabPage
from view.widgets.MsgBox import WarnBox
from view.widgets.ComboBox import ComboBox

import userpaths
from PyQt6.QtWidgets import (
    QWidget,
    QFileDialog, 
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout,
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
        self.logger = makeLogger("F")
        self._initWidget()
        self._initLayout()
        self._connectSignal()
        self._initStyle()
        self._initDimension()
    
    def getFile(self) -> List[fileDict]:
        """ returns a list of files object that user has selected """
        self.logger.info("")
        fileList = []
        try:
            for file in self.filePaths:
                fileObj = self._pathToFileObj(file)
                fileList.append(fileObj)
            return fileList
        except:
            WarnBox("An error ocurred in getting the files to be transcribed")
        
    def _initWidget(self):
        """ initializes the widgets """
        self.logger.info("")
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
        self.logger.info("")
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
        self.logger.info("")
        self.uploadFileBtn.clicked.connect(self._getFiles)
        self.uploadFolderBtn.clicked.connect(self._getFolders)
        
    def _initStyle(self):
        """ initialize the style  """
        self.logger.info("")
        self.fileDisplayList.insertColumn(0)
        self.fileDisplayList.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection)
        self.fileDisplayList.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers)
        self.fileDisplayList.horizontalHeader().hide()
        self.fileDisplayList.verticalHeader().hide()
        self.fileDisplayList.setStyleSheet(f"background-color:{Color.MAIN_BACKRGOUND};"
                                           f"color:{Color.MAIN_TEXT}")
        self.fileDisplayList.setColumnWidth(0,Dimension.SMALL_TABLE_WIDTH) 
    def _initDimension(self):
        """ initializes the dimensions """
        self.logger.info("")
        self.fileDisplayList.setFixedSize(QSize(Dimension.SMALL_TABLE_WIDTH,
                                                Dimension.SMALL_TABLE_HEIGHT))
        
    
    def _pathToFileObj(self, path):  
        """ converts the file path to a file object  """  
        self.logger.info("")
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
        self.logger.info("")
        try:
            dialog = QFileDialog()
            dialog.setDirectory(userpaths.get_desktop())
            fileFilter = Text.fileFilter
            selectedFiles = dialog.getOpenFileNames(filter = fileFilter)
            if selectedFiles:
                files, types = selectedFiles
                self.filePaths = self.filePaths + files
                if self.filePaths:
                    self.signals.nextPage.emit()
                else:
                    WarnBox("No file is uploaded by user")   
                for file in files:
                    self._addFileToFileDisplay(file)
            else:
                WarnBox("No file is uploaded is uploaded by user")
                self.logger.warn("No file is uploaded by user")
        except:
            WarnBox("An error occurred when getting the uploaded file")
            
    def _getFolders (self):
        """ gets the current directory and displays the selected file """
        self.logger.info("")
        try:
            dialog = QFileDialog() 
            selectedFolder = dialog.getExistingDirectory()
            
            if selectedFolder:
                self.filePaths = self.filePaths + [selectedFolder]
                self._addFileToFileDisplay(selectedFolder)
                if self.filePaths:
                    self.signals.nextPage.emit()
            else:
                WarnBox("No file is uploaded by user")
        except:
            WarnBox("An error occurred when getting the uploaded folder")

    def _addFileToFileDisplay(self, file):
        """ add the file to the file display table """
        self.logger.info("")
        try:
            row = self.fileDisplayList.rowCount()
            self.fileDisplayList.insertRow(row)
            newFile = QTableWidgetItem(file)
            self.fileDisplayList.setItem(row, 0, newFile)
            # self.fileDisplayList.resizeColumnsToContents()
            self.fileDisplayList.resizeRowsToContents()
        except:
            WarnBox("An error occurred when displaying the added file")

class ChooseSet(TabPage):
    """ implement a page for user to choose the setting profile
    
    Public Function:
    1.  getProfile(self) -> Profile
        return the profile chosen by the user 
    """
    def __init__(self, settings: List[str], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.profile = settings[0]
        self.settings = settings
        self.logger = makeLogger("F")
        self._initWidget()
        self._initLayout()
        self.setAutoFillBackground(True)
    
    def getProfile(self) -> Profile:
        """ return the selected setting """
        self.logger.info("")
        if self.profile:
            return {"Profile": self.profile}
        else:
            logging.warn("the profile is not chosen")
        
    def _initWidget(self):
        """ initializes the widgets """
        self.logger.info("")
        self.label = Label("select setting profile", FontSize.HEADER3)
        self.selectSettings = ComboBox(self)
        self.selectSettings.addItem(Text.selectSetText)
        self.selectSettings.addItems(self.settings)
        self.selectSettings.setCurrentText("None")
        self.selectSettings.currentTextChanged.connect(self._updateSettings)
        self.selectSettings.currentIndexChanged.connect(self._toNextPage)
   
    def _initLayout(self):
        """ initializes the layouts """
        self.logger.info("")
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.selectSettings)
        
    def _updateSettings(self, setting):
        """ updates the settings
        Args: setting: new settings value with which to update
        """
        self.logger.info("")
        if setting:
            self.profile = setting
            
    def _toNextPage(self, idx):
        """ takes user to the next page in the tab popup """
        self.logger.info("")
        if self.selectSettings.currentText != Text.selectSetText:
            self.signals.nextPage.emit()
            if self.selectSettings.itemText(0) == Text.selectSetText:
                self.selectSettings.removeItem(0)
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
        self.logger = makeLogger("F")
        self.outPath = None
        self._iniWidget()
        self._initLayout()
    
          
    def getOutputPath(self) -> OutputPath:
        """ returns the selected output path """
        try: 
            if not self.outPath:
                logging.error("No output directory is chosen")
                WarnBox("No output directory is chosen")
            else:
                return {"Output": self.outPath}
        except:
            WarnBox("An error occurred when reading output directory")
        
    def _iniWidget(self):
        """ initializes the widgets """
        self.logger.info("")
        self.chooseDirBtn = ColoredBtn("...", Color.PRIMARY_BUTTON, FontSize.HEADER2)
        self.chooseDirBtn.setFixedWidth(70)
        self.dirPathText = QLineEdit(self)
        self.dirPathText.setPlaceholderText(Text.chooseOutPutText)
        self.dirPathText.setMinimumHeight(40)
        self.dirPathText.setReadOnly(True)
        self.chooseDirBtn.clicked.connect(self._addDir)
        
    def _initLayout(self):
        """ initializes the layout """
        self.logger.info("")
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.dirPathText)
        self.layout.addWidget(self.chooseDirBtn)
    
    def _addDir(self):
        """ adds existing directory as output directory """
        self.logger.info("")
        fileDialog = QFileDialog()
        outPath = fileDialog.getExistingDirectory(None, Text.selectFolderText)
        if outPath:
            self.outPath = outPath
            self.signals.close.emit()
            self.dirPathText.setText(outPath)
        else: 
            logging.warn("No output directory is chosen")

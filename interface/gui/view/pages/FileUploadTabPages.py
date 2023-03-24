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

from view.config.Style import Color, FontSize, Dimension, FontFamily
from view.config.Text import FileUploadPageText as Text
from view.util.io import get_name, is_directory
from gbLogger import makeLogger
from controller.mvController import fileDict
from view.widgets.Button import ColoredBtn
from view.widgets.Label import Label
from view.widgets.TabPage import TabPage
from view.widgets.MsgBox import WarnBox
from view.widgets.ComboBox import ComboBox
from view.util.ErrorMsg import WARN, ERR
from PyQt6.QtWidgets import (
    QWidget,
    QFileDialog, 
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout,
    QAbstractItemView,
    QTableWidget,
    QTableWidgetItem,
    QPushButton)
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QDragEnterEvent 

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
        self.setAcceptDrops(True)
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
            for file in self.filePaths.values():
                self.logger.info(f"get file path {file}")
                fileObj = self._pathToFileObj(file)
                fileList.append(fileObj)
            return fileList
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("uploading files", str(e)))
            return False
        
    def _initWidget(self):
        """ initializes the widgets """
        self.logger.info("")
        self.header = Label(Text.uploadInstruction, FontSize.BTN, FontFamily.MAIN)
        self.fileDisplayList = QTableWidget()
        self.filePaths = dict()
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
        self.mainLayout.addWidget(self.header, alignment=center)
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
        self.fileDisplayList.insertColumn(1)
        self.fileDisplayList.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection)
        self.fileDisplayList.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers)
        self.fileDisplayList.horizontalHeader().hide()
        self.fileDisplayList.verticalHeader().hide()
        self.fileDisplayList.setStyleSheet(f"background-color:{Color.MAIN_BACKGROUND};"
                                           f"color:{Color.MAIN_TEXT}")
        self.fileDisplayList.setColumnWidth(0,Dimension.SMALL_TABLE_WIDTH) 
    
    def _initDimension(self):
        """ initializes the dimensions """
        self.logger.info("")
        self.fileDisplayList.setFixedSize(QSize(Dimension.SMALL_TABLE_WIDTH,
                                                Dimension.SMALL_TABLE_HEIGHT)) 
        self.fileDisplayList.setColumnWidth(0, 325)
        self.fileDisplayList.setColumnWidth(1, 25)
    
    def _pathToFileObj(self, path:str):  
        """ converts the file path to a file object  """  
        fullPath = path
        self.logger.info(fullPath)
        date = datetime.date.today().strftime("%m-%d-%y")    
        size = round(os.stat(fullPath).st_size/1000, 2)
        fileName = get_name(fullPath)
        fileType = Text.directoryLogo if is_directory(path) else Text.audioLogo
            
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
            fileFilter = Text.fileFilter
            selectedFiles = dialog.getOpenFileNames(filter = fileFilter)
            if selectedFiles:
                files, types = selectedFiles
                for file in files:
                    self._addFileToFileDisplay(file)
                if self.filePaths:
                    self.signals.nextPage.emit()
                else:
                    WarnBox(WARN.NO_FILE)   
            else:
                WarnBox(WARN.NO_FILE)
                self.logger.warn(WARN.NO_FILE)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("uploading files", str(e)))
            
    def _getFolders (self):
        """ gets the current directory and displays the selected file """
        self.logger.info("")
        try:
            dialog = QFileDialog() 
            selectedFolder = dialog.getExistingDirectory()
            if selectedFolder:
                self._addFileToFileDisplay(selectedFolder)
                if self.filePaths:
                    self.signals.nextPage.emit()
            else:
                WarnBox(WARN.NO_FILE)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("uploading folder", str(e)))

    def _addFileToFileDisplay(self, file):
        """ add the file to the file display table """
        self.logger.info("")
        icon = Text.directoryLogo if os.path.isdir(file) else Text.audioLogo
        try:
            row = self.fileDisplayList.rowCount()
            self.fileDisplayList.insertRow(row)
            self.filePaths[row] = file
            filestr = os.path.join(os.path.basename(os.path.dirname(file)),os.path.basename(file))
            newFile = QTableWidgetItem(icon + filestr)
            self.fileDisplayList.setItem(row, 0, newFile)
            btn = QPushButton(Text.delete)
            btn.setFixedSize(QSize(20,20))
            btn.setContentsMargins(1,5,1,5)
            self.fileDisplayList.setCellWidget(row, 1, btn)
            btn.clicked.connect(lambda: self.removeFile(row, newFile))
            self.fileDisplayList.resizeRowsToContents()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("displaying uploaded file", str(e)))
    
    def removeFile(self, key, fileItem: QTableWidgetItem):
        self.logger.info("remove the file with key {key}")
        try:
            row = self.fileDisplayList.indexFromItem(fileItem).row()
            self.logger.info(f"removing the row {row}")
            self.fileDisplayList.removeRow(row)
            del self.filePaths[key]
        except Exception as e:
            self.logger.error(e, exc_info=e)

    def dragEnterEvent(self, a0: QDragEnterEvent) -> None:
        self.logger.info("get the drag event for user to upload file")
        super().dragEnterEvent(a0)
        if a0.mimeData().hasUrls():
            urls = a0.mimeData().urls()
            self.logger.info(f"received the dragged file{urls}")
            for url in urls:
                path = url.toLocalFile()
                if url.isLocalFile() and path.endswith(".wav") or os.path.isdir(path):
                    self._addFileToFileDisplay(path)
                    self.signals.nextPage.emit()
                    
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
        self.label = Label("Select Setting Profile", FontSize.HEADER3, FontFamily.MAIN)
        self.selectSettings = ComboBox(self)
        self.selectSettings.addItem(Text.selectSetText)
        self.selectSettings.addItems(self.settings)
        self.selectSettings.setCurrentText("None")
        self.selectSettings.currentTextChanged.connect(self._updateSettings)
        self.selectSettings.currentIndexChanged.connect(self._toNextPage)
   
    def _initLayout(self):
        """ initializes the layouts """
        self.logger.info("")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addStretch()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.selectSettings)
        self.layout.addStretch()
        
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
                WarnBox(WARN.NO_OUT_PATH)
            else:
                return {"Output": self.outPath}
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("getting output directory", str(e)))
        
    def _iniWidget(self):
        """ initializes the widgets """
        self.logger.info("")
        self.chooseDirBtn = ColoredBtn("···", Color.PRIMARY_BUTTON, FontSize.HEADER2)
        self.chooseDirBtn.setFixedWidth(70)
        self.dirPathText = QLineEdit(self)
        self.dirPathText.setPlaceholderText(Text.chooseOutPutText)
        self.dirPathText.setMinimumHeight(40)
        self.dirPathText.setReadOnly(True)
        self.dirPathText.setStyleSheet( "QLineEdit {"
                                        "    padding: 5px;"
                                        "    border-radius: 5px;"
                                        "    border: 1px solid black;"
                                        "}")
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

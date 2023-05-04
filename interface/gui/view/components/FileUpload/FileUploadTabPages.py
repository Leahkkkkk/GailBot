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
from typing import List, TypedDict
import os

from controller.mvController import fileDict
from view.config.Text import FileUploadPageText as Text
from view.config.WorkSpace import (
    updateSavedUploadFileDir, 
    getSavedUploadFileDir,
    updateSavedOutputDir,
    getSavedOutputDir)
from view.util.io import get_name, is_directory
from gbLogger import makeLogger
from view.widgets.Label import Label
from view.widgets.TabPage import TabPage
from view.widgets.MsgBox import WarnBox
from view.widgets.Button import ColoredBtn
from view.widgets.ComboBox import ComboBox
from view.widgets.Background import initSecondaryColorBackground
from view.widgets.Button import InstructionBtn
from view.config.InstructionText import INSTRUCTION
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

#### controlling style changes 
from view.config.Style import Dimension, STYLE_DATA, FontFamily

######################
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
        self.blockNext = True
        super().__init__(blockNext=True)
        self.setAcceptDrops(True)
        self.logger = makeLogger("F")
        self.userRootDir = getSavedUploadFileDir()
        self._initWidget()
        self._initLayout()
        self._connectSignal()
        self._initStyle()
        self._initDimension()
    
    def initState(self):
        if self.filePaths:
            self.signals.nextPage.emit()
        else:
            self.signals.blockNextPage.emit()
    
    def getFile(self) -> List[fileDict]:
        """ returns a list of files object that user has selected """
        self.logger.info("")
        fileList = []
        try:
            for file in self.filePaths.values():
                self.logger.info(f"get file path {file}")
                fileObj = self._pathToFileObj(file)
                fileList.append(fileObj)
            updateSavedUploadFileDir(self.userRootDir)
            return fileList
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("uploading files", str(e)))
            return False
        
    def _initWidget(self):
        """ initializes the widgets """
        self.logger.info("")
        self.header = Label(Text.uploadInstruction, STYLE_DATA.FontSize.HEADER4, FontFamily.MAIN)
        self.fileDisplayList = QTableWidget()
        self.filePaths = dict()
        self.uploadFileBtn = ColoredBtn(
            Text.tabAddfile, 
            STYLE_DATA.Color.PRIMARY_BUTTON)
        self.uploadFolderBtn = ColoredBtn(
            Text.tabAddFolder,
            STYLE_DATA.Color.PRIMARY_BUTTON)
       
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
        self.fileDisplayList.setStyleSheet(f"background-color:{STYLE_DATA.Color.MAIN_BACKGROUND};"
                                           f"color:{STYLE_DATA.Color.MAIN_TEXT}")
    
    def _initDimension(self):
        """ initializes the dimensions """
        self.logger.info("")
        self.fileDisplayList.setFixedSize(QSize(Dimension.SMALL_TABLE_WIDTH,
                                                Dimension.SMALL_TABLE_HEIGHT)) 
        self.fileDisplayList.setColumnWidth(0, self.fileDisplayList.width() - Dimension.SMALLICONBTN - 2)
        self.fileDisplayList.setColumnWidth(1, Dimension.SMALLICONBTN)
    
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
            dialog.setDirectory(self.userRootDir)
            fileFilter = Text.fileFilter
            selectedFiles = dialog.getOpenFileNames(filter = fileFilter)
            if selectedFiles:
                files, types = selectedFiles
                for file in files:
                    self._addFileToFileDisplay(file)
                    self.userRootDir = os.path.dirname(file)
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
            dialog.setDirectory(self.userRootDir)
            selectedFolder = dialog.getExistingDirectory()
            if selectedFolder:
                self._addFileToFileDisplay(selectedFolder)
                self.userRootDir = os.path.dirname(selectedFolder)
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
            btn.setFixedSize(QSize(Dimension.SMALLICONBTN,Dimension.SMALLICONBTN))
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
        super().__init__( *args, **kwargs)
        self.profile = settings[0]
        self.settings = settings
        self.logger = makeLogger("F")
        self._initWidget()
        self._initLayout()
        self.setAutoFillBackground(True)
        initSecondaryColorBackground(self)
    
    def getProfile(self) -> Profile:
        """ return the selected setting """
        self.logger.info("")
        if self.profile:
            return {"Profile": self.selectSettings.currentText()}
        else:
            logging.warn("the profile is not chosen")
        
    def _initWidget(self):
        """ initializes the widgets """
        self.logger.info("")
        self.label = Label("Select Setting Profile", STYLE_DATA.FontSize.HEADER4, FontFamily.MAIN)
        self.selectSettings = ComboBox(self)
        self.selectSettings.addItems(self.settings)
        self.selectSettings.setFixedWidth(350)
   
    def _initLayout(self):
        """ initializes the layouts """
        self.logger.info("")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addStretch()
        self.layout.addWidget(self.label, alignment=center)
        self.layout.addWidget(self.selectSettings, alignment=center)
        self.layout.addStretch()
        
class ChooseOutPut(TabPage):
    """ implement a page for user to choose output directory  
    
    Public Function:
    1.  getOutputPath(self) -> OutputPath 
        return the output path chosen by user
    """
    def __init__(self, *args, **kwargs) -> None:
        """ initializes the class """
        super().__init__(blockNext=True, *args, **kwargs)
        self.logger = makeLogger("F")
        self.outPath = None
        self.userRoot = getSavedOutputDir()
        self._initWidget()
        self._initLayout()
              
    def getOutputPath(self) -> OutputPath:
        """ returns the selected output path """
        try: 
            if not self.outPath:
                logging.error("No output directory is chosen")
                WarnBox(WARN.NO_OUT_PATH)
            else:
                updateSavedOutputDir(self.userRoot)
                return {"Output": self.outPath}
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("getting output directory", str(e)))
        
    def initState(self):
        if self.outPath:
            self.signals.nextPage.emit()
        else:
            self.signals.blockNextPage.emit()

    def _initWidget(self):
        """ initializes the widgets """
        self.logger.info("")
        self.chooseOuputLabel = Label(Text.selectOutput,  STYLE_DATA.FontSize.HEADER4, STYLE_DATA.FontFamily.MAIN)
        self.chooseDirBtn = ColoredBtn("···", STYLE_DATA.Color.PRIMARY_BUTTON, STYLE_DATA.FontSize.HEADER4)
        self.chooseDirBtn.setFixedWidth(70)
        self.dirPathText = QLineEdit(self)
        self.dirPathText.setPlaceholderText(Text.chooseOutPutText)
        self.dirPathText.setMinimumHeight(40)
        self.dirPathText.setFixedWidth(350)
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
        self.vlayout = QVBoxLayout()
        self.setLayout(self.vlayout)
        self.selectContainer = QWidget()
        self.hlayout = QHBoxLayout()
        self.selectContainer.setLayout(self.hlayout)
        self.hlayout.addWidget(self.dirPathText)
        self.hlayout.addWidget(self.chooseDirBtn)
        self.vlayout.addStretch()
        self.vlayout.addWidget(self.chooseOuputLabel, alignment=center)
        self.vlayout.addWidget(self.selectContainer, alignment=center)
        self.vlayout.addStretch()
    
    def _addDir(self):
        """ adds existing directory as output directory """
        self.logger.info("add the existing directory")
        fileDialog = QFileDialog()
        fileDialog.setDirectory(self.userRoot)
        outPath = fileDialog.getExistingDirectory()
        
        if outPath:
            self.outPath = outPath
            self.signals.nextPage.emit()
            self.dirPathText.setText(outPath)
            self.userRoot = outPath
        else: 
            logging.warn("No output directory is chosen")

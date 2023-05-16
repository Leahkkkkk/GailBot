'''
File: TabPages.py
Project: GailBot GUI
File Created: Sunday, 16th October 2022 1:30:32 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Sunday, 16th October 2022 1:49:44 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: implementation of pages for user to upload new files, 
             include UploadFileTab, ChooseSetTab, ChooseOutputTab
              
'''
import logging 
import datetime
from typing import List, TypedDict
import os

from controller.mvController import FileDict
from view.config.Text import FILEUPLOAD_PAGE as Text
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
from view.widgets.UploadTable import UploadTable
from view.util.ErrorMsg import WARN, ERR
from PyQt6.QtWidgets import (
    QWidget,
    QFileDialog, 
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDragEnterEvent 

#### controlling style changes 
from view.config.Style import STYLE_DATA

######################
center = Qt.AlignmentFlag.AlignHCenter

class OutputPath(TypedDict):
    """ class representing the output path of a file or directory """
    Output:str

class Profile(TypedDict):
    """ class representing a profile """
    Profile:str

class UploadFileTab(TabPage):
    """ implement a page that allow use to upload file or directory 
    
    Public functions: 
    1.  getFile(self) -> List[FileDict]
        return a list of files uploaded by the user
    """
    def __init__(self, *args, **kwargs) -> None:
        """ initializes class """
        self.blockNext = True
        super().__init__(blockNext=True)
        self.setAcceptDrops(True)
        self.logger = makeLogger()
        self.userRootDir = getSavedUploadFileDir()
        self._initWidget()
        self._initLayout()
        self._connectSignal()
    
    def getFile(self) -> List[FileDict]:
        """ returns a list of files object that user has selected """
        self.logger.info("")
        fileList = []
        try:
            for file in self.fileDisplayList.getValues():
                self.logger.info(f"get file path {file}")
                FileDict = self._pathTofileDict(file)
                fileList.append(FileDict)
            # for saving the current directory for next usage 
            updateSavedUploadFileDir(self.userRootDir)
            return fileList
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("uploading files", str(e)))
            return False
        
    def initState(self):
        """
        redefine function from the super class, send block next page signal
        to disallow user go to the next page until page ha been uploaded 
        """
        if self.filePaths:
            self.signals.nextPage.emit()
        else:
            self.signals.blockNextPage.emit()

    def _initWidget(self):
        """ initializes the widgets """
        self.logger.info("")
        self.header = Label(
            Text.DROP_FILE, 
            STYLE_DATA.FontSize.HEADER3,
            STYLE_DATA.FontFamily.MAIN)
        self.fileDisplayList = UploadTable(self.signals.blockNextPage)
        self.uploadFileBtn = ColoredBtn(
            Text.FROM_FILE, 
            STYLE_DATA.Color.PRIMARY_BUTTON)
        self.uploadFolderBtn = ColoredBtn(
            Text.FROM_FOLDER,
            STYLE_DATA.Color.PRIMARY_BUTTON)
        self.filePaths = list() ## stores the selected file / folder paths 
       
    def _initLayout(self):
        """ initializes the layout  """
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        buttonContainer = QWidget()
        buttonContainerLayout = QHBoxLayout()
        buttonContainer.setLayout(buttonContainerLayout)
        buttonContainerLayout.addWidget(self.uploadFileBtn)
        buttonContainerLayout.addWidget(self.uploadFolderBtn)
        mainLayout.addWidget(self.header, alignment=center)
        mainLayout.addWidget(self.fileDisplayList, alignment=center)
        mainLayout.addWidget(buttonContainer,alignment=center)
        
    def _connectSignal(self):
        """ connects the signals upon button clicks """
        self.uploadFileBtn.clicked.connect(self._getFiles)
        self.uploadFolderBtn.clicked.connect(self._getFolders)
        
    def _pathTofileDict(self, path:str):  
        """ converts the file path to a file object  """  
        fullPath = path
        self.logger.info(fullPath)
        date = datetime.date.today().strftime("%m-%d-%y")    
        fileName = get_name(fullPath)
        fileType = Text.DIR_LOGO if is_directory(path) else Text.AUDIO_LOGO
        return {"Name": fileName, 
                "Type": fileType, 
                "Date": date, 
                "FullPath": fullPath}

    def _getFiles (self):
        """ select current file paths """
        self.logger.info("")
        try:
            dialog = QFileDialog()
            dialog.setDirectory(self.userRootDir)
            FILE_FILTER = Text.FILE_FILTER
            selectedFiles = dialog.getOpenFileNames(filter = FILE_FILTER)
            if selectedFiles:
                files, types = selectedFiles
                for file in files:
                    self._addFileToFileDisplay(file)
                    self.userRootDir = os.path.dirname(file)
                    self.signals.nextPage.emit()
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
                self.signals.nextPage.emit()
            else:
                WarnBox(WARN.NO_FILE)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("uploading folder", str(e)))

    def _addFileToFileDisplay(self, file):
        """ add the file to the file display table """
        self.fileDisplayList.addItem(file)
        self.filePaths = self.fileDisplayList.getValues()
   
    def dragEnterEvent(self, a0: QDragEnterEvent) -> None:
        """ add file to the display list from dragging event """
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
                    
class ChooseSetTab(TabPage):
    """ implement a page for user to choose the setting profile
    
    Public Function:
    1.  getProfile(self) -> Profile
        return the profile chosen by the user 
    """
    def __init__(self, settings: List[str], *args, **kwargs) -> None:
        super().__init__( *args, **kwargs)
        self.profile = settings[0]
        self.settings = settings
        self.logger = makeLogger()
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
        self.label = Label(
            Text.CHOOSE_SET_TAB_HEADER, 
            STYLE_DATA.FontSize.HEADER3, 
            STYLE_DATA.FontFamily.MAIN)
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
        
class ChooseOutputTab(TabPage):
    """ implement a page for user to choose output directory  
    
    Public Function:
    1.  getOutputPath(self) -> OutputPath 
        return the output path chosen by user
    """
    def __init__(self, *args, **kwargs) -> None:
        """ initializes the class """
        super().__init__(blockNext=True, *args, **kwargs)
        self.logger = makeLogger()
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
        self.chooseOuputLabel = Label(Text.SELECT_OUTDIR,  STYLE_DATA.FontSize.HEADER3, STYLE_DATA.FontFamily.MAIN)
        self.chooseDirBtn = ColoredBtn("···", STYLE_DATA.Color.PRIMARY_BUTTON, STYLE_DATA.FontSize.HEADER4)
        self.chooseDirBtn.setFixedWidth(70)
        self.dirPathText = QLineEdit(self)
        self.dirPathText.setPlaceholderText(Text.SELECT_OUTDIR)
        self.dirPathText.setMinimumHeight(40)
        self.dirPathText.setFixedWidth(350)
        self.dirPathText.setReadOnly(True)
        self.dirPathText.setStyleSheet(STYLE_DATA.StyleSheet.STANDARD_LINE_EDIT)
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

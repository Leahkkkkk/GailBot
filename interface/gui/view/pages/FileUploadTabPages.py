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
import tomli 

from genericpath import isdir
import logging 
import datetime
import pathlib
from typing import List, TypedDict
import os

from util.Config import Color, FontSize
from view.widgets.Button import ColoredBtn, BorderBtn
from view.widgets.Label import Label
from view.widgets.TabPage import TabPage
from view.style.Background import initBackground
from view.style.widgetStyleSheet import buttonStyle

from PyQt6.QtWidgets import (
    QFileDialog, 
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout,
    QComboBox,
    QListWidget,
    QStackedWidget,
    QDialog,
    QListView)
from PyQt6.QtCore import QSize, Qt, QAbstractListModel

center = Qt.AlignmentFlag.AlignHCenter

class FileData(TypedDict):
    Name: str
    Type: str
    Date: str 
    Size: str 
    Output: str 
    FullPath: str

class OutputPath(TypedDict):
    Output:str

class Profile(TypedDict):
    Profile:str




class FileModel(QAbstractListModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.files = []
        
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            text = self.files[index.row()]
            return text

    def rowCount(self, index):
        return len(self.files)



class OpenFile(TabPage):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        # self.fileDisplayList = QListWidget()
        self.fileDisplayList = QListView()
        self.fileListModel = FileModel()
        self.fileDisplayList.setModel(self.fileListModel)
        self.filePaths = []
        self.uploadFileBtn = ColoredBtn(
            "Choose From Local", 
            Color.BLUEMEDIUM)
        self.uploadFileBtn.clicked.connect(lambda: self.getOpenFilesAndDirs())
        self.layout.addWidget(self.fileDisplayList, alignment=center)
        self.layout.addWidget(self.uploadFileBtn,alignment=center)
        self.fileDisplayList.setStyleSheet(
            f"border: 1px solid {Color.BLUEDARK};"
            "background-color:white;")
        
        
    def getFile(self) -> List[FileData]:
        fileList = []
        for file in self.filePaths:
            fileObj = self.pathToFileObj(file)
            fileList.append(fileObj)
        return fileList
    
    def pathToFileObj(self, path):    
        fullPath = path
        date = datetime.date.today().strftime("%m-%d-%y")    
        temp = str(fullPath)
        patharr = temp.split("/")
        size = round(os.stat(fullPath).st_size/1000, 2)
        if os.path.isdir(path):
            fileType = "📁"
            fileName = patharr[-2]
        else:
            fileType = pathlib.Path(path).suffix
            if fileType == ".wav":
                fileType = "🔈"
            fileName = patharr[-1]
            
        return {"Name": fileName, 
                "Type": fileType, 
                "Date": date, 
                "Size": f"{size}kb", 
                "FullPath": fullPath}

    def getOpenFilesAndDirs(self, filter=["audio file (*.wav)","directory (/)"]):
        def updateText():
                # update the contents of the line edit widget with the selected files
            selected = []
            for index in view.selectionModel().selectedRows():
                 selected.append('"{}"'.format(index.data()))
            lineEdit.setText(' '.join(selected))

        dialog = QFileDialog()
        dialog.setFileMode(dialog.FileMode.ExistingFiles)
        dialog.setOption(dialog.Option.DontUseNativeDialog, True)
    
        if filter:
            dialog.setNameFilters(filter)

        dialog.accept = lambda: QDialog.accept(dialog)
        stackedWidget = dialog.findChild(QStackedWidget)
        view = stackedWidget.findChild(QListView)
        view.selectionModel().selectionChanged.connect(updateText)

        lineEdit = dialog.findChild(QLineEdit)
        dialog.directoryEntered.connect(lambda: lineEdit.setText(''))
        dialog.exec() 
        selectedFiles = dialog.selectedFiles()
        if selectedFiles: 
            self.signals.nextPage.emit()  
            self.filePaths = self.filePaths + selectedFiles
            self.fileListModel.files.extend(selectedFiles)
            self.fileListModel.layoutChanged.emit()
           

    
class ChooseSet(TabPage):
    """ for user to choose setting profile """
    def __init__(self, settings: List[str], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        print(settings)
        self.profile = settings[0]
        self.settings = settings
        self._initWidget()
        self._initLayout()
        self.setAutoFillBackground(True)
        
    def _initWidget(self):
        self.label = Label("select setting profile", FontSize.HEADER3)
        self.selectSettings = QComboBox(self)
        self.selectSettings.addItem("select settings")
        self.selectSettings.addItems(self.settings)
        self.selectSettings.setCurrentText("None")
        self.selectSettings.currentTextChanged.connect(self._updateSettings)
        self.selectSettings.currentIndexChanged.connect(self._toNextPage)
   
    def _initLayout(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.selectSettings)

        
    def _updateSettings(self, setting):
        if setting:
            self.profile = setting
            
    def _toNextPage(self, idx):
        if idx != 0:
            self.signals.nextPage.emit()
        else:
            logging.warn("the profile is not chosen")
            
    def getProfile(self) -> Profile:
        """ return the selected setting """
        if self.profile:
            return {"Profile": self.profile}
        else:
            logging.warn("the profile is not chosen")

        
class ChooseOutPut(TabPage):
    """ for user to choose output directory  """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.outPath = None
        self._iniWidget()
        self._initLayout()
        
    def _iniWidget(self):
        self.chooseDirBtn = ColoredBtn("...", Color.BLUEMEDIUM, FontSize.HEADER2)
        self.chooseDirBtn.setFixedWidth(70)
        self.dirPathText = QLineEdit(self)
        self.dirPathText.setPlaceholderText("Choose Output Directory")
        self.dirPathText.setMinimumHeight(40)
        self.dirPathText.setReadOnly(True)
        self.chooseDirBtn.clicked.connect(self._addDir)
        
    def _initLayout(self):
        self.layout = QHBoxLayout()
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




        
'''
File: SourceTable.py
Project: GailBot GUI
File Created: 2023/04/01
Author: Siara Small  & Vivian Li
-----
Last Modified:2023/05/13
Modified By:  Siara Small  & Vivian Li
-----
Description: implementation of the source table which is used on pages that 
             display files uploaded by user
'''
# stdlib import
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple
from enum import Enum 

# internal import
from view.signal.Request import Request
from view.signal.interface import DataSignal
from view.components.SettingDetail import ProfileDetail
from view.widgets.MsgBox import WarnBox
from view.widgets.Table import BaseTable
from view.widgets.Button import ColoredBtn, TableBtn
from view.widgets.Background import initSecondaryColorBackground
from ..FileUpload import UploadFileDialog, ChooseSetTab
from ...config.Style import STYLE_DATA
from ...config.Text import FILE_TABLE as Text
from view.util.ErrorMsg import ERR
from gbLogger import makeLogger
from PyQt6.QtWidgets import (
    QTableWidgetItem, 
    QWidget, 
    QCheckBox,
    QVBoxLayout, 
    QHBoxLayout,
    QDialog
)

from PyQt6.QtCore import (
    QObject, 
    Qt, 
    QSize, 
    pyqtSignal,
)
from PyQt6.QtGui import QColor

class Signals(QObject):
    """signals for controlling frontend view changes """
    nonZeroFile   = pyqtSignal()     # emit when any file is selected by user
    ZeroFile      = pyqtSignal()     # emit when no file is selected by user
    select        = pyqtSignal(str)  # emit a single contains the selected file
    unselect      = pyqtSignal(str)  # emit a signal contains the unselected file 
    transferState = pyqtSignal(list) # emit a signal contains a list of file to oe transferred to another state

class TableWidget(Enum):
    # an enum class that stores a list of available widget button 
    # to be added to the source table
    REMOVE = 1
    CHANGE_PROFILE = 2 
    PROFILE_DETAIL = 3
    CHECK = 4
    VIEW_OUTPUT = 5

@dataclass
class DATA_FIELD: 
    # a data class that stores the key
    # in a source dictionary 
    NAME     = "Name"
    TYPE     = "Type"
    PROFILE  = "Profile"
    STATUS   = "Status"
    DATE     = "Date"
    OUTPUT   = "Output"
    FULLPATH = "FullPath"
    PROGRESS = "Progress"


class SourceTable(BaseTable):
    def __init__(self, 
                 headers, 
                 signal, 
                 dataKeyToCol: Dict[str, int],
                 appliedCellWidget: Set[TableWidget], *args, **kwargs):
        self.signal = signal 
        self.dataKeyToCol = dataKeyToCol
        self.tableWidth = STYLE_DATA.Dimension.TABLEWIDTH
        self.tableHeight = STYLE_DATA.Dimension.TABLEMINHEIGHT
        self.nameAtFstColumn = False
        super().__init__(headers, *args, **kwargs)
        self.profiles = []
        self.nameToData = dict()
        self.actionWidgetCol = len(self.headers) - 1
        self.selected : Set[str] = set()
        self.allSelected = False 
        self.appliedCellWidget = appliedCellWidget
        self.signal  = signal 
        self.viewSignal = Signals()
        self.selectWidgets : Dict[str, QCheckBox] = dict()
        self.horizontalHeader().sectionClicked.connect(
            self._headerClickedHandler
        )
    
    ########################  table initializer    #########################
    def initProfiles(self, profiles: List[str]):
        """ initialize the available profiles """
        self.profiles = profiles
    
    def addProfile(self, profileName:str)->None:
        """ add profile, called whenever new profile is added by the user  
        """
        self.profiles.append(profileName)
        
    def deleteProfile(self, profileName:str)->None:
        """ delete profile, called whenever a profile is deleted by the user 
        """
        try: 
            self.profiles.remove(profileName)
        except Exception as e:
            self.logger.error(e, exc_info=e)
         
    ######################  handling selecting file  #####################
    def _headerClickedHandler(self, idx):
        """ handle header clicked signal  """
        try:
            if idx == 0:
                self._toggleAllSelect()
        except Exception as e:
            WarnBox(ERR.ERR_WHEN_DUETO("select all files", e))       
   
    def _toggleAllSelect(self, clear = False):
        """ select or unselect all items in the table """
        if self.allSelected or clear:
            for widget in self.selectWidgets.values():
                widget.setCheckState(Qt.CheckState.Unchecked)
        else:
            for widget in self.selectWidgets.values():
                widget.setCheckState(Qt.CheckState.Checked)
        self.allSelected = not self.allSelected
    
    def addToSelected(self, name:str) -> None:
        """ add the file to transcribe list

        Args:
            name (str): the name to identify the file
        """
        self.logger.info(name)
        self.logger.info(self.selected)
        try:
            if name in self.nameToTablePins:
                self.selected.add(name)
                rowIdx = self.indexFromItem(self.nameToTablePins[name]).row()
                self._setColorRow(rowIdx, STYLE_DATA.Color.HIGHLIGHT)
                self.viewSignal.nonZeroFile.emit()
            else: 
                raise Exception("File is not found in the data")
        except Exception as err:
            self.logger.error(err)
        else:
            return
             
    def removeFromSelected(self, name:str) -> None:
        """ remove the file from the transcribe list 

        Args:
            name (str): the name that identifies the file to be removed
        """
        self.logger.info(name)
        self.logger.info(self.selected)
        try:
            if name in self.selected:
                self.selected.remove(name)
                rowIdx = self.indexFromItem(self.nameToTablePins[name]).row()
                self._setColorRow(rowIdx, STYLE_DATA.Color.MAIN_BACKGROUND)
                self.clearSelection()
                if len(self.selected) == 0:
                    self.viewSignal.ZeroFile.emit()
            else:
                raise Exception("File is not added to transcribe list")
        except Exception as err:
            self.logger.error(err)
        else:
            return
         
    def _setColorRow(self, rowIdx, color):
        """ change the color of the row at rowIdx """
        self.logger.info(self.rowAt(rowIdx))
        for i in range(self.columnCount()):
            if self.item(rowIdx, i):
                self.item(rowIdx, i).setBackground(QColor(color))
            else:
                self.logger.info("failed to set row color")
   
    def getSelectedFile(self) -> List[Tuple[str, Dict[str, str]]]:
        """ return a list of file selected by the user

        Returns:
            List[Tuple[str, Dict[str, str]]]: a list of tuple of the form 
            (filename:str, filedata:Dict) 
        """
        data = list ()
        for file in self.selected:
            data.append((file, self.nameToData[file]))
        return data 
     
    def getAllFile(self) -> List[Tuple[str, Dict[str, str]]]:
        """get all the file uploaded by the user

        Returns:
            List[Tuple[str, Dict[str, str]]]: a list of tuple of the form 
            (filename:str, filedata:Dict) 
        """
        data = [(name, filedata) for name, filedata in self.nameToData.items()]
        return data 
      
    ########################  add source handler     #########################
    def uploadFile(self):
        """ open up a pop up dialog for user to upload file 
           ** connected to upload file button 
        
        """
        try:
            addFileWindow = UploadFileDialog(self.profiles)
            addFileWindow.signals.postFile.connect(self._postFile)
            addFileWindow.exec()
        except Exception as e:
            self.logger.error(e, exc_info=e) 
            WarnBox("An error occurred when uploading the file")
    
    def _postFile(self, file):
        """ send signals to post file to the database 
        """
        self.signal.postRequest.emit(Request(data=file, succeed=self.addItem))
    
    def resetFileDisplay(self, files: List[Tuple]):
        """ clear all previously displayed file on the table  and only display 
            the list of files passed by caller

        Args:
            files (List[Tuple]): a list of tuple that stores the file data and 
                                 file names
        """
        self.setRowCount(0)
        self.nameToTablePins = dict()
        self.nameToData = dict()
        self.addItems(files)
        
    def addItem(self, source: Tuple[str, Dict[str, str]], **kwargs):
        """add item to the table 

        Args:
            source (Tuple[str, Dict[str, str]]): a Tuple with the form 
            (filename: str, filedata: Dict)
        """
        super().addItem(source, **kwargs)
        name, data = source
        self.nameToData[name] = data 
      
   
    ######################### add cell widget ###########################
    def addCellWidgets(self, name: str, row: int):
        """add cell widget 

        Args:
            name (str): the name of the file 
            row (int): the initial row of the file 
        """
        if TableWidget.CHECK in self.appliedCellWidget:
            checkBox = self.getCheckBox(name)
            self.setCellWidget(row, 0, checkBox)
        cellWidget = QWidget()
        layout     = QHBoxLayout()
        cellWidget.setLayout(layout)
        
        if TableWidget.REMOVE in self.appliedCellWidget:
            layout.addWidget(self.getRemoveBtn(name))
            
        if TableWidget.VIEW_OUTPUT in self.appliedCellWidget:
            self.logger.info("view output widget added")
            layout.addWidget(self.getViewOutputBtn(name))
            
        if TableWidget.PROFILE_DETAIL in self.appliedCellWidget:
            layout.addWidget(self.getViewProfileBtn(name))
            
        if TableWidget.CHANGE_PROFILE in self.appliedCellWidget:
            layout.addWidget(self.getChangeProfileBtn(name))
        lastTableCell = QTableWidgetItem()
        self.setItem(row, self.actionWidgetCol, lastTableCell)
        self.setCellWidget(row, self.actionWidgetCol, cellWidget)

    def getCheckBox(self, sourceName) -> QWidget:
        """return a checkbox with connected signal

        Args:
            sourceName (str): the name of the file

        Returns:
            QWidget: a checkBox widget
        """
        container = QWidget()
        layout = QVBoxLayout()
        container.setLayout(layout)
        checkBox = QCheckBox()
        layout.addWidget(checkBox, alignment = Qt.AlignmentFlag.AlignHCenter)
        checkBox.stateChanged.connect(
            lambda state: self.addToSelected(sourceName)
                          if state else self.removeFromSelected(sourceName))
        self.selectWidgets[sourceName] = checkBox
        return container
    
    def getViewProfileBtn(self, name) -> QWidget:
        """get a button with connected signal when clicking open up the 
           profile information of the added file 

        Args:
            name (str): the name of the file

        Returns:
            QWidget: the button widget 
        """
        btn = TableBtn(icon=STYLE_DATA.Asset.tableDetail)
        btn.clicked.connect(
            lambda:self.fileProfileRequest(name)
        )
        return btn
        
    def getChangeProfileBtn(self, name) -> QWidget:
        """ get a button with connected signal when clicking open up 
            a dialog to change the file profile and update the changes in 
            backend

        Args:
            name (str): the name of the file

        Returns:
            QWidget: the button widget
        """
        btn = TableBtn(icon=STYLE_DATA.Asset.tableEdit) 
        btn.clicked.connect(
            lambda: self.changeProfileRequest(name)
        )
        return btn

####################### function for button click action ####################
    def changeProfileRequest(self, name):
        """ open up a dialog to allow user to change the file profile

        Args:
            name (str): the name of the file 
        """
        dialog = _ChangeProfileDialog(
            self.profiles, 
            name, 
            self.signal, 
            succeed=self.changeProfileSucceed, parent=self)
        dialog.exec()
   
    def changeProfileSucceed(self, result: Tuple[str, str]):
        """succeed continuation of the profile change, update the file's
           profile information on the frontend interface

        """
        try:
            name, profilekey = result
            if name in self.nameToTablePins:
                row = self.indexFromItem(self.nameToTablePins[name]).row()
                newitem = QTableWidgetItem(profilekey)
                newitem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setItem(row, self.dataKeyToCol["Profile"], newitem)
                if name in self.selected: 
                    newitem.setBackground(QColor(STYLE_DATA.Color.HIGHLIGHT))
            else:
                WarnBox(ERR.ERR_WHEN_DUETO.format("Update profile", "cannot find file name"))
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("adding new profile option", str(e)))
    
    def fileProfileRequest(self, name):
        """send a request to get the file's profile data

        Args:
            name (str): the name of the file
        """
        self.signal.fileProfileRequest.emit(
            Request(data=name, succeed=self.displayDetail)
        )
        
    def displayDetail(self, data):
        """succeed continuation of the request to view profile details

        Args:
            data (Dict): the data to be displayed
        """
        name, setting = data 
        try:
            ProfileDetail(name, setting) 
        except Exception as e:
            self.logger.error(e, exc_info=e)
   
    def deleteSucceed(self, name):
        """succeed continuation for removing a file from the table 

        Args:
            name (str): the name of the file
        """
        super().deleteSucceed(name)
        if name in self.selected:
            self.selected.remove(name)
        del self.nameToData[name]
        del self.selectWidgets[name]
       
    def deleteAll(self):
        """
        Delete all the files on the table 
        """
        for name in self.nameToTablePins.keys():
            self.delete(name, withConfirm=False)

############################## for editing source data #######################
    def changeFileToTranscribed(self, name:str):
        """ change one file's status to be transcribed, and delete the file
            from the file table

        Args:
            name (str): a file name that identifies the file
        """
        try:
            if name in self.nameToTablePins:
                self.updateFileContent((name, DATA_FIELD.STATUS, Text.COMPLETE))
            else:
                WarnBox(ERR.ERR_WHEN_DUETO.format("updating file status", "file name cannot be found"))
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("updating file status", str(e)))
        
    def showOneFileProgress(self, progress: Tuple[str, str]):
        """update the transcription progress of one file

        Args:
            progress (Tuple[str, str]): the Tuple stores the file key and the 
            progress message
        """     
        name, msg = progress
        self.logger.info(f"receiver progress message for file {name} {msg}")
        try:
            self.updateFileContent((name, DATA_FIELD.PROGRESS, msg))
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("updating file progress", str(e)))

    def updateFileContent(self, file: Tuple[str, str, str]):
        """ update the file content on the table

        Args:
            file (Tuple[key, field, value]): 
        """
        self.logger.info(f"get updated information {file}")
        key, field, value = file 
        self.logger.info(self.nameToTablePins)
        if key in self.nameToTablePins:
            if field in self.headers:
                row = self.indexFromItem(self.nameToTablePins[key]).row()
                col = self.dataKeyToCol[field] 
                newitem = QTableWidgetItem(value)
                self.setItem(row, col, newitem)
                if key in self.selected:
                    newitem.setBackground(STYLE_DATA.Color.HIGHLIGHT)
        else:
            self.logger.error("File is not found")

##################### for editing file profile ##############################
class _ChangeProfileDialog(QDialog):
    def __init__(self, 
                 profiles: List[str], 
                 fileKey:str, 
                 signal:DataSignal,
                 succeed: callable,
                 *args, 
                 **kwargs) -> None:
        """ open up a dialog for user to change the profile for the file

        Args:
            profiles (List[str]):  a list of profile keys
            fileKey (str): the file name for which its profile will be changed
        """
        super().__init__(*args, **kwargs)
        self.signals = signal
        self.succeed = succeed
        self.logger = makeLogger()
        self.fileKey = fileKey
        self.selectSetting = ChooseSetTab(profiles)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.confirmBtn = ColoredBtn("Confirm", STYLE_DATA.Color.PRIMARY_BUTTON)
        self.layout.addWidget(self.selectSetting)
        self.layout.addWidget(self.confirmBtn, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.confirmBtn.clicked.connect(
            self.updateProfile)
        initSecondaryColorBackground(self)
        self.setFixedSize(QSize(450, 300))
    
    def updateProfile(self):
        """ send a signal to update the profile in the database
        """
        self.logger.info("update signal send")
        newSetting = self.selectSetting.getProfile()["Profile"]
        self.logger.info((self.fileKey, newSetting))
        self.signals.changeFileProfileRequest.emit(
            Request(data =(self.fileKey,newSetting), succeed=self.succeed))
        self.close()
    
'''
File: TableWidgets.py
Project: GailBot GUI
File Created: Friday, 14th October 2022 7:24:24 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Saturday, 15th October 2022 10:43:45 am
Modified By:  Siara Small  & Vivian Li
-----
'''


# from view.widgets import (Label, Button)
# from view.style.styleValues import Color, FontFamily, FontSize

import logging

from typing import Dict, List, Set, TypedDict, Tuple

from view.widgets.FileTab import ChooseFileTab
from view.widgets.TabPages import ChooseSet

from PyQt6.QtWidgets import (
    QTableWidget, 
    QTableWidgetItem, 
    QWidget, 
    QAbstractItemView,
    QHeaderView,
    QCheckBox,
    QPushButton,
    QVBoxLayout, 
    QHBoxLayout, 
    QDialog
)

from PyQt6.QtCore import QObject, Qt, QSize, pyqtSignal
from PyQt6.QtGui import QColor

class fileObject(TypedDict):
    Name: str
    Type: str
    Profile: str
    Status: str
    Date: str
    Size: int
    Output: str
    FullPath: str
    
class DisplayFile(QObject):
    def __init__(
        self, 
        table: QTableWidget,
        pin: QTableWidgetItem, 
        key: str,
        deleteFun:callable, 
        setFun:callable, 
        selectFun:callable, 
        unselectFun:callable, 
        gosetFun:callable,
        *args, 
        **kwargs):
        """ A wrapper class that contains all widgets in one row of filetable

        Args:
            table (QTableWidget): the parent table of the widget
            pin (QTableWidgetItem): used to pin the position of the 
                                    file on the table
            key (str): a key that identify the file in the data 
            deleteFun (callable): function to delete the file
            setFun (callable): function to change 
            selectFun (callable): function to select the file
            unselectFun (callable): function to unselect the file
            gosetFun:callable: function to view the setting
        """
        super().__init__(*args, **kwargs)
        self.pin = pin
        self.key = key
        self.table = table
        self.selectFun = selectFun
        self.unselectFun = unselectFun
        self.gosetFule = gosetFun
        self.checkBox = QCheckBox()
        self.Action = QWidget()
        self.ActionLayout = QVBoxLayout()
        self.Action.setLayout(self.ActionLayout)
        self.deleteBtn = QPushButton("Delete")
        self.setBtn = QPushButton("Change Setting")
        self.profileBtn = QPushButton("Profile Details")
        
        self.ActionLayout.addWidget(self.deleteBtn)
        self.ActionLayout.addWidget(self.setBtn)
        self.ActionLayout.addWidget(self.profileBtn)
        self.ActionLayout.setSpacing(1)
        self.ActionLayout.addStretch()
        self.deleteBtn.clicked.connect(lambda: deleteFun(self.pin, self.key))
        self.setBtn.clicked.connect(lambda: setFun(self.key))
        self.profileBtn.clicked.connect(lambda: gosetFun(self.key))
        self.checkBox.stateChanged.connect(self.checkStateChanged)
    
    def checkStateChanged(self, state:bool):
        if state:
            self.selectFun(self.key)
        else:
            self.unselectFun(self.key)
            
    def setCheckState(self, state):
        if state:
            self.checkBox.setCheckState(Qt.CheckState.Checked)
        else: 
            self.checkBox.setCheckState(Qt.CheckState.Unchecked)
            
    def addWidgetToTable(self, row, rowWidgets: Set[str]):
        if "select" in rowWidgets:
            self.table.setCellWidget(row, 0, self.checkBox)
        if "setting" in rowWidgets or "delete" in rowWidgets:
            self.table.setCellWidget(row, self.table.columnCount()- 1, self.Action)
        if "delete" not in rowWidgets:
            self.deleteBtn.hide()
            self.setBtn.hide()
        if "setting" not in rowWidgets:
            self.profileBtn.hide()
 
        
class Signals(QObject):
    goSetting = pyqtSignal(str)
    changeSetting = pyqtSignal(list)


class changeProfileDialog(QDialog):
    def __init__(self, settings: List[str], fileKey:str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.signals = Signals()
        self.fileKey = fileKey
        self.selectSetting = ChooseSet(settings)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.selectSetting)
        self.selectSetting.confirmBtn.clicked.connect(self.updateProfile)
        self.setFixedSize(QSize(200, 200))
    
    def updateProfile(self):
        print("update signal send")
        newSetting = self.selectSetting.getProfile()["Profile"]
        print([self.fileKey, newSetting])
        self.signals.changeSetting.emit([self.fileKey,newSetting])
        self.close()
    
class FileTable(QTableWidget):
    def __init__(self, 
                 headers: List[str], 
                 filedata: Dict[str, fileObject], 
                 rowWidgets: Set[str]  = {"delete", "setting", "select"},
                 settings: List[str] = ["default"],  
                 *args, 
                 **kwargs):
        """_summary_

        Args:
            headers (List[str]): list of headers 
            filedata (Dict[str, fileObject]): initial file data
        """
        super().__init__(0, (len(headers)), *args, **kwargs)
        
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.headers = headers          # stores the file header, 
                                        # dictate what data in file data will 
                                        # be displayed on the table
        
        self.filedata = filedata        # stores the file data
        self.settings = settings
        self.pinFileData = dict()       # used to track file's position on 
                                        # table by pin
        self.transcribeList: List[str] = []   
                                        # a list of keys of the file that will
                                        #  be transcribed, 
                                   
        self.fileWidgets: Dict[str, DisplayFile] = dict()      
                                        # a dictionary to keep track of current
                                        # widget on the table 
       
        self.allSelected = False        # True of all files are selected 
        
        self.nextkey = len(self.filedata) + 1  
                                        # the key of the next added file
        
        self.rowWidgets = rowWidgets
        
        self.signals = Signals()
    
        self._initializeTable()
    
    def resizeCol(self, widths:List[int]) -> None:
        """ takes in a list of width and resize the width of the each 
            column to the width
        """
        if len(widths) != self.columnCount():
            logging.error("cannot resize column")
        else:
            for i in range(len(widths)):
                self.setColumnWidth(i, widths[i])
    
    def clearAll(self):
        self.clearContents()
        for i in range(self.rowCount()):
            self.removeRow(i)
    
    def addFilesToTable(self, fileData: Dict[str, fileObject])->None:
        """ take fileData with multiple files and add to the table
        """
        self.clearContents()
        for key, item in fileData.items():
            self._addFiletoTable(item, key)
            self.filedata[key] = item
        self.resizeRowsToContents()          
        
    
    def _initializeTable(self) -> None:
        """ Initialize the table """
        self._setFileHeader()     # set file header 
        self._setFileData()                   # set initial file data
        self._initStyle()
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)   # TODO: set the selection color of the file table 
        
        
    def _initStyle(self) -> None:
        self.horizontalHeader().setFixedHeight(45)
        for i in range(self.columnCount()):
            self.horizontalHeader().setSectionResizeMode(i,QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setStyleSheet("font-size:14px;")
        self.setStyleSheet("selection-background-color: #f0f9f6;"
                           "selection-color:black")  # TODO: change to color to var
        self.verticalHeader().setStyleSheet("background-color: #f0f9f6 ")
        self.setFixedWidth(900)
        self.setMaximumHeight(300)
        
    def _setFileHeader(self) -> None:
        """ initialize file headers
        
        Args: 
            headers: (List[str]) a list of header names
        """
        for i in range(len(self.headers)):
            headerItem = QTableWidgetItem(self.headers[i])
            self.setHorizontalHeaderItem(i, headerItem)
        self.horizontalHeader().sectionClicked.connect(self._headerClickedHandler)
    
    
    def _setFileData(self):
        """ display initial file data on to the table """
        for key, item in self.filedata.items():
            self._addFiletoTable(item,key)
    
    def _headerClickedHandler(self, idx):
        """ handle header clicked signal  """
        if idx == 0:
            self._toggleAllSelect()
   
    def _toggleAllSelect(self):
        """ select or unselect all items in the table """
        if self.allSelected:
            for key,widget in self.fileWidgets.items():
                widget.setCheckState(False)
                if key in self.transcribeList:
                    self.transcribeList.remove(key) 
        else:
            for key,widget in self.fileWidgets.items():
                widget.setCheckState(True)
                if not key in self.transcribeList:
                    self.transcribeList.append(key)
        
        self.allSelected = not self.allSelected
    
    def getFile(self):
        addFileWindow = ChooseFileTab(self.settings)
        addFileWindow.signals.sendFile.connect(self._addFile)
        addFileWindow.exec()
        
        
    def _addFile(self, file: dict):
        """ Add a file 
        """
        """ call a module to open add file dialog """
        """ store the file data in self.data """
        """ add file meta data to table """
        
        """ add file widget to table """
        try:
            self._addFiletoData(file, f"{self.nextkey}")
            self._addFiletoTable(file, f"{self.nextkey}")
        except:  
            logging.error("cannot add file to data")
        else:
            self.nextkey += 1 
            logging.info("file added successfully")
        
    def _addFiletoData(self, file: fileObject, key:str):
        """ add one file to the file data """
        self.filedata[key] = file
    
    def _addFiletoTable(self, file: dict, key:str):
        """ display one file on the  table"""
        newRowIdx = self.rowCount()
        self.insertRow(newRowIdx)
        for col in range(len(self.headers)):
            if self.headers[col] in file.keys():
                newItem = QTableWidgetItem(str(file[self.headers[col]]))
                if col == 1: 
                    filePin = newItem
                    self.pinFileData[key] = filePin
                self.setItem(newRowIdx, col, newItem)
        
        
        self._addFileWidgetToTable(filePin, newRowIdx, key)
        self.resizeRowsToContents()          
                
    def _addFileWidgetToTable(self, pin: QTableWidgetItem, row:int, key:str):
        """ Add the widget that manipulates each file in a certain row 
            to the table
    
        Args:
            pin (QTableWidgetItem): _description_
        """
        newFileWidget = DisplayFile( 
                            self,
                            pin, 
                            key,
                            self.deleteFile, 
                            self.changeSetting, 
                            self.addToTranscribe, 
                            self.removeFromTranscribe,
                            self.settingDetails)
        
        newFileWidget.addWidgetToTable(row, self.rowWidgets)
        self.fileWidgets[key] = newFileWidget
         
    def deleteFile(self, pin: QTableWidgetItem, key):
        """ delete a file from the table

        Args:
            pin (QTableWidgetItem): a pin to identify file on the table
            key (_type_): file key in database
        """
        print("Try to delete")
        rowIdx = self.indexFromItem(pin).row()
        if rowIdx >= 0:
            self.removeRow(rowIdx)
            del self.fileWidgets[key]
        if key in self.transcribeList:
            self.transcribeList.remove(key)

    def addToTranscribe(self, key:str) -> None:
        """ add the file to transcribe list

        Args:
            key (str): the key to identify the file
        """
        try:
            if key in self.filedata:
                self.transcribeList.append(key)
            else: 
                raise Exception("file is not found in the data")
        except Exception as err:
            logging.error(err)
        else:
            return
        
            
    def removeFromTranscribe(self, key:str) -> None:
        """ remove the file from the transcribe list 

        Args:
            key (str): the key to identify the file 
        """
        try:
            if key in self.transcribeList:
                self.transcribeList.remove(key)
            else:
                raise Exception("file is not added to transcribe list")
        except Exception as err:
            logging.error(err)
        else:
            return
        
            
    def transcribe(self) -> Dict[str, fileObject]:
        """ 
        redirect to the transcribe page and transcribe all the selected 
        file
        """
        transcribeData = dict()
        for i in self.transcribeList:
            fileData = {**self.filedata[i], 
                        **{"Selected Action": "Transcribe"}, 
                        **{"Action in Progress":"Transcribing"}}
            transcribeData[i] = fileData
        
        return transcribeData
       
        
    def changeSetting(self, key:str) -> None:
        """ configure the setting of one file identified by key

        Args:
            key (str): a key to identify file
        """
        selectSetting = changeProfileDialog(self.settings, key)
        selectSetting.signals.changeSetting.connect(self.updateSetting)
        selectSetting.exec()
        selectSetting.setFixedSize(QSize(200,200))
    
    def settingDetails(self, key:str)->None:
        print(key)
        print(self.filedata)
        if key in self.filedata:
            self.signals.goSetting.emit(self.filedata[key]["Profile"])
    
    def updateSetting(self, newSetting:List[str]) -> None:
        # logging.DEBUG(newSetting)
        # print("we get the new setting", newSetting)
        print("we reached the update seting")
        self.filedata[newSetting[0]]["Profile"] = newSetting[1]
        rowIdx = self.indexFromItem(self.pinFileData[newSetting[0]]).row()
        newSettingText = QTableWidgetItem(newSetting[1])
        self.setItem(rowIdx, 3, newSettingText)
        
            
            
    
MainTableHeader = ["Select All", 
                  "Type", 
                  "Name", 
                  "Profile", 
                  "Status", 
                  "Date", 
                  "Size", 
                  "Actions"]
MainTableDimension = [70,70,140,140,140,70,80,175]


ConfirmHeader = ["Type",
                 "Name",
                 "Profile",
                 "Selected Action", 
                 " "]
ConfirmHeaderDimension = [85,300,200,130,170]

ProgressHeader = ["Type",
                  "Name",
                  "Action in Progress"]

ProgressDimension = [170, 450, 265]

SuccessHeader = ["Type",
                 "Name",
                 "Status",
                 "Output"]
SuccessDimension = [120, 300, 250, 215]
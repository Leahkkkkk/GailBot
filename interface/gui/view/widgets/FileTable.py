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

""" TODO: add function to change data on the table by cell; 
    TODO: change transribe status, pass a file key and change the transcribe status
    TODO: change the type value to be displayed as icons 
    TODO: pop up window for setting details
    TODO: file summary section 
    TODO: set sorting icon 
    TODO: **sorting function
    TODO: **searching function 
    TODO: **
"""
KEYERROR = "File key not found"
# from view.widgets import (Label, Button)
# from view.style.styleValues import Color, FontFamily, FontSize
from typing import Dict, List, Set, Tuple, TypedDict
import logging

from view.components.ChooseFileTab import ChooseFileTab
from view.pages.FileUploadTabPages import ChooseSet
from view.style.styleValues import Color
from view.style.Background import initBackground
from util import Path
from util.Logger import makeLogger
from view.Signals import FileSignals

from PyQt6.QtWidgets import (
    QTableWidget, 
    QTableWidgetItem, 
    QWidget, 
    QAbstractItemView,
    QHeaderView,
    QCheckBox,
    QPushButton,
    QVBoxLayout, 
    QDialog
)

from PyQt6.QtCore import QObject, Qt, QSize, pyqtSignal
from PyQt6.QtGui import QColor, QIcon

logger = makeLogger("Frontend")

class fileObject(TypedDict):
    Name: str
    Type: str
    Profile: str
    Status: str
    Date: str
    Size: str
    Output: str
    FullPath: str
    
class Signals(QObject):
    goSetting = pyqtSignal()
    changeSetting = pyqtSignal(tuple)
    transferState = pyqtSignal(list)
    nonZeroFile = pyqtSignal()
    ZeroFile = pyqtSignal()

    error = pyqtSignal(str)


class FileTable(QTableWidget):
    """ TODO: update setting keys """
    def __init__(self, 
                 headers: List[str], 
                 dbSignal: FileSignals,
                 settings: List[str] = ["default"],  
                 rowWidgets: Set[str]  = {"delete", "setting", "select"}, 
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
        self.settings = settings        # TODO: delete eventually 
        
        self.filePins = dict()       # used to track file's position on 
                                        # table by pin
                                        
        self.transferList: set[str] = set()  
                                        # a list of keys of the file that will
                                        #  be transferred to the next state, 
                                   
        self.fileWidgets: Dict[str, TableCellButtons] = dict()      
                                        # a dictionary to keep track of current
                                        # widget on the table 
       
        self.allSelected = False        # True of all files are selected 
        
        
        self.rowWidgets = rowWidgets
        
        self.signals = Signals()
        self.dbSignal = dbSignal
        self.setMidLineWidth(500)
        self.setMaximumWidth(1000)
    
        self._initializeTable()
    
    def uploadFile(self):
        """ open up a pop up dialog for user to upload file 
           ** connected to upload file button 
        
        """
        addFileWindow = ChooseFileTab(self.settings)
        addFileWindow.signals.postFile.connect(self.postFile)
        addFileWindow.exec()
    
    def postFile(self, file: fileObject):
        """ send signals to post file to the database 
            ** connected to the upload file button TODO
        """
        self.dbSignal.postFile.emit(file)
        
    def addFile(self, file: Tuple[str, fileObject]):
        """ given a file object, adding it to the file table
            
        Args:
            file (Tuple[key, fileObject]): a file object
        """
        logger.info(file[0])
        logger.info(file[1])
        key, data = file
        newRowIdx = self.rowCount()
        self.insertRow(newRowIdx)
        for col in range(len(self.headers)):
            if self.headers[col] in data.keys():
                newItem = QTableWidgetItem(str(data[self.headers[col]]))
                if col == 1: 
                    filePin = newItem
                    self.filePins[key] = filePin
                self.setItem(newRowIdx, col, newItem)
        
        self._addFileWidgetToTable(newRowIdx, key) #TODO:improve addwidget
        self.resizeRowsToContents()  
     
    def addFiles(self, files: List[Tuple]):
        """ adding a list of files to file table

        Args:
            files (List[Tuple]): _description_
        """
        for file in files:
            self.addFile(file)
   
    def deleteFile(self, key:str):
        """ delete one file
            ** connected to delete file button 
        Args:
            key (str): _description_
        """
        if key in self.filePins:
            rowIdx = self.indexFromItem(self.filePins[key]).row()
            self.removeRow(rowIdx)
            self.dbSignal.delete.emit(key)
            if key in self.transferList:
                self.transferList.remove(key)
        else:
            self.signals.error(KEYERROR)
    
    def deleteAll(self):
        """ delete all files on the file table 
            ** connected to deleteAll button 
        """
        for key in self.filePins.keys():
            self.deleteFile(key)
            
        self.transferList.clear()
        self.filePins.clear()

    def settingDetails(self, key:str):
        """ send a reqeust to see file details
            *** connected to setting details page
        Args: ket(str): a file key 
        """
        self.dbSignal.requestprofile.emit(key) # make request to load profile data 
        self.signals.goSetting.emit() # go to the profile page
        
    def changeFileToTranscribed(self, key:str):
        """ change one file's status to be transcribed 

        Args:
            key (str): a file key that identifies the file
        """
        self.dbSignal.changeStatus((key, "Transcribed")) 
        if key in self.filePins:
            row = self.indexFromItem(self.filePins[key]).row()
            newitem = QTableWidgetItem("Transcribed")
            self.setItem(row, 4, newitem)
        else:
            self.signals.error.emit(KEYERROR)
    
    def changeSetting(self, key:str):
        """ open a pop up for user to change file setting 
            ** connected to changesetting button 
        Args:
            key (str): a key to identify file
        """
        selectSetting = changeProfileDialog(self.settings, key)
        selectSetting.signals.changeSetting.connect(self.postNewFileProfile)
        selectSetting.exec()
        selectSetting.setFixedSize(QSize(200,200))
    
    def postNewFileProfile(self, newprofile: Tuple[str, str]):
        """ post the newly updated file change to the dataabse

        """
        key, profilekey = newprofile
        self.dbSignal.changeProfile.emit(newprofile) 
        if key in self.filePins:
            row = self.indexFromItem(self.filePins[key]).row()
            newitem = QTableWidgetItem(profilekey)
            self.setItem(row, 3, newitem)
        else:
            self.signals.error.emit(KEYERROR)

    def addProfile(self, profileName:str)->None:
        """ add profile keys 
        """
        self.settings.append(profileName)
    
    def filterFile(self, files: Set[str]):
        """ given a set of file keys, the table will only show the file that 
            is in the list 
        
        Args:
            files (List[str]) a list of file keys
        """
        logging.info("filter")
        logging.info(len(self.filePins))
        self.transferList.clear()
        for key, pin in self.filePins.items():
            rowidx = self.indexFromItem(pin).row()
            if key in files:
                self.showRow(rowidx)
                self.transferList.add(key)
            else:
                self.hideRow(rowidx)
    
    def transcribeFile(self):
        self.dbSignal.transcribe.emit(self.transferList)  
        
        
        
    """ """ """ """ """ functuion for styling   """ """ """ """ """
    def resizeCol(self, widths:List[int]) -> None:
        """ takes in a list of width and resize the width of the each 
            column to the width
        """
        widthSum = self.width()
        if len(widths) != self.columnCount():
            logger.error("cannot resize column")
        else:
            for i in range(len(widths)):
                self.setColumnWidth(i, widths[i] * widthSum)
    
    
    def _setColorRow(self, rowIdx, color):
        """ change the color of the row at rowIdx """
        logger.info(self.rowAt(rowIdx))
        for i in range(self.columnCount()):
            if self.item(rowIdx, i):
                self.item(rowIdx, i).setBackground(QColor(color))
            else:
                logger.info("cannot set row color")

    
    def addToNextState(self, key:str) -> None:
        """ add the file to transcribe list

        Args:
            key (str): the key to identify the file
        """
        logger.info(key)
        logger.info(self.transferList)
        try:
            if key in self.filePins:
                self.transferList.add(key)
                rowIdx = self.indexFromItem(self.filePins[key]).row()
                self._setColorRow(rowIdx, Color.BLUEWHITE)
                self.signals.nonZeroFile.emit()
                
            else: 
                raise Exception("file is not found in the data")
        except Exception as err:
            logger.error(err)
        else:
            return
        
            
    def removeFromNextState(self, key:str) -> None:
        """ remove the file from the transcribe list 

        Args:
            key (str): the key that identifies the file to be removed
        """
        logger.info(key)
        logger.info(self.transferList)
        try:
            if key in self.transferList:
                self.transferList.remove(key)
                rowIdx = self.indexFromItem(self.filePins[key]).row()
                self._setColorRow(rowIdx, "#fff")
                self.clearSelection()
                if len(self.transferList) == 0:
                    self.signals.ZeroFile.emit()
            else:
                raise Exception("file is not added to transcribe list")
        except Exception as err:
            logger.error(err)
        else:
            return
        
    def transferState(self) -> None:
        """ send a signal that includes all the files that will be transfered
            to the next state
        """
        logging.info(self.transferList)
        self.signals.transferState.emit(self.transferList)

        
    def _initializeTable(self) -> None:
        """ Initialize the table """
        self._setFileHeader()     # set file header 
        self._initStyle()
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)   # TODO: set the selection color of the file table 
       
    def _initStyle(self) -> None:
        """ Initialize the table style """
        self.horizontalHeader().setFixedHeight(45)
        for i in range(self.columnCount()):
            self.horizontalHeader().setSectionResizeMode(i,QHeaderView.ResizeMode.Fixed)
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
        self.verticalHeader().hide()
    
    def _headerClickedHandler(self, idx):
        """ handle header clicked signal  """
        if idx == 0:
            self._toggleAllSelect()
   
    def _toggleAllSelect(self, clear=False):
        """ select or unselect all items in the table """
        if self.allSelected or clear:
            for key,widget in self.fileWidgets.items():
                widget.setCheckState(False)
                if key in self.transferList:
                    self.transferList.remove(key) 
        else:
            for key,widget in self.fileWidgets.items():
                widget.setCheckState(True)
                if not key in self.transferList:
                    self.transferList.add(key)
        
        self.allSelected = not self.allSelected
    
            
    def _addFileWidgetToTable(self, row:int, key:str):
        """ Add the widget that manipulates each file in a certain row 
            to the table
    
        Args:
            pin (QTableWidgetItem): _description_
        """
        newFileWidget = TableCellButtons( 
                            self,
                            key,
                            self.deleteFile, 
                            self.changeSetting, 
                            self.addToNextState, 
                            self.removeFromNextState,
                            self.settingDetails)
        
        newFileWidget.addWidgetToTable(row, self.rowWidgets)
        self.fileWidgets[key] = newFileWidget
         
    
    def _resizeTable(self):
        logger.info("resized")
    
    def resizeEvent(self, e) -> None:
        self._resizeTable()
    
    
   

        
""" TODO: add responsive handling feature """            
MainTableHeader = ["Select All", 
                    "Type", 
                    "Name", 
                    "Profile", 
                    "Status", 
                    "Date", 
                    "Size", 
                    "Actions"]
MainTableDimension = [0.07,0.07,0.2,0.15,0.15,0.08,0.08,0.2]


ConfirmHeader = ["Type",
                 "Name",
                 "Profile",
                 "SelectedAction", 
                 " "]
ConfirmHeaderDimension = [0.1,0.35,0.25,0.13,0.17]

ProgressHeader = ["Type",
                  "Name",
                  "Progress"]
ProgressDimension = [0.2, 0.55, 0.25]

SuccessHeader = ["Type",
                 "Name",
                 "Status",
                 "Output"]
SuccessDimension = [0.17, 0.35, 0.25, 0.23]



class TableCellButtons(QObject):
    def __init__(
        self, 
        table: QTableWidget,
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
            key (str): a key that identify the file in the data 
            deleteFun (callable): function to delete the file
            setFun (callable): function to change 
            selectFun (callable): function to select the file
            unselectFun (callable): function to unselect the file
            gosetFun:callable: function to view the setting
        """
        super().__init__(*args, **kwargs)
        self.key = key  # to localize the flle on the actual data base 
        self.table = table
        self.selectFun = selectFun
        self.unselectFun = unselectFun
        self.gosetFule = gosetFun
        self.checkBoxContainer = QWidget()
        self.checkBoxLayout = QVBoxLayout()
        self.checkBoxContainer.setLayout(self.checkBoxLayout)
        self.checkBox = QCheckBox()
        self.checkBoxLayout.addWidget(
            self.checkBox, 
            alignment=Qt.AlignmentFlag.AlignCenter)
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
        self.deleteBtn.clicked.connect(lambda: deleteFun(self.key))
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
            firstCell = QTableWidgetItem()
            self.table.setItem(row, 0, firstCell, )
            self.table.setCellWidget(row, 0, self.checkBoxContainer)
        if "setting" in rowWidgets or "delete" in rowWidgets:
            lastCell = QTableWidgetItem()
            self.table.setItem(row,self.table.columnCount() - 1, lastCell)
            self.table.setCellWidget(row, self.table.columnCount() - 1, self.Action)
        if "delete" not in rowWidgets:
            self.deleteBtn.hide()
            self.setBtn.hide()
        if "setting" not in rowWidgets:
            self.profileBtn.hide()

class changeProfileDialog(QDialog):
    def __init__(self, settings: List[str], fileKey:str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.signals = Signals()
        self.fileKey = fileKey
        self.selectSetting = ChooseSet(settings)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.selectSetting)
        self.selectSetting.selectSettings.currentTextChanged.connect(self.updateProfile)
        initBackground(self, Color.BLUEWHITE)
        self.setFixedSize(QSize(450, 300))
    
    def updateProfile(self):
        logger.info("update signal send")
        newSetting = self.selectSetting.getProfile()["Profile"]
        logger.info((self.fileKey, newSetting))
        self.signals.changeSetting.emit((self.fileKey,newSetting))
        self.close()
    
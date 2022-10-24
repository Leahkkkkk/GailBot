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

# from view.widgets import (Label, Button)
# from view.style.styleValues import Color, FontFamily, FontSize
from typing import Dict, List, Set, TypedDict

from view.components.ChooseFileTab import ChooseFileTab
from view.pages.FileUploadTabPages import ChooseSet
from view.style.styleValues import Color
from view.style.Background import initBackground
from util import Path
from util.Logger import makeLogger

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
    goSetting = pyqtSignal(str)
    changeSetting = pyqtSignal(list)
    nonZeroFile = pyqtSignal()
    ZeroFile = pyqtSignal()
    sendFile = pyqtSignal(object)

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
        initBackground(self, Color.BLUEWHITE)
        self.setFixedSize(QSize(450, 300))
    
    def updateProfile(self):
        logger.info("update signal send")
        newSetting = self.selectSetting.getProfile()["Profile"]
        logger.info([self.fileKey, newSetting])
        self.signals.changeSetting.emit([self.fileKey,newSetting])
        self.close()
    
class FileTable(QTableWidget):
    """ TODO: update setting keys """
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
        self.transferList: List[str] = []   
                                        # a list of keys of the file that will
                                        #  be transferred to the next state, 
                                   
        self.fileWidgets: Dict[str, DisplayFile] = dict()      
                                        # a dictionary to keep track of current
                                        # widget on the table 
       
        self.allSelected = False        # True of all files are selected 
        
        self.nextkey = len(self.filedata) + 1  
                                        # the key of the next added file
        
        self.rowWidgets = rowWidgets
        
        self.signals = Signals()
        self.setMidLineWidth(500)
        self.setMaximumWidth(1000)
    
        self._initializeTable()
    
    
    def addProfileKeys(self, profileName:str)->None:
        self.settings.append(profileName)
        
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
    
    def clearAll(self):
        self.clearContents()
        for i in range(len(self.transferList)):
            del self.transferList[i]
        for i in range(self.rowCount()):
            self.removeRow(i)
        self.filedata.clear()
        logger.info(self.transferList)
    
    
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
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)   # TODO: set the selection color of the file table 
       
    def _initStyle(self) -> None:
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
            # code for using non-default icon
            # headerItem = QTableWidgetItem(QIcon(os.path.join(Path.getProjectRoot(), 
            #                                                  f"view/asset/sort.png")),
            #                               self.headers[i])
            headerItem = QTableWidgetItem(self.headers[i])
            self.setHorizontalHeaderItem(i, headerItem)
            # self.horizontalHeader().setSortIndicator(i, Qt.SortOrder.AscendingOrder)
                
        self.horizontalHeader().sectionClicked.connect(self._headerClickedHandler)
        self.verticalHeader().hide()
    
    def _setFileData(self):
        """ display initial file data on to the table """
        for key, item in self.filedata.items():
            self._addFiletoTable(item,key)
    
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
                    self.transferList.append(key)
        
        self.allSelected = not self.allSelected
    
    def changeToTranscribed(self, key):
        self.filedata[key]["Status"] = "Transcribed"
        row = self.indexFromItem(self.pinFileData[key]).row()
        newitem = QTableWidgetItem("Transcribed")
        self.setItem(row, 4, newitem)
    
    def getFile(self):
        """ TODO: improve the tab widget implementation """
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
            logger.error("cannot add file to data")
        else:
            self.nextkey += 1 
            logger.info("file added successfully")
        
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
                            self.addToNextState, 
                            self.removeFromNextState,
                            self.settingDetails)
        
        newFileWidget.addWidgetToTable(row, self.rowWidgets)
        self.fileWidgets[key] = newFileWidget
         
    def deleteFile(self, pin: QTableWidgetItem, key):
        """ delete a file from the table

        Args:
            pin (QTableWidgetItem): a pin to identify file on the table
            key (_type_): file key in database
        """
        logger.info("Delete the file from table")
        rowIdx = self.indexFromItem(pin).row()
        if rowIdx >= 0:
            self.removeRow(rowIdx)
            del self.fileWidgets[key]
        if key in self.transferList:
            self.transferList.remove(key)

    def addToNextState(self, key:str, pin: QAbstractItemView) -> None:
        """ add the file to transcribe list

        Args:
            key (str): the key to identify the file
        """
        try:
            if key in self.filedata:
                self.transferList.append(key)
                self._setColorRow(self.indexFromItem(pin).row(), Color.BLUEWHITE)
                self.signals.nonZeroFile.emit()
                
            else: 
                raise Exception("file is not found in the data")
        except Exception as err:
            logger.error(err)
        else:
            return
        
            
    def removeFromNextState(self, key:str, pin: QAbstractItemView) -> None:
        """ remove the file from the transcribe list 

        Args:
            key (str): the key to identify the file 
        """
        try:
            if key in self.transferList:
                self.transferList.remove(key)
                self._setColorRow(self.indexFromItem(pin).row(), "#fff")
                self.clearSelection()
                if len(self.transferList) == 0:
                    self.signals.ZeroFile.emit()
            else:
                raise Exception("file is not added to transcribe list")
        except Exception as err:
            logger.error(err)
        else:
            return
        
            
    def getTransferData(self) -> None:
        """ 
        get the file data that will be transfered to the next state
        """
        transferData = dict()
        for i in self.transferList:
            fileData = {**self.filedata[i], 
                        **{"Selected Action": "Transcribe"}, 
                        **{"Action in Progress":"Transcribing"}}
            transferData[i] = fileData
        self.signals.sendFile.emit(transferData)
        self._toggleAllSelect(clear=True)
       
        
    def changeSetting(self, key:str) -> None:
        """ configure the setting of one file identified by key

        Args:
            key (str): a key to identify file
        """
        selectSetting = changeProfileDialog(self.settings, key)
        selectSetting.signals.changeSetting.connect(self.updateSetting)
        selectSetting.exec()
        selectSetting.setFixedSize(QSize(200,200))
    
    """ TODO: change to a pop up """
    def settingDetails(self, key:str)->None:
        logger.info(key)
        logger.info(self.filedata)
        if key in self.filedata:
            self.signals.goSetting.emit(self.filedata[key]["Profile"])
    
    def updateSetting(self, newSetting:List[str]) -> None:
        logger.info("we reached the update seting")
        self.filedata[newSetting[0]]["Profile"] = newSetting[1]
        rowIdx = self.indexFromItem(self.pinFileData[newSetting[0]]).row()
        newSettingText = QTableWidgetItem(newSetting[1])
        self.setItem(rowIdx, 3, newSettingText)
    
    def _setColorRow(self, rowIdx, color):
        logger.info(self.rowAt(rowIdx))
        for i in range(self.columnCount()):
            if self.item(rowIdx, i):
                self.item(rowIdx, i).setBackground(QColor(color))
            else:
                logger.info("cannot set row color")
    
    def _resizeTable(self):
        logger.info("resized")
    
    def resizeEvent(self, e) -> None:
        self._resizeTable()
    
    
    def deleteAll(self)->None:
        for key, pin in self.pinFileData.items():
            self.deleteFile(pin, key)
            self.transferList.clear()
        
        self.pinFileData.clear()
        self.filedata.clear()

        
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
                 "Selected Action", 
                 " "]
ConfirmHeaderDimension = [0.1,0.35,0.25,0.13,0.17]

ProgressHeader = ["Type",
                  "Name",
                  "Action in Progress"]
ProgressDimension = [0.2, 0.55, 0.25]

SuccessHeader = ["Type",
                 "Name",
                 "Status",
                 "Output"]
SuccessDimension = [0.17, 0.35, 0.25, 0.23]



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
        self.pin = pin  # to localize the file on the table
        self.key = key  # to localize the flle on the actual data base 
        self.table = table
        self.selectFun = selectFun
        self.unselectFun = unselectFun
        self.gosetFule = gosetFun
        self.checkBoxContainer = QWidget()
        self.checkBoxLayout = QVBoxLayout()
        self.checkBoxContainer.setLayout(self.checkBoxLayout)
        self.checkBox = QCheckBox()
        self.checkBoxLayout.addWidget(self.checkBox, 
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
        self.deleteBtn.clicked.connect(lambda: deleteFun(self.pin, self.key))
        self.setBtn.clicked.connect(lambda: setFun(self.key))
        self.profileBtn.clicked.connect(lambda: gosetFun(self.key))
        self.checkBox.stateChanged.connect(self.checkStateChanged)

    
    def checkStateChanged(self, state:bool):
        if state:
            self.selectFun(self.key, self.pin)
        else:
            self.unselectFun(self.key, self.pin)
            
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
            self.table.setCellWidget(row, self.table.columnCount()- 1, self.Action)
        if "delete" not in rowWidgets:
            self.deleteBtn.hide()
            self.setBtn.hide()
        if "setting" not in rowWidgets:
            self.profileBtn.hide()
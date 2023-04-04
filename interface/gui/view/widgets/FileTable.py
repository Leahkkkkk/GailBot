'''
File: TableWidgets.py
Project: GailBot GUI
File Created: Friday, 14th October 2022 7:24:24 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Saturday, 15th October 2022 10:43:45 am
Modified By:  Siara Small  & Vivian Li
-----
Description: implementation of file table 
'''

KEYERROR = "File key not found"

from typing import Dict, List, Set, Tuple, TypedDict
from enum import Enum 

from .MsgBox import WarnBox, ConfirmBox
from .Background import initSecondaryColorBackground

from view.components.UploadFileTab import UploadFileTab
from view.pages.FileUploadTabPages import ChooseSet
from view.Signals import FileSignals
from gbLogger import makeLogger
from ..config.Style import Dimension, Color, FontSize, FontFamily
from ..config.Text import FileTableText as Text
from view.style.WidgetStyleSheet import FILE_TABLE, SCROLL_BAR, TABLE_HEADER
from view.util.ErrorMsg import ERR, WARN
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
from PyQt6.QtCore import (
    QObject, 
    Qt, 
    QSize, 
    pyqtSignal
)
from PyQt6.QtGui import QColor, QFont

class TableWidget(Enum):
    REMOVE = 1
    CHANGE_PROFILE = 2 
    PROFILE_DETAIL = 3
    CHECK = 4

class fileObject(TypedDict):
    """ interface for file dictionary """
    Name: str
    Type: str
    Profile: str
    Status: str
    Date: str
    Size: str
    Output: str
    FullPath: str
    
class Signals(QObject):
    """signals for controlling frontend view changes """
    requestProfile = pyqtSignal(str)
    requestChangeProfile = pyqtSignal(str)
    goSetting = pyqtSignal()
    changeProfile = pyqtSignal(tuple)
    nonZeroFile = pyqtSignal()
    ZeroFile = pyqtSignal()
    delete = pyqtSignal(str)
    select = pyqtSignal(str)
    unselect = pyqtSignal(str)
    transferState = pyqtSignal(list)
    error = pyqtSignal(str)

class FileTable(QTableWidget):
    """ class for the file tables """
    def __init__(self, 
                 headers: List[str], 
                 fileSignal: FileSignals,
                 tableWidgetsSet: Set[TableWidget] = None, 
                 transferListColor = Color.MAIN_BACKGROUND,
                 *args, 
                 **kwargs):
        """ a file table that display the files uploaded by the user, 
            and support different widgets that can be added to the 
            file table to edit the file's setting profile, removing file 
            from database, as well as selecting file to be transcribed

        Args:
            headers (List[str]): list of headers 
            filedata (Dict[str, fileObject]): initial file data
            fileSignal (FileSignals): signals to communicate with database
            profiles (List[str]): a list of available profile names
            tableWidgetsSet (Set[TableWidget]): a set of widgets name that will be displayed
                                   on each row
        """
        super().__init__(0, (len(headers)), *args, **kwargs)
        self.profiles = []
        self.headers = headers        
        self.filePins = dict()          # used to track file's position on 
                                        # table by pin
                                        
        self.transferList: set[str] = set()  
                                        # a set of keys of the file that will
                                        # be transferred to the next state
                                   
        self.fileWidgets: Dict[str, _TableCellWidgets] = dict()      
                                        # a dictionary to keep track of current
                                        # widget on the table 
                                        
        self.allSelected = False        # True if all files are selected 
        self.tableWidgetsSet = tableWidgetsSet
        self.logger =  makeLogger("F")
        self.transferlistBackground = transferListColor
        self.viewSignal = Signals()
        self.fileSignal = fileSignal
        self._setFileHeader()           # set file header 
        self._initStyle()
        self._connectViewSignal()
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)  
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    
        
    def resizeCol(self, widths:List[int]) -> None:
        """ takes in a list of width and resize the width of the each 
            column to the width
        """
        try:
            widthSum = self.width()
            if len(widths) != self.columnCount():
                self.logger.error("Cannot resize column")
            else:
                for i in range(len(widths)):
                    self.setColumnWidth(i, int(widths[i] * widthSum))
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.FAIL_TO.format("resize file table column"))
    
    ########################  table initializer    #########################
    def  _connectViewSignal(self):
        """ connects the signals upon button clicks """
        self.viewSignal.delete.connect(self._confirmRemoveFile)
        self.viewSignal.select.connect(self.addToNextState)
        self.viewSignal.unselect.connect(self.removeFromNextState)
        self.viewSignal.requestChangeProfile.connect(self.changeProfile)  
        self.viewSignal.requestProfile.connect(self.settingDetails)
    
    def _initStyle(self) -> None:
        """ Initialize the table style """
        self.horizontalHeader().setFixedHeight(45)
        self.setObjectName("FileTable")
        self.setStyleSheet(f"#FileTable{FILE_TABLE}")

        for i in range(self.columnCount()):
            self.horizontalHeader().setSectionResizeMode(
                i, QHeaderView.ResizeMode.Fixed)
        self.setFixedWidth(Dimension.TABLEWIDTH)
        self.setMinimumHeight(Dimension.TABLEMINHEIGHT)
        self.verticalScrollBar().setStyleSheet(SCROLL_BAR) 
        self.horizontalScrollBar().setStyleSheet(SCROLL_BAR)
        font = QFont(FontFamily.OTHER, FontSize.TABLE_ROW)
        self.setFont(font)
          
    def _setFileHeader(self) -> None:
        """ initialize file headers
        
        Args: 
            headers: (List[str]) a list of header names
        """
        try:
            for idx, header in enumerate(self.headers):
                headerItem = QTableWidgetItem(header)
                self.setHorizontalHeaderItem(idx, headerItem)
            self.horizontalHeader().sectionClicked.connect(
                self._headerClickedHandler)
            self.verticalHeader().hide()
        except Exception as e:
            self.logger.info(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("initialize file header", str(e)))
        self.horizontalHeader().setStyleSheet(TABLE_HEADER)
    
    
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
            for key, widget in self.fileWidgets.items():
                widget.setCheckState(False)
                if key in self.transferList:
                    self.transferList.remove(key) 
        else:
            for key, widget in self.fileWidgets.items():
                widget.setCheckState(True)
                if not key in self.transferList:
                    self.transferList.add(key)
        
        self.allSelected = not self.allSelected
    
    ########################  upload file handlers ########################
    def uploadFile(self):
        """ open up a pop up dialog for user to upload file 
           ** connected to upload file button 
        
        """
        try:
            addFileWindow = UploadFileTab(self.profiles)
            addFileWindow.signals.postFile.connect(self._postFile)
            addFileWindow.exec()
        except Exception as e:
            self.logger.error(e, exc_info=e) 
            WarnBox("An error occurred when uploading the file")
    
    def _postFile(self, file: fileObject):
        """ send signals to post file to the database 
            ** connected to the upload file button 
        """
        self.fileSignal.postFile.emit(file)
    
    def addFiles(self, files: List[Tuple]):
        """ adding a list of files to file table
            ** connected to sendfile signal from file database
        Args:
            files (List[Tuple])
        """
        for file in files:
            self.addFile(file)
    
    def addFile(self, file: Tuple[str, fileObject]):
        """ given a file object, adding it to the file table
            
        Args:
            file (Tuple[key, fileObject]): a file object
        """
        self.logger.info(file[0])
        self.logger.info(file[1])
        key, data = file
        try:
            newRowIdx = self.rowCount()
            self.insertRow(newRowIdx)
            for col in range(len(self.headers)):
                if self.headers[col] in data.keys():
                    newItem = QTableWidgetItem(str(data[self.headers[col]]))
                    if col == 1: 
                        filePin = newItem
                        self.filePins[key] = filePin
                    self.setItem(newRowIdx, col, newItem)
            
            if self.tableWidgetsSet:
                self._addFileWidgetToTable(newRowIdx, key) 
            self.resizeRowsToContents()  
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("uploading file", str(e)))
    
    def _addFileWidgetToTable(self, row:int, key:str):
        """ Add the widget that manipulates each file in a certain row 
            to the table
    
        Args:
            pin (QTableWidgetItem): _description_
        """
        newFileWidget = _TableCellWidgets(
            self,
            key,
            self.viewSignal,
            row,
            self.tableWidgetsSet)
        
        self.fileWidgets[key] = newFileWidget

    ####################### delete file handlers  #########################
    def _confirmRemoveFile(self, key:str):
        """ open a pop up for confirm to remove file """
        ConfirmBox("Are you sure to remove the file?", 
                          lambda: self.removeFile(key))
        
    def removeFile(self, key:str):
        """ remove one file from the table
        Args:
            key (str): file key 
        """
        try:
            if key in self.filePins:
                rowIdx = self.indexFromItem(self.filePins[key]).row()
                self.removeRow(rowIdx)
                self.fileSignal.delete.emit(key)
                del self.fileWidgets[key]
                del self.filePins[key]
                if key in self.transferList:
                    self.transferList.remove(key)
            else:
                self.viewSignal.error(KEYERROR)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("removing file", str(e)))
    
    def removeAll(self):
        """ remove all the file from table
        """
        keys = list(self.filePins)
        for key in keys:
            self.removeFile(key)
            
        self.transferList.clear()
        self.filePins.clear()
        self.viewSignal.ZeroFile.emit()
        

    ##################### edit profile handlers #########################
    def settingDetails(self, key:str):
        """ send a request to see file details
            *** connected to setting details page
            
        Args: key(str): a file key 
        """
        try:
            self.fileSignal.requestprofile.emit(key) # make request to load profile data 
            self.viewSignal.goSetting.emit()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("accessing file profile", str(e)))
        
    def changeFileToTranscribed(self, key:str):
        """ change one file's status to be transcribed, and delete the file
            from the file table

        Args:
            key (str): a file key that identifies the file
        """
        try:
            if key in self.filePins:
                self.updateFileContent((key, "Status", Text.complete))
            else:
                self.viewSignal.error.emit(KEYERROR)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("updating file status", str(e)))
        
    def showOneFileProgress(self, progress: Tuple[str, str]):
        """update the transcription progress of one file

        Args:
            progress (Tuple[str, str]): the Tuple stores the file key and the 
            progress message
        """     
        fileKey, msg = progress
        try:
            self.updateFileContent((fileKey, "Progress", msg))
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("updating file progress", str(e)))
        
    def changeProfile(self, key:str):
        """ open a pop up for user to change file setting 
            ** connected to changeProfile button 
        Args:
            key (str): a key to identify file
        """
        try:
            selectSetting = _ChangeProfileDialog(self.profiles, key)
            selectSetting.signals.changeProfile.connect(self.postNewFileProfile)
            selectSetting.exec()
            selectSetting.setFixedSize(QSize(200,200))
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("changing file profile", str(e)))
    
    def postNewFileProfile(self, newprofile: Tuple[str, str]):
        """ post the newly updated file change to the database
        """
        try:
            key, profilekey = newprofile
            self.fileSignal.changeProfile.emit(newprofile) 
            if key in self.filePins:
                row = self.indexFromItem(self.filePins[key]).row()
                newitem = QTableWidgetItem(profilekey)
                self.setItem(row, 3, newitem)
                if key in self.transferList: 
                    newitem.setBackground(QColor(self.transferlistBackground))
            else:
                self.viewSignal.error.emit(KEYERROR)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("adding new profile option", str(e)))
    
    def initProfiles(self, profiles: List[str]):
        """ initialize a list of available profile"""
        self.profiles = profiles
    
    def addProfile(self, profileName:str)->None:
        """ add profile keys 
            ** connect to the backend signal to add profile
        """
        self.profiles.append(profileName)
        
    def deleteProfile(self, profileName:str)->None:
        """ delete profile

        Args:
            profileName (str): the name of the profile
        """
        try: 
            self.profiles.remove(profileName)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            
            
    ###################### edit file handler ###############################        
    def updateFileContent(self, file: Tuple[str, str, str]):
        """ update the file content on the table

        Args:
            file (Tuple[key, field, value]): 
        """
        self.logger.info(f"get updated information {file}")
        key, field, value = file 
        if key in self.filePins:
            if field in self.headers:
                row = self.indexFromItem(self.filePins[key]).row()
                col = self.headers.index(field)
                newitem = QTableWidgetItem(value)
                self.setItem(row, col, newitem)
                if key in self.transferList:
                    newitem.setBackground(QColor(self.transferlistBackground))
        else:
            self.logger.error("File is not found")
    
    ###################### file transfer handler ##############################       
    def filterFile(self, files: Set[str]):
        """ given a set of file keys, the table will only show the file that 
            is in the list 
        
        Args:
            files (List[str]) a list of file keys
        """
        self.transferList.clear()
        for key, pin in self.filePins.items():
            rowidx = self.indexFromItem(pin).row()
            if key in files:
                self.showRow(rowidx)
                self.transferList.add(key)
            else:
                self.hideRow(rowidx)
    
    def addToNextState(self, key:str) -> None:
        """ add the file to transcribe list

        Args:
            key (str): the key to identify the file
        """
        self.logger.info(key)
        self.logger.info(self.transferList)
        try:
            if key in self.filePins:
                self.transferList.add(key)
                rowIdx = self.indexFromItem(self.filePins[key]).row()
                self._setColorRow(rowIdx,self.transferlistBackground)
                self.viewSignal.nonZeroFile.emit()
            else: 
                raise Exception("File is not found in the data")
        except Exception as err:
            self.logger.error(err)
        else:
            return
             
    def removeFromNextState(self, key:str) -> None:
        """ remove the file from the transcribe list 

        Args:
            key (str): the key that identifies the file to be removed
        """
        self.logger.info(key)
        self.logger.info(self.transferList)
        try:
            if key in self.transferList:
                self.transferList.remove(key)
                rowIdx = self.indexFromItem(self.filePins[key]).row()
                self._setColorRow(rowIdx, Color.MAIN_BACKGROUND)
                self.clearSelection()
                if len(self.transferList) == 0:
                    self.viewSignal.ZeroFile.emit()
            else:
                raise Exception("File is not added to transcribe list")
        except Exception as err:
            self.logger.error(err)
        else:
            return
        
    def transferState(self) -> None:
        """ send a signal that includes all the files that will be 
            transfer to the next state
        """
        self.viewSignal.transferState.emit(self.transferList)
        
    def transcribeFile(self):
        """ send signal to controller to transcribe file """
        self.fileSignal.transcribe.emit(self.transferList)  
        
    def _setColorRow(self, rowIdx, color):
        """ change the color of the row at rowIdx """
        self.logger.info(self.rowAt(rowIdx))
        for i in range(self.columnCount()):
            if self.item(rowIdx, i):
                self.item(rowIdx, i).setBackground(QColor(color))
            else:
                self.logger.info("failed to set row color")
       
class _TableCellWidgets(QObject):
    def __init__(
        self, 
        table: QTableWidget,
        key: str,
        signals: Signals,
        rowidx: int,
        widgets: Set[TableWidget],
        *args, 
        **kwargs):
        """ A wrapper class that contains all widgets in one row of filetable

        Args:
            table (QTableWidget): the parent table of the widget
            key (str): a key that identify the file in the data 
            signals (Signals): a Signals object that contains signal to be 
                               used for connecting the button with each file
            rowidx: the index of the row that the widgets will be inserted
            widgets: specifies a set of widgets that will be inserted 
        """
        super().__init__(*args, **kwargs)
        self.key = key  # to localize the flle on the actual data base 
        self.table = table
        self.signals = signals
        self.widgets = widgets
        self.rowidx = rowidx
        self._initWidgets()

    def _initWidgets(self):
        """ initialize the widget """
        if self.widgets:
            #create the widget
            self.Action = QWidget()
            self.ActionLayout = QVBoxLayout()
            self.Action.setLayout(self.ActionLayout)
            
            if TableWidget.CHECK in self.widgets:
                self._addCheckWidget()
                
            if TableWidget.REMOVE in self.widgets:
                self._addRemoveWidget()
                
            if TableWidget.CHANGE_PROFILE in self.widgets:
                self._addChangeProfileWidget()
                
            if TableWidget.PROFILE_DETAIL in self.widgets:
                self._addProfileDetailWidget()
                
            self.ActionLayout.setSpacing(1)
            self.ActionLayout.addStretch()
            
            # add widget to table
            lastCell = QTableWidgetItem()
            lastCol = self.table.columnCount() - 1
            self.table.setItem(self.rowidx, lastCol, lastCell)
            self.table.setCellWidget(self.rowidx, lastCol, self.Action)

    def _addCheckWidget(self):     
        self.checkBoxContainer = QWidget()
        self.checkBoxLayout = QVBoxLayout()
        self.checkBoxContainer.setLayout(self.checkBoxLayout)
        self.checkBox = QCheckBox()
        # connect widget signal to function
        self.checkBox.stateChanged.connect(self._checkStateChanged)
        self.checkBoxLayout.addWidget(
            self.checkBox, 
            alignment=Qt.AlignmentFlag.AlignCenter)
        # add widget to table
        firstCell = QTableWidgetItem()
        self.table.setItem(self.rowidx, 0, firstCell)
        self.table.setCellWidget(self.rowidx, 0, self.checkBoxContainer)
    
    def _addRemoveWidget(self):
        self.removeBtn = QPushButton(Text.delete)
        self.ActionLayout.addWidget(self.removeBtn)
        self.removeBtn.clicked.connect(
            lambda: self.signals.delete.emit(self.key))
    
    def _addChangeProfileWidget(self):
        self.editBtn = QPushButton(Text.changeSet)
        self.ActionLayout.addWidget(self.editBtn)
        self.editBtn.clicked.connect(
            lambda: self.signals.requestChangeProfile.emit(self.key)
        )
        
    def _addProfileDetailWidget(self):
        self.detailBtn = QPushButton(Text.profileDet)
        self.ActionLayout.addWidget(self.detailBtn)
        self.detailBtn.clicked.connect(
            lambda: self.signals.requestProfile.emit(self.key)
        )
        
    def _checkStateChanged(self, state:bool):
        """ emit signal to store the checked file to the transfer list """
        if state:
            self.signals.select.emit(self.key)
        else:
            self.signals.unselect.emit(self.key)
            
    def setCheckState(self, state):
        """ set the state of the check box """
        if state:
            self.checkBox.setCheckState(Qt.CheckState.Checked)
        else: 
            self.checkBox.setCheckState(Qt.CheckState.Unchecked)
            
class _ChangeProfileDialog(QDialog):
    def __init__(self, 
                 profiles: List[str], 
                 fileKey:str, 
                 *args, 
                 **kwargs) -> None:
        """ open up a dialog for user to change the profile for the file

        Args:
            profiles (List[str]):  a list of profile keys
            fileKey (str): the file key for which its profile will be changed
        """
        super().__init__(*args, **kwargs)
        self.signals = Signals()
        self.logger = makeLogger("F")
        self.fileKey = fileKey
        self.selectSetting = ChooseSet(profiles)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.selectSetting)
        self.selectSetting.selectSettings.currentTextChanged.connect(
            self.updateProfile)
        initSecondaryColorBackground(self)
        self.setFixedSize(QSize(450, 300))
    
    def updateProfile(self):
        """ send a signal to update the profile in the database
        """
        self.logger.info("update signal send")
        newSetting = self.selectSetting.getProfile()["Profile"]
        self.logger.info((self.fileKey, newSetting))
        self.signals.changeProfile.emit((self.fileKey,newSetting))
        self.close()
    
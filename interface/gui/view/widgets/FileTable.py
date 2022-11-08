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

""" 
    TODO: **sorting function
    TODO: **searching function 
"""
KEYERROR = "File key not found"

from typing import Dict, List, Set, Tuple, TypedDict
import logging

from view.widgets import MsgBox
from view.components.ChooseFileTab import ChooseFileTab
from view.pages.FileUploadTabPages import ChooseSet
from view.widgets.Background import initSecondaryColorBackground
from view.Signals import FileSignals
from util.Logger import makeLogger
from util.Style import Dimension, Color, FontFamily, FontSize
from util.Text import FileTableText as Text

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
from PyQt6.QtGui import QColor

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
                 dbSignal: FileSignals,
                 profiles: List[str] = [Text.default],  
                 rowWidgets: Set[str] = None, 
                 *args, 
                 **kwargs):
        """_summary_

        Args:
            headers (List[str]): list of headers 
            filedata (Dict[str, fileObject]): initial file data
            dbSignal (FileSignals): signals to communicate with database
            profiles (List[str]): a list of available profile names
            rowWidgets (Set[str]): a set of widgets name that will be displayed
                                   on each row
        """
        super().__init__(0, (len(headers)), *args, **kwargs)
        
        self.headers = headers        
        self.profiles = profiles      
        self.filePins = dict()          # used to track file's position on 
                                        # table by pin
                                        
        self.transferList: set[str] = set()  
                                        # a set of keys of the file that will
                                        # be transferred to the next state
        self.selecetdList: set[str] = set()
                                        # a set of currently selected files
                                   
        self.fileWidgets: Dict[str, TableCellButtons] = dict()      
                                        # a dictionary to keep track of current
                                        # widget on the table 
                                        
        self.allSelected = False        # True if all files are selected 
        self.rowWidgets = rowWidgets
        self.logger =  makeLogger("Frontend")
        
        self.viewSignal = Signals()
        self.dbSignal = dbSignal
        self._setFileHeader()     # set file header 
        self._initStyle()
        self._connectViewSignal()
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)  
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
    
    ########################  table initialier    #########################
    def  _connectViewSignal(self):
        """ connects the signals upon button clicks """
        self.viewSignal.delete.connect(self.removeFile)
        self.viewSignal.select.connect(self.addToNextState)
        self.viewSignal.unselect.connect(self.removeFromNextState)
        self.viewSignal.requestChangeProfile.connect(self.changeProfile)  
        self.viewSignal.requestProfile.connect(self.settingDetails)
    
    def _initStyle(self) -> None:
        """ Initialize the table style """
        self.horizontalHeader().setFixedHeight(45)
        for i in range(self.columnCount()):
            self.horizontalHeader().setSectionResizeMode(
                i,
                QHeaderView.ResizeMode.Fixed)
        self.setFixedWidth(Dimension.TABLEWIDTH)
        self.setMinimumHeight(Dimension.TABLEMINHEIGHT)
        
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
                    self.setColumnWidth(i, widths[i] * widthSum)
        except:
            msgBox = MsgBox.WarnBox("Failed to resize the table")
          
      
    def _setFileHeader(self) -> None:
        """ initialize file headers
        
        Args: 
            headers: (List[str]) a list of header names
        """
        try:
            for i in range(len(self.headers)):
                headerItem = QTableWidgetItem(self.headers[i])
                self.setHorizontalHeaderItem(i, headerItem)
                    
            self.horizontalHeader().sectionClicked.connect(
                self._headerClickedHandler)
            self.verticalHeader().hide()
        except:
            msgBox = MsgBox.WarnBox("Failed to set file header")
        
        self.horizontalHeader().setStyleSheet(f"background-color:{Color.TABLE_HEADER};"
                                              f"font-size:{FontSize.SMALL};"
                                              f"font-family:{FontFamily.MAIN};"
                                              f"color:{Color.PRIMARY_INTENSE}")
    
    
    def _headerClickedHandler(self, idx):
        """ handle header clicked signal  """
        try:
            if idx == 0:
                self._toggleAllSelect()
        except:
            msgBox = MsgBox.WarnBox("Failed to select all item")
   
    def _toggleAllSelect(self, clear = False):
        """ select or unselect all items in the table """
        if self.allSelected or clear:
            for key, widget in self.fileWidgets.items():
                widget.setCheckState(False)
                if key in self.transferList:
                    self.transferList.remove(key) 
                    self.selecetdList.remove(key)
        else:
            for key, widget in self.fileWidgets.items():
                widget.setCheckState(True)
                if not key in self.transferList:
                    self.transferList.add(key)
                    self.selecetdList.add(key)
        
        self.allSelected = not self.allSelected
    
    ########################  upload file handlers ########################
    
    def uploadFile(self):
        """ open up a pop up dialog for user to upload file 
           ** connected to upload file button 
        
        """
        addFileWindow = ChooseFileTab(self.profiles)
        addFileWindow.signals.postFile.connect(self._postFile)
        addFileWindow.exec()
    
    def addFiles(self, files: List[Tuple]):
        """ adding a list of files to file table
            ** connected to sendfile signal from file database
        Args:
            files (List[Tuple]): _description_
        """
        for file in files:
            self.addFile(file)
    
    def _postFile(self, file: fileObject):
        """ send signals to post file to the database 
            ** connected to the upload file button 
        """
        self.dbSignal.postFile.emit(file)
    
               
    def addFile(self, file: Tuple[str, fileObject]):
        """ given a file object, adding it to the file table
            
        Args:
            file (Tuple[key, fileObject]): a file object
        """
        self.logger.info(file[0])
        self.logger.info(file[1])
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
        
        if self.rowWidgets:
            self._addFileWidgetToTable(newRowIdx, key) #TODO:improve addwidget
        self.resizeRowsToContents()  
    
    def _addFileWidgetToTable(self, row:int, key:str):
        """ Add the widget that manipulates each file in a certain row 
            to the table
    
        Args:
            pin (QTableWidgetItem): _description_
        """
        newFileWidget = TableCellButtons(
            self,
            key,
            self.viewSignal,
            row,
            self.rowWidgets)
        
        self.fileWidgets[key] = newFileWidget

    ####################### delete file handlers  #########################
    def removeFile(self, key:str):
        """ delete one file
            ** connected to delete file button 
        Args:
            key (str): _description_
        """
        if key in self.filePins:
            rowIdx = self.indexFromItem(self.filePins[key]).row()
            self.removeRow(rowIdx)
            del self.filePins[key]
            del self.fileWidgets[key]
            if key in self.transferList:
                self.transferList.remove(key)
                self.selecetdList.remove(key)
        else:
            self.viewSignal.error(KEYERROR)
    
    def removeAll(self):
        """ delete all files on the file table 
            ** connected to deleteAll button 
        """
        for key in self.filePins.keys():
            self.removeFile(key)
            
        self.transferList.clear()
        self.selecetdList.clear()
        self.filePins.clear()
        

    ##################### edit profile handlers #########################
    def settingDetails(self, key:str):
        """ send a reqeust to see file details
            *** connected to setting details page
            
        Args: ket(str): a file key 
        """
        self.dbSignal.requestprofile.emit(key) # make request to load profile data 
        self.viewSignal.goSetting.emit()
   
    def changeFileToTranscribed(self, key:str):
        """ change one file's status to be transcribed, and delete the file
            from the file table

        Args:
            key (str): a file key that identifies the file
        """
        if key in self.filePins:
            self.updateFileContent((key, "Status", "Transcribed"))
        else:
            self.viewSignal.error.emit(KEYERROR)
            
    def changeAllFileProgress(self, progress: str):
        """ change the file progress for all files on the table """
        for key in self.filePins:
            self.updateFileContent((key, "Progress", progress))
        
    def changeProfile(self, key:str):
        """ open a pop up for user to change file setting 
            ** connected to changeProfile button 
        Args:
            key (str): a key to identify file
        """
        selectSetting = changeProfileDialog(self.profiles, key)
        selectSetting.signals.changeProfile.connect(self.postNewFileProfile)
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
            if key in self.selecetdList: 
                newitem.setBackground(QColor(Color.HIGHLIGHT))
        else:
            self.viewSignal.error.emit(KEYERROR)
    
    def addProfile(self, profileName:str)->None:
        """ add profile keys 
            ** connect to the backend signal to add profile
        """
        self.profiles.append(profileName)
    
            
    ###################### edit file handler ###############################        
    def updateFileContent(self, file: Tuple[str, str, str]):
        """ update the file content on the table

        Args:
            file (Tuple[key, field, value]): _description_
        """
        key, field, value = file 
        if key in self.filePins:
            if field in self.headers:
                row = self.indexFromItem(self.filePins[key]).row()
                col = self.headers.index(field)
                newitem = QTableWidgetItem(value)
                self.setItem(row, col, newitem)
                if key in self.selecetdList:
                    newitem.setBackground(QColor(Color.HIGHLIGHT))
        else:
            self.logger.error("File is not found")
    
    ###################### file transfer handler ##############################       
    def filterFile(self, files: Set[str]):
        """ given a set of file keys, the table will only show the file that 
            is in the list 
        
        Args:
            files (List[str]) a list of file keys
        """
        logging.info("Filter file")
        logging.info(len(self.filePins))
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
                self.selecetdList.add(key)
                rowIdx = self.indexFromItem(self.filePins[key]).row()
                self._setColorRow(rowIdx, Color.HIGHLIGHT)
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
                self.selecetdList.remove(key)
                rowIdx = self.indexFromItem(self.filePins[key]).row()
                self._setColorRow(rowIdx, "#fff")
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
            transfered to the next state
        """
        logging.info(self.transferList)
        self.viewSignal.transferState.emit(self.transferList)
        self.viewSignal.ZeroFile.emit()
        
    def transcribeFile(self):
        """ send signal to controller to transcribe file """
        self.dbSignal.transcribe.emit(self.transferList)  
        
        
    def _setColorRow(self, rowIdx, color):
        """ change the color of the row at rowIdx """
        self.logger.info(self.rowAt(rowIdx))
        for i in range(self.columnCount()):
            if self.item(rowIdx, i):
                self.item(rowIdx, i).setBackground(QColor(color))
            else:
                self.logger.info("failed to set row color")
    
     
class TableCellButtons(QObject):
    def __init__(
        self, 
        table: QTableWidget,
        key: str,
        signals:Signals,
        rowidx:int,
        widgets: Set[str],
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
        """ iniatialize the widget """
        if "check" in self.widgets:
            # create the widget
            self.checkBoxContainer = QWidget()
            self.checkBoxLayout = QVBoxLayout()
            self.checkBoxContainer.setLayout(self.checkBoxLayout)
            self.checkBox = QCheckBox()
            # connect widget signal to function
            self.checkBox.stateChanged.connect(self.checkStateChanged)
            self.checkBoxLayout.addWidget(
                self.checkBox, 
                alignment=Qt.AlignmentFlag.AlignCenter)
            # add widget to table
            firstCell = QTableWidgetItem()
            self.table.setItem(self.rowidx, 0, firstCell)
            self.table.setCellWidget(self.rowidx, 0, self.checkBoxContainer)
        
        if self.widgets:
            #creat the widget
            self.Action = QWidget()
            self.ActionLayout = QVBoxLayout()
            self.Action.setLayout(self.ActionLayout)
            if "delete" in self.widgets:
                self.deleteBtn = QPushButton(Text.delete)
                self.ActionLayout.addWidget(self.deleteBtn)
                self.deleteBtn.clicked.connect(
                    lambda: self.signals.delete.emit(self.key))
            if "edit" in self.widgets:
                self.editBtn = QPushButton(Text.changeSet)
                self.ActionLayout.addWidget(self.editBtn)
                self.editBtn.clicked.connect(
                    lambda: self.signals.requestChangeProfile.emit(self.key)
                )
            if "details" in self.widgets:
                self.detailBtn = QPushButton(Text.profileDet)
                self.ActionLayout.addWidget(self.detailBtn)
                self.detailBtn.clicked.connect(
                    lambda: self.signals.requestProfile.emit(self.key)
                )
            self.ActionLayout.setSpacing(1)
            self.ActionLayout.addStretch()
            #add widget to table
            lastCell = QTableWidgetItem()
            lastCol = self.table.columnCount() - 1
            self.table.setItem(self.rowidx, lastCol, lastCell)
            self.table.setCellWidget(self.rowidx, lastCol, self.Action)

    def checkStateChanged(self, state:bool):
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
            
class changeProfileDialog(QDialog):
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
        self.logger = makeLogger("Frontend")
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
        """ send a signal to upldate the profile in the database
        """
        self.logger.info("update signal send")
        newSetting = self.selectSetting.getProfile()["Profile"]
        self.logger.info((self.fileKey, newSetting))
        self.signals.changeProfile.emit((self.fileKey,newSetting))
        self.close()
    
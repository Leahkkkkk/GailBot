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
from typing import Dict, List, TypedDict


import sys
from types import new_class
from PyQt6.QtWidgets import (
    QTableWidget, 
    QTableWidgetItem, 
    QWidget, 
    QVBoxLayout,
    QApplication,
    QAbstractItemView,
    QHeaderView,
    QLabel,
    QCheckBox,
    QPushButton,
    QHBoxLayout)

from PyQt6.QtCore import QSize, QObject, Qt

class fileObject(TypedDict):
    Name: str
    Type: str
    Profile: str
    Status: str
    Date: str
    Size: str
    Output: str
    
class DisplayFile(QObject):
    def __init__(
        self, 
        table: QTableWidget,
        pin:QTableWidgetItem, 
        key:str,
        deleteFun:callable, 
        setFun:callable, 
        selectFun:callable, 
        unselectFun:callable, 
        *args, 
        **kwargs):
        """ A wrapper class that contains all widgets in one row of filetable

        Args:
            table (QTableWidget): the parent table of the widget
            pin (QTableWidgetItem): used to pin the position of the 
                                    file on the table
            key (str): a key that identify the file in the data 
            deleteFun (callable): function to delete the file
            setFun (callable): function to change or view the setting
            selectFun (callable): function to select the file
            unselectFun (callable): function to unselect the file
        """
        super().__init__(*args, **kwargs)

        self.pin = pin
        self.key = key
        self.table = table
        self.selectFun = selectFun
        self.unselectFun = unselectFun
        self.checkBox = QCheckBox()
        self.Action = QWidget()
        self.ActionLayout = QHBoxLayout()
        self.Action.setLayout(self.ActionLayout)
        self.deleteBtn = QPushButton("Delete")
        self.setBtn = QPushButton("Set")
        
        self.ActionLayout.addWidget(self.deleteBtn)
        self.ActionLayout.addWidget(self.setBtn)
        
        self.deleteBtn.clicked.connect(lambda: deleteFun(self.pin, self.key))
        self.setBtn.clicked.connect(lambda: setFun(self.key))
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
            
    def addWidgetToTable(self, row):
        self.table.setCellWidget(row, 0, self.checkBox)
        self.table.setCellWidget(row, self.table.columnCount()- 1, self.Action)
        
    
    

class FileTabel(QTableWidget):
    def __init__(self, 
                 headers: List[str], 
                 filedata: Dict[str, fileObject],  
                 *args, 
                 **kwargs):
        """_summary_

        Args:
            headers (List[str]): list of headers 
            filedata (Dict[str, fileObject]): initial file data
        """
        super().__init__(0, (len(headers)), *args, **kwargs)
        
        
        self.headers = headers          # stores the file header, 
                                        # dictate what data in file data will 
                                        # be displayed in the table
        
        self.filedata = filedata        # stores the file data
        
        self.transcribeList: List[str] = []   
                                        # a list of keys of the file that will
                                        #  be transcribed, 
                                   
        self.fileWidgets: Dict[str, DisplayFile] = dict()      
                                        # a dictionary to keep track of current
                                        # widget on the table 
       
        self.allSelected = False        # True of all files are selected 
        
        self.nextkey = len(self.filedata) + 1  
                                        # the key of the next added file
    
        self.initializeTable()
    
    def initializeTable(self) -> None:
        """ Initialize the table """
        self._setFileHeader(self.headers)     # set file header 
        self._setFileData()              # set initial file data
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

    def _setFileHeader(self,headers) -> None:
        """ initialize file headers
        
        Args: 
            headers: (List[str]) a list of header names
        """
        self.headerList = []
        for i in range(len(headers)):
            headerItem = QTableWidgetItem(headers[i])
            self.headerList.append(headerItem)
            self.setHorizontalHeaderItem(i, headerItem)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().sectionClicked.connect(self._headerClickedHandler)
    
    def _setFileData(self):
        """ display initial file data on to the table """
        for key, item in self.filedata.items():
            self.addFiletoTable(item,key)
    
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
    
    
    def addFile(self, file: fileObject):
        """ Add a file 
        
        """
        """ call a module to open add file dialog """
        """ store the file data in self.data """
        """ add file meta data to table """
        
        """ add file widget to table """
        try:
            self.addFiletoData(file, f"{self.nextkey}")
            self.addFiletoTable(file, f"{self.nextkey}")
        except:  
            print("errr")  
        else:
            self.nextkey += 1 
            print("file added")
    
    
    def addFiletoData(self, file: fileObject, key:str):
        """ add one file to the file data """
        self.filedata[key] = file
    
    def addFiletoTable(self, file: dict, key:str):
        """ display one file on the  table"""
        newRowIdx = self.rowCount()
        self.insertRow(newRowIdx)
        filePin = QTableWidgetItem(file[self.headers[1]])
        self.setItem(newRowIdx, 1, filePin)
        for col in range(2, len(self.headers)):
            if self.headers[col] in file.keys():
                newItem = QTableWidgetItem(file[self.headers[col]])
                self.setItem(newRowIdx, col, newItem)
        
        self.addFileWidgetToTable(filePin, newRowIdx, key)          
                
    def addFileWidgetToTable(self, pin: QTableWidgetItem, row:int, key:str):
        """ Add the widget that manipulates each file in a certain row 
            to the table
    
        Args:
            pin (QTableWidgetItem): _description_
        """
        newFileWidget = DisplayFile( 
                            self,
                            pin, # The table passes a pin to connect the widget
                            key,
                            self.deleteFile, 
                            self.goToSetting, 
                            self.addToTranscribe, 
                            self.removeFromTranscribe)
        newFileWidget.addWidgetToTable(row)
        self.fileWidgets[key] = newFileWidget
         
         
    def deleteFile(self, pin: QTableWidgetItem, key):
        """ delete a file from the table

        Args:
            pin (QTableWidgetItem): a pin to identify file on the table
            key (_type_): file key in database
        """
        rowIdx = self.indexFromItem(pin).row()
        if rowIdx >= 0:
            self.removeRow(rowIdx)
            del self.fileWidgets[key]
    

    def addToTranscribe(self, key:str):
        """ add the file to transcribe list

        Args:
            key (str): the key to identify the file
        """
        try:
            if key in self.filedata:
                self.transcribeList.append(key)
                print(f"current list after add: {self.transcribeList}")
            else: 
                raise Exception("file is not found in the data")
        except Exception as err:
            logging.error(err)
        else:
            return
        
            
    def removeFromTranscribe(self, key:str):
        """ remove the file from the transcribe list 

        Args:
            key (str): the key to identify the file 
        """
        try:
            if key in self.transcribeList:
                self.transcribeList.remove(key)
                print(f"current list after remove: {self.transcribeList}")
            else:
                raise Exception("file is not added to transcribe list")
        except Exception as err:
            logging.error(err)
        else:
            return

        
            
    def transcribe(self):
        print(self.transcribeList)
        
    
    def goToSetting(self, key:str):
        """ configure the setting of one file identified by key

        Args:
            key (str): a key to identify file
        """
        if key in self.filedata:
            print(self.filedata[key]["Profile"])
    

class Table(QWidget):
    def __init__(self):
        super().__init__()
        headers =["Select All","Type", "Name", "Profile", "Status", "Date", "Size", "Actions"]
        data = {
                   "1": {
                        "Type": ".wav",
                        "Name": "hello.wav",
                        "Profile": "Coffee Study",
                        "Status": "Not Transcribed",
                        "Date": "10/13/2020",
                        "Size": "85mb",
                        "Output": "Desktop",
                    },
                    "2": {
                        "Type": ".wav",
                        "Name": "hello.wav",
                        "Profile": "Coffee Study",
                        "Status": "Not Transcribed",
                        "Date": "10/13/2020",
                        "Size": "85mb",
                        "Output": "Desktop",
                    },
                    "3": {
                        "Type": ".wav",
                        "Name": "hello.wav",
                        "Profile": "Coffee Study",
                        "Status": "Not Transcribed",
                        "Date": "10/13/2020",
                        "Size": "85mb",
                        "Output": "Desktop",
                    }
                 }
       
        self.Table =FileTabel(headers, data, parent=self)
        self.Table.addFile({
                        "Type": ".wav",
                        "Name": "morning.wav",
                        "Profile": "Coffee Study",
                        "Status": "Not Transcribed",
                        "Date": "10/13/2020",
                        "Size": "85mb",
                        "Output": "Desktop",
                    })
        self.Table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.layout.addWidget(self.Table)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    example = Table()
    example.show()
    sys.exit(app.exec())
    
    

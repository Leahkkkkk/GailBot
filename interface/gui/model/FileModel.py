'''
File: FileModel.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 9:47:56 am
Modified By:  Siara Small  & Vivian Li
-----
'''
from model.FileItem import FileItem

from PyQt6 import QtCore
from PyQt6.QtCore import Qt

# TODO: possible format on transcription page- checkbox, type, 
# name, profile, transcription status, date, size, actions (3 clickable icons)

class FileModel(QtCore.QAbstractTableModel):
    """ conatains the database that store data about file 
        and functionality to reflect the changes in displaying the data
        on the front-end 
    """  
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.columns[section]
        if orientation == Qt.Orientation.Vertical and role == Qt.ItemDataRole.DisplayRole:
            return f"{section + 1}"
        
    def __init__(self):
        super(FileModel, self).__init__()
        self._data = [["", "", "", 
                       "", "", "", "", ""]]
        self._dataDict = dict()
        self.columns = [" ", "Type", "Name", "Profile", 
                       "Status", "Date", "Size", "Action"]
        self.placeHolder = True
        
        
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]
        
    def rowCount(self, index):
        """ return the row count """
        return len(self._data)

    def columnCount(self, index):
        """ return the column count """
        if self.rowCount(0) > 0:
            return len(self._data[0])
        else:
            return 0
    
    def getFile(self, rowidx):
        """ return a dictionart with filename and filepath """
        # print(self._dataDict[rowidx])
        return {"name": self._dataDict[rowidx].name, "path": self._dataDict[rowidx].path}

    def addFileHandler(self, fileObj: FileItem):
        """public function for adding the file to the database and 
           reflect the front-end changes on the file table

        Args:
            fileobj 
        """
        fileData = fileObj.convertToData()
        
        if self.placeHolder:
            self._data[0] = fileData
            self.placeHolder = False
        else:
            self._data.append(fileData)
            
        self.layoutChanged.emit()
        key = len(self._data) - 1
        self._dataDict[key] = fileObj
        return key

    def deleteFileHandler(self, key: int):
        del self._data[key]
        self.layoutChanged.emit()
        self.placeHolder = False
        
    
    def changeToTranscribed(self, idx:int):
        """ change the file status to be transcrbed """
        self._data[idx][3] = "transcribed"
        self.layoutChanged.emit()

class ConfirmFileModel(FileModel):
    def __init__(self):
        super(FileModel, self).__init__()
        self.columns = [" ", "Type", "Name",  "profile", "Selected Action"]
        self._data = [["","📁","Dummy.wav","Default", "Transcribe"]]


class ProgressFileMode(FileModel):
    def __init__(self):
        super(FileModel, self).__init__()
        self.columns = [" ", "Type", "Name",  "Action in Progress"]
        self._data = [["","📁","Dummy.wav","Transcribing"]]

class SuccessFileModel(FileModel):
    def __init__(self):
        super(FileModel, self).__init__()
        self.columns = [" ", "Type", "Name",  "Status", "Location", "Action"] 
        self._data = [["","📁","Dummy.wav","Transcribed","Desktop/output",""]]


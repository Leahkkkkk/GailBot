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

class FileModel(QtCore.QAbstractTableModel):
    """ conatains the database that store data about file 
        and functionality to reflect the changes in displaying the data
        on the front-end 
    """
    def __init__(self):
        super(FileModel, self).__init__()
        self._data = [["Type", "Name", "Profile", "status", "date", "size", "action"]]
        self._dataDict = dict()

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]
        
    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])
    
    def getFile(self, rowidx):
        print(self._dataDict[rowidx])
        return {"name": self._dataDict[rowidx].name, "path": self._dataDict[rowidx].path}

    def addFileHandler(self, fileObj: FileItem):
        """public function for adding the file to the database and 
           reflect the front-end changes on the file table

        Args:
            fileobj ([str]): a list of strings that contain the informatin 
                             about the file
        """

        fileData = fileObj.convertToData()
        self._data.append(fileData)
        print(fileData)
        self.layoutChanged.emit()
        key = len(self._data) - 1
        self._dataDict[key] = fileObj
        
    
    def changeToTranscribed(self, idx:int):
        self._data[idx][3] = "transcribed"
        self.layoutChanged.emit()

# TODO: possible format on transcription page- checkbox, type, 
# name, profile, transcription status, date, size, actions (3 clickable icons)

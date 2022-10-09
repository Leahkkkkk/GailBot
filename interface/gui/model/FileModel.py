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

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]
        
    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])
    
    def getFile(self, rowidx):
        print(self._data[rowidx])
        return {"name": self._data[rowidx][0], "path": self._data[rowidx][1]}

    def addFileHandler(self, fileobj):
        """public function for adding the file to the database and 
           reflect the front-end changes on the file table

        Args:
            fileobj ([str]): a list of strings that contain the informatin 
                             about the file
        """
        self._data.append(fileobj)
        self.layoutChanged.emit()
    
    def changeToTranscribed(self, idx:int):
        self._data[idx][3] = "transcribed"
        self.layoutChanged.emit()

# TODO: possible format on transcription page- checkbox, type, 
# name, profile, transcription status, date, size, actions (3 clickable icons)

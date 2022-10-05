""" Gailbot Model 
Define the data structure of the data and how data 
are displayed on user interface
"""
from PyQt6 import QtCore
from PyQt6.QtCore import Qt

class FileModel(QtCore.QAbstractTableModel):
    def __init__(self):
        super(FileModel, self).__init__()
        self._data = [["filename", "filepath", "filesize", "status"]]

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]
        
    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])
    
    def getfile(self, rowidx):
        print(self._data[rowidx])
        return {"name": self._data[rowidx][0], "path": self._data[rowidx][1]}

    def addfilehandler(self, fileobj):
        self._data.append(fileobj)
        self.layoutChanged.emit()
    
    def changeToTranscribed(self, idx:int):
        self._data[idx][3] = "transcribed"
        self.layoutChanged.emit()

# TODO: possible format on transcription page- checkbox, type, 
# name, profile, transcription status, date, size, actions (3 clickable icons)

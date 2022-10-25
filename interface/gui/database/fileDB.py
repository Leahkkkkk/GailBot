from typing import TypedDict

from PyQt6.QtCore import QObject, pyqtSignal


class fileObject(TypedDict):
    Name:str
    Type:str
    Profile:str
    Status: str
    Date: str
    Size: str
    Output: str
    FullPath: str
    
class Signals(QObject):
    sendFile = pyqtSignal(object)
    deleted  = pyqtSignal(str)
    profileRequest = pyqtSignal(str)
    fileAdded = pyqtSignal(tuple)
    error = pyqtSignal(str)
    success = pyqtSignal(str)


class fileModel:
    def __init__(self) -> None:
        self.filedata = dict() 
        self.signals = Signals()
        self.currentKey = 1
    
    def postFile(self, file:fileObject) -> None:
        """ add file to file database """
        key = str(self.currentKey)
        if key not in self.filedata:
            self.filedata[key] = file 
            self.signals.fileAdded.emit((key, file))
            self.currentKey += 1
        else:
            self.signals.error.emit("duplicate key")
    
    def deleteFile(self, key: str):
        if key in self.filedata:
            del self.filedata[key]
            if key not in self.filedata:
                self.signals.success.emit("file deleted from data base")
                self.signals.deleted.emit(str(key))
        else:
            self.signals.error.emit("file key not found")
    
    
    def editFile (self, )
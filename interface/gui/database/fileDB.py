from typing import TypedDict, Tuple

from PyQt6.QtCore import QObject, pyqtSignal

KEYERROR = "File key not found"

class fileObject(TypedDict):
    Name:str
    Type:str
    Profile:str
    Status: str
    Date: str
    Size: str
    Output: str
    FullPath: str
    SelectedAction: str
    Progress:str
    
class Signals(QObject):
    send = pyqtSignal(object)
    deleted  = pyqtSignal(str)
    error = pyqtSignal(str)
    success = pyqtSignal(str)
    requestprofile = pyqtSignal(str)
    profileRequest = pyqtSignal(str)
    fileAdded = pyqtSignal(tuple)
    transcribeRequest = pyqtSignal(tuple)
    

class FileModel:
    def __init__(self) -> None:
        self.data = dict() 
        self.signals = Signals()
        self.currentKey = 1
    
    def post(self, file:fileObject) -> None:
        """ add file to file database """
        key = str(self.currentKey)
        if key not in self.data:
            self.data[key] = file 
            self.signals.fileAdded.emit((key, file))
            self.currentKey += 1
        else:
            self.signals.error.emit("duplicate key")
    
    def delete(self, key: str):
        """delete the file from the database
        Args:
            key (str): the file key of the file to be deleted 
        """
        if key in self.data:
            del self.data[key]
            if key not in self.data:
                self.signals.success.emit(KEYERROR)
                self.signals.deleted.emit(str(key))
        else:
            self.signals.error.emit("file key not found")
    
    
    def edit(self, file: Tuple[str,fileObject]) -> None:
        """ change the file information on the database 
        Args:
            file Tuple[key,fileObject]: a tuple with file key and file object 
        """
        if file[0] not in self.data:
            self.signals.error.emit(KEYERROR)
        else:
            self.data[file[0]] = file[1]
        pass 


    def requestSetting(self, key:str):
        """ request to view the setting fo the file on the data base
        Args:
            key (str): _description_
        """
        if key not in self.data:
            self.signals.error.emit(KEYERROR)
        else:
            profile = self.data[key]["Profile"]
            self.signals.profileRequest.emit(profile)
    
    
    def editFileProfile(self, data: Tuple[str, str]) -> None:
        """change the profile information of the file 
        Args:
            data (Tuple[key, new profile]): _description_
        """
        if data[0] not in self.data:
            self.signals.error.emit(KEYERROR)
        else:
            self.data[data[0]]["Porfile"] = data[1]
        pass 


    def editFileStatus(self, data: Tuple[str, str]) -> None:
        """change the status information of the file 
        Args:
            data (Tuple[key, new status]): _description_
        """
        if data[0] not in self.data:
            self.signals.error.emit(KEYERROR)
        else:
            self.data[data[0]]["Status"] = data[1]
        pass
    
    def get(self, filekey:str) -> None:
        if filekey not in self.data:
            self.signals.error.emit(KEYERROR)
        else:
            self.signals.send.emit(self.data[filekey])
    
    def prepareTranscribe(self, filekey:str) -> None: 
        if filekey not in self.data:
            self.signals.error.emit(KEYERROR)
        else:
            fileData = self.data[filekey]
            fileData["Selected Action"] = "Transcription"
            self.signals.transcribeRequest.emit(())
    
    
    def getTranscribeData(self, filekey:str) -> Tuple:
        return (filekey, 
                self.data[filekey]["Name"], 
                self.data[filekey]["FullPath"],
                self.data[filekey]["Output"])
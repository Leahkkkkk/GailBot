from dataclasses import dataclass
from typing import TypedDict, Tuple, Dict

from util.Logger import makeLogger
from util.Error import ErrorMsg, DBExecption
from PyQt6.QtCore import QObject, pyqtSignal

from dict_to_dataclass import DataclassFromDict, field_from_dict



@dataclass 
class FileObj(DataclassFromDict):
    Name:     str  = field_from_dict()
    Type:     str  = field_from_dict()
    Profile:  str = field_from_dict()
    Status:   str = field_from_dict()
    Date:     str = field_from_dict()
    Size:     str = field_from_dict()
    Output:   str = field_from_dict()
    FullPath: str = field_from_dict()
    SelectedAction: str = field_from_dict()
    Progress:       str = field_from_dict()
    
    
class fileDict(TypedDict):
    Name:   str
    Type:   str
    Profile:str
    Status: str
    Date:   str
    Size:   str
    Output: str
    FullPath: str
    SelectedAction: str
    Progress:str
    
class Signals(QObject):
    send = pyqtSignal(object)
    deleted  = pyqtSignal(str)
    error = pyqtSignal(str)
    success = pyqtSignal(str)
    profileRequest = pyqtSignal(str)
    fileAdded = pyqtSignal(tuple)
    fileUpdated = pyqtSignal(tuple)
    

class FileModel:
    def __init__(self) -> None:
        """ file database """
        self.data : Dict[str, FileObj] = dict() 
        self.signals = Signals()
        self.currentKey = 1
    
    
    ##########################  request handler ###########################
    def post(self, data : fileDict) -> None:
        """ add file to file database """
        self.logger = makeLogger("Database")
        self.logger.info("post file to database")
        key = str(self.currentKey)
        try:
            if key not in self.data:
                file = FileObj.from_dict(data)
                self.data[key] = file 
                self.signals.fileAdded.emit((key, data))
                self.currentKey += 1
            else:
                self.signals.error.emit(ErrorMsg.DUPLICATEKEY)
                self.logger.error(ErrorMsg.DUPLICATEKEY)
        except:
            self.signals.error.emit(ErrorMsg.POSTERROR)
            self.logger.error(ErrorMsg.POSTERROR)
    
    
    def delete(self, key: str):
        """delete the file from the database
        Args:
            key (str): the file key of the file to be deleted 
        """
        
        self.logger.info("delete file from database")
        try:
            if key in self.data:
                del self.data[key]
                if key not in self.data:
                    self.signals.deleted.emit(key)
                else:
                    raise DBExecption(ErrorMsg.DELETEEROR)
            else:
                self.signals.error.emit(ErrorMsg.KEYERROR)
                self.logger.error(ErrorMsg.KEYERROR)
        except DBExecption as err:
            self.signals.error.emit(err)
            self.logger.error(err)
            
            
    def edit(self, file: Tuple[str,fileDict]) -> None:
        """ change the file information on the database 
        Args:
            file Tuple[key,fileObject]: a tuple with file key and file object 
        """
        self.logger.info("edit file in the database")
        key, newfile  = file
        try:
            if key not in self.data:
                self.logger.error(ErrorMsg.KEYERROR)
                self.signals.error.emit(ErrorMsg.KEYERROR)
            else:
                self.data[key] = newfile
        except:
            self.signals.error.emit(ErrorMsg.EDITERROR) 


    def editFileStatus(self, data: Tuple[str, str]) -> None:
        """change the status information of the file 
        Args:
            data (Tuple[key, new status]): _description_
        """
        self.logger.info("edit the file status in the database")
        key, status = data
        try:
            if key not in self.data:
                self.signals.error.emit(ErrorMsg.KEYERROR)
                self.logger.error(ErrorMsg.KEYERROR)
            else:
                self.data[key].Status = status
        except:
            self.signals.error.emit(ErrorMsg.EDITERROR)
            self.logger.error(ErrorMsg.EDITERROR)
            
    
    def changeFiletoTranscribed(self, key: str):
        """ change the file status to be transcrbed """    
        self.editFileStatus((key, "Transcribed"))
    
    
    def editFileProfile(self, data: Tuple[str, str]) -> None:
        """change the profile information of the file 
        Args:
            data (Tuple[key, new profile]): _description_
        """
        self.logger.info("request to edit file profile in the database")
        key, profile = data
        try:
            if key not in self.data:
                self.signals.error.emit(ErrorMsg.KEYERROR)
                self.logger.error(ErrorMsg.KEYERROR)
            else:
                self.data[key].Profile = profile
                self.updateFileResponse(key, "Profile", profile)
        except:
            self.signals.error.emit(ErrorMsg.EDITERROR)
            self.logger.error(ErrorMsg.EDITERROR)
            
    def updateFileProgress(self, data):
        self.logger.info("request to change file progress in the database")
        key, progress = data
        try:
            if key not in self.data:
                self.signals.error.emit(ErrorMsg.KEYERROR)
                self.logger.error(ErrorMsg.KEYERROR)
            else:
                self.data[key].Progress = progress
                self.updateFileResponse(key, "Progress", progress)
        except:
            self.signals.error.emit(ErrorMsg.EDITERROR)
            self.logger.error(ErrorMsg.EDITERROR)
        

    ##################### response emitter ############################# 
    def updateFileResponse(self, key, field, value):
        """ send the signal to update the file data, which will be reflected
            on the front end 

        Args:
            key (str): file key
            field (str): updated field 
            value (str): updated value
        """
        self.logger.info("response to update file database content")
        try:
            self.signals.fileUpdated.emit((key, field, value))
        except:
            self.signals.error.emit(ErrorMsg.EDITERROR)
            self.logger.error(ErrorMsg.EDITERROR)
    
    
    def requestProfile(self, key:str):
        """ request to view the setting fo the file on the data base
        Args:
            key (str): _description_
        """
        self.logger.info("request file profile setting from database")  
        try:
            if key not in self.data:
                self.signals.error.emit(ErrorMsg.KEYERROR)
                self.logger.error(ErrorMsg.KEYERROR)
            else:
                profile = self.data[key].Profile
                self.signals.profileRequest.emit(profile)
                self.logger.info((key,profile))
        except:
            self.signals.error.emit(ErrorMsg.GETERROR)
            self.logger.error(ErrorMsg.GETERROR)
            
 
    def get(self, filekey:str) -> None:
        """ send the signal to get file data 

        Args:
            filekey (str): 
        """
        self.logger.info("get the file from the database")
        try:
            if filekey not in self.data:
                self.signals.error.emit(ErrorMsg.KEYERROR)
                self.logger.error(ErrorMsg.KEYERROR)
            else:
                self.signals.send.emit(self.data[filekey])
        except:
            self.signals.error.emit(ErrorMsg.GETERROR)
            self.logger.error(ErrorMsg.GETERROR)  
            
              
    def getTranscribeData(self, key:str) -> Tuple:
        """ send the file data that will be transcribed

        Args:
            filekey (str): _description_

        Returns:
            Tuple: (filekey, fileobject)
        """
        self.logger.info("get the file data that will be trancribed")
        if key not in self.data:
            self.signals.error.emit(ErrorMsg.GETERROR)
            self.logger.info(ErrorMsg.GETERROR)
        else:
            return (key, self.data[key])
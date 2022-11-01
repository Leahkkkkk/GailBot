
from logging import raiseExceptions
from typing import TypedDict, Tuple


from util.Logger import makeLogger
from util.Error import ErrorMsg, DBExecption

from PyQt6.QtCore import QObject, pyqtSignal

logger = makeLogger("Database")


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
    fileUpdated = pyqtSignal(tuple)
    transcribed = pyqtSignal(str)
    

class FileModel:
    def __init__(self) -> None:
        logger.info("init file database")
        self.data = dict() 
        self.signals = Signals()
        self.currentKey = 1
    
    
    def post(self, file:fileObject) -> None:
        """ add file to file database """
        
        logger.info("post file to database")
        key = str(self.currentKey)
        try:
            if key not in self.data:
                self.data[key] = file 
                self.signals.fileAdded.emit((key, file))
                self.currentKey += 1
            else:
                self.signals.error.emit(ErrorMsg.DUPLICATEKEY)
                logger.error(ErrorMsg.DUPLICATEKEY)
        except:
            self.signals.error.emit(ErrorMsg.POSTERROR)
            logger.error(ErrorMsg.POSTERROR)
    
    
    def delete(self, key: str):
        """delete the file from the database
        Args:
            key (str): the file key of the file to be deleted 
        """
        
        logger.info("delete file from database")
        try:
            if key in self.data:
                del self.data[key]
                if key not in self.data:
                    self.signals.deleted.emit(key)
                else:
                    raise DBExecption(ErrorMsg.DELETEEROR)
            else:
                self.signals.error.emit(ErrorMsg.KEYERROR)
                logger.error(ErrorMsg.KEYERROR)
        except DBExecption as err:
            self.signals.error.emit(err)
            logger.error(err)
            
            
    
    def edit(self, file: Tuple[str,fileObject]) -> None:
        """ change the file information on the database 
        Args:
            file Tuple[key,fileObject]: a tuple with file key and file object 
        """
        logger.info("edit file in the database")
        key, newfile  = file
        try:
            if key not in self.data:
                logger.error(ErrorMsg.KEYERROR)
                self.signals.error.emit(ErrorMsg.KEYERROR)
            else:
                self.data[key] = newfile
        except:
            self.signals.error.emit(ErrorMsg.EDITERROR) 


    def requestSetting(self, key:str):
        """ request to view the setting fo the file on the data base
        Args:
            key (str): _description_
        """
        
        logger.info("request file profile setting from database")  
        try:
            if key not in self.data:
                self.signals.error.emit(ErrorMsg.KEYERROR)
                logger.error(ErrorMsg.KEYERROR)
            else:
                profile = self.data[key]["Profile"]
                self.signals.profileRequest.emit(profile)
        except:
            self.signals.error.emit(ErrorMsg.GETERROR)
            logger.error(ErrorMsg.GETERROR)
    
    def editFileProfile(self, data: Tuple[str, str]) -> None:
        """change the profile information of the file 
        Args:
            data (Tuple[key, new profile]): _description_
        """
        logger.info("request to edit file profile in the database")
        key, profile = data
        try:
            if key not in self.data:
                self.signals.error.emit(ErrorMsg.KEYERROR)
                logger.error(ErrorMsg.KEYERROR)
            else:
                self.data[key]["Porfile"] = profile
                self.signals.fileUpdated.emit((key, "Profile", profile))
        except:
            self.signals.error.emit(ErrorMsg.EDITERROR)
            logger.error(ErrorMsg.EDITERROR)
            
   
    def editFileStatus(self, data: Tuple[str, str]) -> None:
        """change the status information of the file 
        Args:
            data (Tuple[key, new status]): _description_
        """
        logger.info("edit the file status in the database")
        key, status = data
        try:
            if key not in self.data:
                self.signals.error.emit(ErrorMsg.KEYERROR)
                logger.error(ErrorMsg.KEYERROR)
            else:
                self.data[key]["Status"] = status
        except:
            self.signals.error.emit(ErrorMsg.EDITERROR)
            logger.error(ErrorMsg.EDITERROR)
            
    def changeFiletoTranscribed(self, key: str):
        """ change the file status to be transcrbed """    
        self.editFileStatus((key, "Transcribed"))
        
        
    def get(self, filekey:str) -> None:
        """ send the signal to get file data 

        Args:
            filekey (str): 
        """
        logger.info("get the file from the database")
        try:
            if filekey not in self.data:
                self.signals.error.emit(ErrorMsg.KEYERROR)
                logger.error(ErrorMsg.KEYERROR)
            else:
                self.signals.send.emit(self.data[filekey])
        except:
            self.signals.error.emit(ErrorMsg.GETERROR)
            logger.error(ErrorMsg.GETERROR)  
            
              
    def getTranscribeData(self, key:str) -> Tuple:
        """ send the file data that will be transcribed

        Args:
            filekey (str): _description_

        Returns:
            Tuple: (filekey, fileobject)
        """
        logger.info("get the file data that will be trancribed")
        if key not in self.data:
            self.signals.error.emit(ErrorMsg.GETERROR)
            logger.info(ErrorMsg.GETERROR)
        else:
            return (key, self.data[key])
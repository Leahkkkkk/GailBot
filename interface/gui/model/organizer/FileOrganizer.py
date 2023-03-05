'''
File: fileDB.py
Project: GailBot GUI
File Created: Friday, 4th November 2022 1:01:27 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Sunday, 13th November 2022 8:38:26 am
Modified By:  Siara Small  & Vivian Li
-----
Description: Implementation of a database that stores all the file data 
'''


from dataclasses import dataclass
from typing import TypedDict, Tuple, Dict, Set
from gailbot.api import GailBot

from util.Logger import makeLogger
from util.Error import ErrorMsg, DBException, ErrorFormatter
from PyQt6.QtCore import QObject, pyqtSignal
from dict_to_dataclass import DataclassFromDict, field_from_dict



@dataclass 
class FileObj(DataclassFromDict):
    """ implement the interface of a file object  """
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
    """ the scheme of file data, 
        a file is posted to the database through a dictionary that 
        follows this scheme
    """
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
    """ 
        contains pyqtSignal to support communication between 
        file database and view 
    """
    send = pyqtSignal(object)
    deleted  = pyqtSignal(str)
    error = pyqtSignal(str)
    success = pyqtSignal(str)
    profileRequest = pyqtSignal(str)
    fileAdded = pyqtSignal(tuple)
    fileUpdated = pyqtSignal(tuple)
    

class FileOrganizer:
    def __init__(self, gbController: GailBot) -> None:
        """ implementation of File database
        
        Field:
        1. data : a dictionary stores the file data
        2. signals: a signal object to support communication between the 
                    database and the caller, the caller should support function
                    from view object to handle signal emitted by the file 
                    database
        3. currentKey: stores the file key that will be used when a new file 
                        is posted to the database
        
        
        Public Functions: 
        
        Database modifier:
        functions that delete or add file to the database
        1. post(self, data : fileDict) -> None 
        2. delete(self, key: str) -> None
        
        File modifier:
        functions that modify files data that is already in the database
        3. edit(self, file: Tuple[str,fileDict]) -> None
        4. editFileStatus(self, data: Tuple[str, str]) -> None
        5. changeFiletoTranscribed(self, key: str) -> None
        6. editFileProfile(self, data: Tuple[str, str]) -> None
        7. updateFileProgress(self, data: Tuple [str, str]) -> None
        
        Database access:
        functions that access data from database
        9. requestProfile(self, key:str) -> None
        10. get(self, filekey:str) -> None
        11. getTranscribeData(self, key:str) -> Tuple
        """
        self.gb: GailBot = gbController
        self.data : Dict[str, FileObj] = dict() 
        self.signals = Signals()
        self.currentKey = 1
        self.logger = makeLogger("F")
    
    
    ##########################  request handler ###########################
    def post(self, data : fileDict) -> None:
        """ add file to file database 
        data: (fileDict) a dictionary that contains the file data to be 
              added to the database
        """
        self.logger.info("post file to database")
        key = str(self.currentKey)
        self.logger.info(data)
        file = FileObj.from_dict(data)
        try:
            if key not in self.data and self.gb.add_source(file.FullPath, file.Output):
                self.data[key] = file 
                self.signals.fileAdded.emit((key, data))
                self.currentKey += 1
            else:
                self.signals.error.emit(ErrorMsg.DUPLICATEKEY)
                self.logger.error(ErrorMsg.DUPLICATEKEY)
        except Exception as e:
            self.signals.error.emit(ErrorFormatter.DEFAULT_ERROR.format(source="post file", msg=e))
            self.logger.error(f"Error in posting file: {e}")
    
    
    def delete(self, key: str) -> None:
        """delete the file from the database
        Args:
            key (str): the file key of the file to be deleted 
        """
        
        self.logger.info("delete file from database")
        try:
            if key in self.data and self.gb.remove_source(self.data[key].Name):
                del self.data[key]
                self._updateFileResponse(key, "Status", "deleted")
                if key not in self.data:
                    self.signals.deleted.emit(key)
                else:
                    raise DBException(ErrorMsg.DELETEEROR)
            else:
                self.signals.error.emit(ErrorMsg.KEYERROR)
                self.logger.error(ErrorMsg.KEYERROR)
        except DBException as err:
            self.signals.error.emit(err)
            self.logger.error(err)
            
            
    def edit(self, file: Tuple[str,fileDict]) -> None:
        """ change the file information on the database 
        Args:
            file Tuple[key,fileObject]: a tuple with file key and file object 
        """
        self.logger.info("edit file in the database")
        key, newFile  = file
        try:
            if key not in self.data:
                self.logger.error(ErrorMsg.KEYERROR)
                self.signals.error.emit(ErrorMsg.KEYERROR)
            else:
                self.data[key] = newFile
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
            
    
    def changeFiletoTranscribed(self, key: str)-> None:
        """ change the file status to be transcribed 
        Args: 
            key: a file key that identifies the file in the database
        """    
        try:
            self.editFileStatus((key, "Transcribed"))
            assert self.gb.remove_source(self.data[key].Name)
        except Exception as e:
            self.logger.error("Deleting file from gailbot fails, error {e}")
    
    
    def editFileProfile(self, data: Tuple[str, str]) -> None:
        """change the profile information of the file 
        Args:
            data (Tuple[key, new profile]): a tuple  that stores the file key 
                                            and a the new profile name
        """
        self.logger.info("request to edit file profile in the database")
        key, profile = data
        try:
            if key not in self.data or not self.gb.is_source(self.data[key].Name):
                self.signals.error.emit(ErrorMsg.KEYERROR)
                self.logger.error(ErrorMsg.KEYERROR)
                return 
            elif not self.gb.is_setting(profile):
                self.signals.error.emit(ErrorMsg.PROFILE_NOT_FOUND)
                self.logger.error(f"{profile}: {ErrorMsg.PROFILE_NOT_FOUND}")
            else:
                self.data[key].Profile = profile
                assert self.gb.apply_setting_to_source(self.data[key].Name, profile)
                self._updateFileResponse(key, "Profile", profile)
        except:
            self.signals.error.emit(ErrorMsg.EDITERROR)
            self.logger.error(ErrorMsg.EDITERROR)
            
            
    def updateFileProgress(self, data: Tuple [str, str]) -> None:
        """ update the file transcribing progress in file database 

        Args:
            data (Tuple[str, str]):a tuple that stores the file key and the 
                                   current transcribe progress in strings
        """
        self.logger.info("request to change file progress in the database")
        key, progress = data
        try:
            if key not in self.data:
                self.signals.error.emit(ErrorMsg.KEYERROR)
                self.logger.error(ErrorMsg.KEYERROR)
            else:
                self.data[key].Progress = progress
                self._updateFileResponse(key, "Progress", progress)
        except:
            self.signals.error.emit(ErrorMsg.EDITERROR)
            self.logger.error(ErrorMsg.EDITERROR)
        

    ##################### response emitter ############################# 
    def _updateFileResponse(self, key, field, value) -> None:
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
    
    
    def requestProfile(self, key:str) -> None:
        """ request to view the setting fo the file on the data base
        Args:
            key (str): a file key that identifies the file in the database
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
            filekey (str): a file key that identifies the file in the database
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
            
    def getTranscribeData(self, keys: Set[str]) -> Dict[str, str]:
        data = dict()
        for key in keys:
            name = self.getFileName(key)
            if name: 
                data[key] = name
        return data
            
              
    def getFileName(self, key:str) -> str:
        """ send the file data that will be transcribed

        Args:
            key (str):a file key that identifies the file in the database

        Returns:
            Tuple: (filekey, fileobject): return a tuple containint the file key 
                                            and the file object
        """
        self.logger.info("get the file data that will be trancribed")
        if key not in self.data:
            self.signals.error.emit(ErrorMsg.GETERROR)
            self.logger.info(ErrorMsg.GETERROR)
            return False
        else:
            return self.data[key].Name
        
    def profileDeleted(self, profileName:str):
        """ send signal to update the profile of the files to default 
            after the original profile is deleted

        Args:
            profileName (str): profile name that is deleted

        """
        try:
            for key, file in self.data.items():
                if file.Profile == profileName:
                    file.Profile = self.gb.get_src_setting_name(file.Name)
                    self._updateFileResponse(key, "Profile", file.Profile)
        except Exception as e:
            self.logger.error(f"error deleting profile {e}")
            
                
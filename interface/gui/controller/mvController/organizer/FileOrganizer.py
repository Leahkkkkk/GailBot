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
from view.Signals import FileSignals
from controller.Request import Request
from gbLogger import makeLogger
from controller.util.Error import  ERR
from PyQt6.QtCore import QObject, pyqtSignal
from dict_to_dataclass import DataclassFromDict, field_from_dict



@dataclass 
class FileObj(DataclassFromDict):
    """ implement the interface of a file object  """
    Name    : str = field_from_dict()
    Type    : str = field_from_dict()
    Output  : str = field_from_dict()
    FullPath: str = field_from_dict()
    Profile : str = field_from_dict()
    Status  : str = field_from_dict()
    Date    : str = field_from_dict()
    Size    : str = field_from_dict()
    Progress: str = field_from_dict()
    
class fileDict(TypedDict):
    """ the scheme of file data, 
        a file is posted to the database through a dictionary that 
        follows this scheme
    """
    Name    : str
    Type    : str
    Profile : str
    Status  : str
    Date    : str
    Size    : str
    Output  : str
    FullPath: str
    Progress: str
    
class Signals(QObject):
    """ 
        contains pyqtSignal to support communication between 
        file database and view 
    """
    error          = pyqtSignal(str)
    
class FileOrganizer:
    def __init__(self, gbController: GailBot, fileSignal: FileSignals) -> None:
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
        self.signals = Signals()
        self.currentKey = 1
        self.logger = makeLogger("F")
        self.registerSignal(fileSignal)
    
    def registerSignal(self, signal:FileSignals):
        signal.requestprofile.connect(self.requestProfile)
        signal.postFileRequest.connect(self.post)
        signal.changeProfileRequest.connect(self.editFileProfile)
        signal.deleteRequest.connect(self.delete)
        signal.viewOutput.connect(self.viewOutput)
    
    ##########################  request handler ###########################
    def post(self, request : Request) -> None:
        """ add file to file database 
        data: (fileDict) a dictionary that contains the file data to be 
              added to the database
        """
        self.logger.info("post file to database")
        self.logger.info(request.data)
        file = FileObj.from_dict(request.data)
        try:
            if self.gb.is_source(file.Name):
                request.fail(ERR.DUPLICATE_FILE_NAME)
            elif self.gb.add_source(file.FullPath, file.Output):
                request.succeed((file.Name, request.data))
                self.currentKey += 1
                assert self.gb.apply_setting_to_source(file.Name, file.Profile)
            else:
                request.fail(ERR.DUPLICATE_FILE_KEY)
                self.logger.error(ERR.DUPLICATE_FILE_KEY)
        except Exception as e:
            request.fail(ERR.ERROR_WHEN_DUETO.format("posting new file", str(e)))
            self.logger.error(f"Error in posting file: {e}", exc_info=e)
    
    
    def delete(self, request: Request) -> None:
        """delete the file from the database
        Args:
            key (str): the file key of the file to be deleted 
        """
        self.logger.info("delete file from database")
        try:
            if self.gb.remove_source(request.data):
                request.succeed(request.data)
            else:
                request.fail(ERR.DELETE_FILE_ERROR)
                self.logger.error(f"file {request.data} is not found")
        except Exception as e:
            self.logger.error(e, exc_info=e)
            request.fail(ERR.DELETE_FILE_ERROR)
            
            
    def editFileProfile(self, request: Request) -> None:
        """change the profile information of the file 
        Args:
            data (Tuple[key, new profile]): a tuple  that stores the file key 
                                            and a the new profile name
        """
        file, profile = request.data
        self.logger.info(f"request to change the file {file}'s setting to {profile}")
        try:
            if not self.gb.is_source(file):
                request.fail(ERR.FILE_KEY_ERR)
                self.logger.error(ERR.FILE_KEY_ERR)
                return 
            elif not self.gb.is_setting(profile):
                request.fail(ERR.PROFILE_NOT_FOUND)
                self.logger.error(f"{profile}: {ERR.PROFILE_NOT_FOUND}")
            else:
                assert self.gb.apply_setting_to_source(file, profile)
                self.logger.info(f"the setting of the file {file} is change to {self.gb.get_source_setting_dict(file)}")
                request.succeed(request.data)
        except:
            request.fail(ERR.EDIT_FILE_ERROR)
            self.logger.error(ERR.EDIT_FILE_ERROR)
            
            
    def requestProfile(self, request:Request) -> None:
        """ request to view the setting fo the file on the data base
        Args:
            key (str): a file key that identifies the file in the database
        """
        self.logger.info("request file profile setting from database")  
        try:
            profile = self.gb.get_src_setting_name(request.data)
            profileData = self.gb.get_setting_dict(profile)
            request.succeed((profile, profileData))
        except Exception as e:
            request.fail(ERR.GET_FILE_ERROR)
            self.logger.error(ERR.GET_FILE_ERROR, exc_info=e)
    
    
    def viewOutput(self, request: Request) -> None:
        try:
            path = self.gb.get_source_outdir(request.data)
            request.succeed(path)
        except Exception as e:
            request.fail(ERR.GET_FILE_OUTPUT_ERROR)   
            self.logger.error(e, exc_info=e)     
 
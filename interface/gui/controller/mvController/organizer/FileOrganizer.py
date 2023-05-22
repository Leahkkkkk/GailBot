'''
File: FileOrganizer.py
Project: GailBot GUI
File Created: 2023/04/01
Author: Siara Small  & Vivian Li
-----
Last Modified:2023/05/06
Modified By:  Siara Small  & Vivian Li
-----
Description: implement file organizer to handle GUI request for file data 
'''

from typing import TypedDict
from gailbot.api import GailBot
from view.signal.interface import FileDataSignal
from controller.Request import Request
from gbLogger import makeLogger
from controller.util.Error import  ERR
from PyQt6.QtCore import QObject, pyqtSignal
from .DataOrganizer import DataOrganizer

    
class FileDict(TypedDict):
    """ the scheme of file data, 
        a file is posted to the database through a dictionary that 
        follows this scheme
    """
    Name    : str
    Type    : str
    Profile : str
    Status  : str
    Date    : str
    Output  : str
    FullPath: str
    Progress: str
    
class Signals(QObject):
    """ 
        contains pyqtSignal to support communication between 
        file database and view 
    """
    error          = pyqtSignal(str)
    
class FileOrganizer(DataOrganizer):
    def __init__(self, gb: GailBot, fileSignal: FileDataSignal) -> None:
        """ 
        Args:
            gb (GailBot): an instance of GailBot api
            fileSignal (FileDataSignal): an instance of FileDataSignal object 
                                       which will emit signal for request 
                                       related to file data 
        """
        super().__init__(gb, fileSignal)
    
    def registerSignal(self, signal: FileDataSignal):
        """ connect signal to the handler functions 

        Args:
            signal (FileDataSignal): an instance of FileDataSignal that stores signals
                                 related to file data 
        """
        signal.fileProfileRequest.connect(self.requestProfile)
        signal.changeFileProfileRequest.connect(self.editFileProfile)
        signal.postRequest.connect(self.postHandler)
        signal.deleteRequest.connect(self.deleteHandler)
        signal.viewOutputRequest.connect(self.viewOutput)
    
    ##########################  request handler ###########################
    def postHandler(self, request : Request) -> None:
        """ add file to file database 
        data: (FileDict) a dictionary that contains the file data to be 
              added to the database
        """
        self.logger.info("postHandler file to database")
        self.logger.info(request.data)
        file : FileDict = request.data
        
        try:
            name = self.gb.add_source(file["FullPath"], file["Output"])
            assert name 
            request.data["Name"] = name
            request.succeed((name, request.data))
            
            assert self.gb.apply_setting_to_source(name, file["Profile"])
        except Exception as e:
            request.fail(ERR.POST_FILE_ERROR)
            self.logger.error(f"Error in posting file: {e}", exc_info=e)
    
    
    def deleteHandler(self, request: Request) -> None:
        """deleteHandler the file from the database
        Args:
            key (str): the file key of the file to be deleted 
        """
        self.logger.info("deleteHandler file from database")
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
 
'''
File: profileDB.py
Project: GailBot GUI
File Created: Friday, 4th November 2022 1:01:27 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Sunday, 13th November 2022 9:06:38 am
Modified By:  Siara Small  & Vivian Li
-----
Description:
Implementation of a database that stores the profile data
'''
from view.signal.interface import DataSignal
from controller.Request import Request
from gailbot.api import GailBot
from gbLogger import makeLogger
from controller.util.Error import ERR

class ProfileOrganizer:
    def __init__(self, gb: GailBot, profileSignal: DataSignal) -> None:
        self.logger = makeLogger("B")
        self.gb = gb
        self.logger.info(f"front end profile organizer initialized, the default setting is {self.gb.get_default_profile_setting_name()}") 
        self.registerSignal(profileSignal)
    
    def registerSignal(self, signal: DataSignal):
       signal.postRequest.connect(self.postHandler)
       signal.deleteRequest.connect(self.deleteHandler)
       signal.getRequest.connect(self.getHandler)
       signal.editRequest.connect(self.editHandler)
       signal.viewSourceRequest.connect(self.viewSourceHandler)
       
    def postHandler(self,postRequest: Request) -> None :
        """ post a new profile to profile database

        Args:
            profile (Tuple[profile name, dict]): a tuple that stores the profile name 
                                                 and profile data
        """
        self.logger.info(f"received post request")
        name, data = postRequest.data
        data = data.copy() 
        try:
            if self.gb.is_setting(name): 
                postRequest.fail(ERR.DUPLICATED_NAME.format(name)) 
                self.logger.error(ERR.DUPLICATED_NAME.format(name))
            elif not self.gb.create_new_setting(name, data):
                postRequest.fail(ERR.INVALID_PROFILE.format(name)) 
                self.logger.error(ERR.INVALID_PROFILE.format(name))
            else:
                self.logger.info(f"New profile created {name}, {data}")
                postRequest.succeed(postRequest.data)
        except Exception as e:
            postRequest.fail(ERR.SAVE_PROFILE.format(name))
            self.logger.error(f"Creating new profile error {e}", exc_info=e)
        
    def deleteHandler(self, deleteRequest: Request) -> None :
        """ delete a file from database 

        Args:
            name (str): the profile name that identified the profile  
                              to be deleted
        """
        name = deleteRequest.data
        self.logger.info(f"deleting profile {name}")
        self.logger.info(f"the default setting is {self.gb.get_default_profile_setting_name()}")
        if not self.gb.is_setting(name):
            deleteRequest.fail(ERR.PROFILE_NOT_FOUND.format(name))
            self.logger.error(ERR.PROFILE_NOT_FOUND.format(name))
        elif name == self.gb.get_default_profile_setting_name():
            deleteRequest.fail(ERR.DELETE_DEFAULT)
            self.logger.error(ERR.DELETE_DEFAULT)
        elif self.gb.is_setting_in_use(name):
            deleteRequest.fail(ERR.PROFILE_IN_USE.format(name))
            self.logger.error(ERR.PROFILE_IN_USE.format(name)) 
        elif not self.gb.remove_setting(name):
            deleteRequest.fail(ERR.DELETE_PROFILE.format(name))
            self.logger.error(ERR.DELETE_PROFILE.format(name))
        else:
            deleteRequest.succeed(name)
    
    def editHandler(self, editRequest: Request) -> None :
        """ update a file
        Args:
            profile (Tuple[name, dict]): a name that identified the profile 
                                        and new profile
        """
        try:
            name, data = editRequest.data
            if not self.gb.is_setting(name):
                editRequest.fail(ERR.PROFILE_NOT_FOUND.format(name))
                self.logger.error(ERR.PROFILE_NOT_FOUND.format(name))
            elif not self.gb.update_setting(name, data):
                editRequest.fail(ERR.PROFILE_EDIT.format(name))
                self.logger.error(ERR.PROFILE_EDIT.format(name))
        except Exception as e:
            editRequest.fail(ERR.PROFILE_EDIT.format(name))
            self.logger.error(e, exc_info=e)
        else:
            editRequest.succeed(editRequest.data)
     
    def getHandler(self, getRequest: Request) -> None:
        """ 
        Args: send a signal that stores the profile information
            name (str): the profile name that identifies a profile 
        """
        name = getRequest.data
        try:
            if not self.gb.is_setting(name):
                getRequest.fail(ERR.PROFILE_NOT_FOUND.format(name))
                self.logger.error(KeyError)
            else:
                data = self.gb.get_setting_dict(name)
                getRequest.succeed((name, data))
        except Exception as e:
            getRequest.fail(ERR.GET_PROFILE.format(name))
            self.logger.error(e, exc_info=e)
            
    def viewSourceHandler(self, viewRequest: Request) -> None:
        name = viewRequest.data 
        try:
            path = self.gb.get_profile_src_path(name)
            viewRequest.succeed(path)
        except Exception as e:
            viewRequest.fail(
                ERR.PROFILE_SRC_CODE.format(viewRequest.data, str(e)))
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
from .DataOrganizer import DataOrganizer

class ProfileOrganizer(DataOrganizer):
    def __init__(self, gb: GailBot, profileSignal: DataSignal) -> None:
        """ 
        Args:
            gb (GailBot): an instance of GailBot api
            profileSignal (DataSignal): an instance of DataSignal object 
                                       which will emit signal for request 
                                       related to profile data 
        """
        super().__init__(gb, profileSignal)
       
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
        response to the get request with the corresponding profile data 
        from the gailbot api
        
        Args: 
            request (Request): 
                request.data : name of the profile 
                request.succeed: a function that accept a dictionary that 
                                 stores the profile data 
                request.fail: a failure continuation that accept a failure 
                              message as a string 
                
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
            
    def viewSourceHandler(self, request: Request) -> None:
        """ 
        response the request to view source with the source path 
        from gailbot api 

        Args:
            request (Request): 
                request.data : name of the source 
                request.succeed: a function that accept a string that stores 
                                 the path to the source file
                request.fail: a failure continuation that accept a failure 
                              message as a string 
        """
        name = request.data 
        try:
            path = self.gb.get_profile_src_path(name)
            request.succeed(path)
        except Exception as e:
            request.fail(
                ERR.PROFILE_SRC_CODE.format(request.data, str(e)))

                
    
    def getAllNamesHandler(self, request: Request) -> None:
        """ given a request that includes a success and failure continuation 
            response with the list of available profile names 
            
            Args: 
                request(Request): an instance of request object that stores  
                                  success and failure continuation, 
                                  the success continuation will be a function 
                                  that expect to receive a list of available 
                                  profile names as the input argument
        """
        try:
            names = self.gb.get_all_profile_names()
            request.succeed(names)
        except Exception as e :
            request.fail(
                ERR.GET_PROFILE.format("all profile names")
            )
            self.logger.error(e, exc_info=e)
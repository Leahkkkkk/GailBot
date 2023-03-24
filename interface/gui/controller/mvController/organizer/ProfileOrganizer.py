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


from typing import Tuple, Union, Dict

from gailbot.api import GailBot
from gbLogger import makeLogger
from controller.util.Error import ERR

from PyQt6.QtCore import QObject, pyqtSignal 

class Signals(QObject):
    """ signals sent by profile model """
    send    = pyqtSignal(tuple)
    deleteProfile  = pyqtSignal(str)  
    deleted = pyqtSignal(bool)
    error   = pyqtSignal(str)
    success = pyqtSignal(str)
    profileAdded = pyqtSignal(str)
    
    
class ProfileOrganizer:
    """ implementation of the Profile database
    
    Field:
    1. data : a dictionary that stores the profile data 
    2. profilekeys: a list of profile names that are currently available 
                    in the database
    3. signals: a signal object for communication between the database 
                and the caller, the caller should support function from
                view object to handle signal emitted by the profile database
    
    
    Public function:
    Database modifier: 
    1. post(self, profile: Tuple[str, dict]) -> None 
    2. delete(self, name:str) -> None
    
    Profile modifier:
    3. edit(self, profile: Tuple[str, dict]) -> None 
    
    Database access: 
    4. get(self, name:str) -> None 
    """
    def __init__(self, gb: GailBot) -> None:
        self.logger = makeLogger("B")
        self.logger.info("the setting data {self.data}")         
        self.signals = Signals()
        self.gb = gb
        self.logger.info(f"front end profile organizer initialized, the default setting is {self.gb.get_default_setting_name()}") 
    
    def post(self, profile: Tuple[str, dict]) -> None :
        """ post a new profile to profile database

        Args:
            profile (Tuple[profile name, dict]): a tuple that stores the profile name 
                                                 and profile data
        """
        name, data = profile
        data = data.copy() 
        try:
            if self.gb.is_setting(name): 
                self.signals.error.emit(ERR.DUPLICATED_NAME.format(name)) 
                self.logger.error(ERR.DUPLICATED_NAME.format(name))
            elif not self.gb.create_new_setting(name, data):
                self.signals.error.emit(ERR.INVALID_PROFILE.format(name)) 
                self.logger.error(ERR.INVALID_PROFILE.format(name))
            elif not self.gb.save_setting(name):
                self.signals.error.emit(ERR.SAVE_PROFILE.format(name))
                self.logger.error(ERR.SAVE_PROFILE.format(name))
            else:
                self.logger.info(f"New profile created {name}, {data}")
                self.signals.profileAdded.emit(name)
        except Exception as e:
            self.logger.error(f"Creating new profile error {e}", exc_info=e)
        
    def delete(self, name:str) -> None :
        """ delete a file from database 

        Args:
            name (str): the profile name that identified the profile  
                              to be deleted
        """
        self.logger.info(f"deleting profile {name}")
        self.logger.info(f"the default setting is {self.gb.get_default_setting_name()}")
        if not self.gb.is_setting(name):
            self.signals.error.emit(ERR.PROFILE_NOT_FOUND.format(name))
            self.logger.error(ERR.PROFILE_NOT_FOUND.format(name))
        elif name == self.gb.get_default_setting_name():
            self.signals.error.emit(ERR.DELETE_DEFAULT)
            self.logger.error(ERR.DELETE_DEFAULT)
        elif not self.gb.remove_setting(name):
            self.signals.error.emit(ERR.DELETE_PROFILE.format(name))
            self.logger.error(ERR.DELETE_PROFILE.format(name))
        else:
            self.signals.deleteProfile.emit(name)
            self.signals.deleted.emit(True)
    
    def edit(self, profile: Tuple[str, dict]) -> None :
        """ update a file
        Args:
            profile (Tuple[name, dict]): a name that identified the profile 
                                        and new profile
        """
        try:
            name, data = profile
            if not self.gb.is_setting(name):
                self.signals.error.emit(ERR.PROFILE_NOT_FOUND.format(name))
                self.logger.error(ERR.PROFILE_NOT_FOUND.format(name))
            elif not self.gb.update_setting(name, data):
                self.signals.error.emit(ERR.PROFILE_EDIT.format(name))
                self.logger.error(ERR.PROFILE_EDIT.format(name))
        except Exception as e:
            self.signals.error.emit(ERR.PROFILE_EDIT.format(name))
            self.logger.error(e, exc_info=e)
     
    def get(self, name:str) -> None:
        """ 
        Args: send a signal that stores the profile information
            name (str): the profile name that identifies a profile 
        """
        try:
            if not self.gb.is_setting(name):
                self.signals.error.emit(ERR.PROFILE_NOT_FOUND.format(name))
                self.logger.error(KeyError)
            else:
                data = self.gb.get_setting_dict(name)
                self.signals.send.emit((name, data))
        except Exception as e:
            self.signals.error.emit(ERR.GET_PROFILE.format(name))
            self.logger.error(ERR.GET_PROFILE.format(name))
            

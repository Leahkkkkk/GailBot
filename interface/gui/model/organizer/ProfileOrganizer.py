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
from util.Logger import makeLogger
from config.Setting import ProfilePreset
from util.Error import ErrorMsg

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
    2. delete(self, profilekey:str) -> None
    
    Profile modifier:
    3. edit(self, profile: Tuple[str, dict]) -> None 
    
    Database access: 
    4. get(self, profilekey:str) -> None 
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
            profile (Tuple[profile name, dict]): _description_
        """
        name, data = profile
        data = data.copy() 
        try:
            if self.gb.is_setting(name): 
                self.signals.error.emit("duplicated profile name") 
                self.logger.error(f"Duplicated profile name {name}")
            elif not self.gb.create_new_setting(name, data):
                self.signals.error.emit("not a valid profile") 
                self.logger.error(f"not a valid profile") 
            elif not self.gb.save_setting(name):
                self.signals.error.emit("profile cannot be saved locally")
                self.logger.error(f"profile cannont be saved locally")
            else:
                self.logger.info(f"New profile created {name}, {data}")
                self.signals.profileAdded.emit(name)
        except Exception as e:
            self.logger.error(f"Creating new profile error {e}")
        
    def delete(self, profilekey:str) -> None :
        """ delete a file from database 

        Args:
            profilekey (str): the profile name that identified the profile  
                              to be deleted
        """
        self.logger.info(f"deleting profile {profilekey}")
        self.logger.info(f"the default setting is {self.gb.get_default_setting_name()}")
        if not self.gb.is_setting(profilekey):
            self.signals.error.emit(f"The setting profile {profilekey} does not exist")
            self.logger.error(ErrorMsg.KEYERROR)
        elif profilekey == self.gb.get_default_setting_name():
            self.signals.error.emit(ErrorMsg.DELETE_DEFAULT)
            self.logger.error(ErrorMsg.DELETE_DEFAULT)
        elif not self.gb.remove_setting(profilekey):
            self.signals.error.emit(f"Error: the profile {profilekey} cannot be deleted")
            self.logger.error(f"profile {profilekey} cannot be deleted")
        else:
            self.signals.deleteProfile.emit(profilekey)
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
                self.signals.error.emit(ErrorMsg.KEYERROR)
                self.logger.error(KeyError)
            elif not self.gb.update_setting(name, data):
                self.signals.error.emit(f"Updating setting {name} failed")
                self.logger.error(f"Error updating setting {name}")
        except Exception as e:
            self.signals.error.emit(ErrorMsg.EDITERROR)
            self.logger.error(f"error in updating the profile setting {e}")
     
    def get(self, profilekey:str) -> None:
        """ 
        Args:
            profilekey (str): _description_
        """
        try:
            if not self.gb.is_setting(profilekey):
                self.signals.error.emit(ErrorMsg.KEYERROR)
                self.logger.error(KeyError)
            else:
                data = self.gb.get_setting_dict(profilekey)
                self.signals.send.emit((profilekey, data))
        except Exception as e:
            self.signals.error.emit(ErrorMsg.GETERROR)
            self.logger.error(f"error getting the profile {e}")
            

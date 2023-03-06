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
    delete  = pyqtSignal(str)  
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
        self.data: Dict[str, Dict] = gb.get_all_settings_data()  
        self.logger.info("the setting data {self.data}")         
        self.profilekeys = list(self.data) 
        self.signals = Signals()
        self.gb = gb
    
    def post(self, profile: Tuple[str, dict]) -> None :
        """ post a new profile to profile database

        Args:
            profile (Tuple[profile name, dict]): _description_
        """
        name, data = profile
        data = data.copy() 
        try:
            if name in self.data or self.gb.is_setting(name): 
                self.signals.error.emit("duplicated profile name") 
                self.logger.error(f"Duplicated profile name {name}")
            elif not self.gb.create_new_setting(name, data):
                self.signals.error.emit("not a valid profile") 
                self.logger.error(f"not a valid profile") 
            else:
                self.data[name] = data
                self.logger.info(f"New profile created {name}, {data}")
                self.signals.profileAdded.emit(name)
        except Exception as e:
            self.logger.error("Creating new profile error {e}")
        
    def delete(self, profilekey:str) -> None :
        """ delete a file from database 

        Args:
            profilekey (str): the profile name that identified the profile  
                              to be deleted
        """
        if profilekey not in self.data or not self.gb.remove_setting(profilekey):
            self.signals.error.emit(ErrorMsg.KEYERROR)
            self.logger.error(ErrorMsg.KEYERROR)
        else:
            del self.data[profilekey]
            self.signals.delete(profilekey)
    
    def edit(self, profile: Tuple[str, dict]) -> None :
        """ update a file
        Args:
            profile (Tuple[name, dict]): a name that identified the profile 
                                        and new profile
        """
        try:
            name, data = profile
            if name not in self.data:
                self.signals.error.emit(ErrorMsg.KEYERROR)
                self.logger.error(KeyError)
            elif not self.gb.update_setting(name, data):
                self.signals.error.emit(f"Updating setting {name} failed")
                self.logger.error(f"Error updating setting {name}")
            else:
                self.data[name] = data
        except Exception as e:
            self.signals.error.emit(ErrorMsg.EDITERROR)
            self.logger.error(e)
     
    def get(self, profilekey:str) -> None:
        """ 
        Args:
            profilekey (str): _description_
        """
        try:
            if profilekey not in self.data:
                self.signals.error.emit(ErrorMsg.KEYERROR)
                self.logger.error(KeyError)
                self.logger.info(self.data[profilekey])
            else:
                self.signals.send.emit((profilekey, self.data[profilekey]))
        except:
            self.signals.error(ErrorMsg.GETERROR)
            self.logger.error(ErrorMsg.GETERROR)

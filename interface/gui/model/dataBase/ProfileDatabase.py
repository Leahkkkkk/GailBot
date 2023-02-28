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

from util.Logger import makeLogger
from util.Setting import ProfilePreset
from util.Error import ErrorMsg

from PyQt6.QtCore import QObject, pyqtSignal 

class Signals(QObject):
    """ signals sent by profile model """
    send    = pyqtSignal(tuple)
    delete  = pyqtSignal(str)  
    error   = pyqtSignal(str)
    success = pyqtSignal(str)
    profileAdded = pyqtSignal(str)
    
    
class ProfileModel:
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
    def __init__(self) -> None:
        self.logger = makeLogger("B")
        self.data = ProfilePreset              
        self.profilekeys = list(ProfilePreset) 
        self.signals = Signals()
    
    def post(self, profile: Tuple[str, dict]) -> None :
        """ post a new profile to profile database

        Args:
            profile (Tuple[profile key, dict]): _description_
        """
        key, data = profile 
        if key not in self.data: 
            self.data[key] = data
            self.logger.info(key)
            self.logger.info(data)
            self.signals.profileAdded.emit(key)
        else:
            self.signals.error.emit("duplicated profile name") 
    

    def delete(self, profilekey:str) -> None :
        """ delete a file from database 

        Args:
            profilekey (str): the profile key that identified the profile  
                              to be deleted
        """
        
        if profilekey not in self.data:
            self.signals.error.emit(ErrorMsg.KEYERROR)
            self.logger.error(ErrorMsg.KEYERROR)
        else:
            del self.data[profilekey]
    
    def edit(self, profile: Tuple[str, dict]) -> None :
        """ update a file
        Args:
            profile (Tuple[key, dict]): a key that identified the profile 
                                        and new profile
        """
        try:
            key, data = profile
            if key not in self.data:
                self.signals.error.emit(ErrorMsg.KEYERROR)
                self.logger.error(KeyError)
            else:
                self.data[key] = data
        except:
            self.signals.error.emit(ErrorMsg.EDITERROR)
            self.logger.error(ErrorMsg.EDITERROR)
    
    
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

    def get_profile(self, profilekey: str) -> Union[Dict, bool]:
        if profilekey in self.data:
            self.logger.info(self.data[profilekey])
            return self.data[profilekey]
        else:
            return False
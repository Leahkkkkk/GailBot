from ast import Delete
from typing import TypedDict, Tuple

from model.dummySettingData import dummySettingForms, dummySettingValues
from PyQt6.QtCore import QObject, pyqtSignal 


KEYERROR = "profile not found"

class Signals(QObject):
    """ signals sent by profile model """
    send = pyqtSignal(tuple)
    deleted  = pyqtSignal(str)  
    error = pyqtSignal(str)
    success = pyqtSignal(str)
    profileAdded = pyqtSignal(str)
    
    
class ProfileModel:
    """ database for profile  """
    def __init__(self) -> None:
        self.data = dummySettingValues              #TODO: for testing delete 
        self.profilekeys = list(dummySettingValues) #TODO: for testing delete
        self.signals = Signals()
    
    def post(self, profile: Tuple[str, dict]):
        """ post a new profile to profile database

        Args:
            profile (Tuple[profile key, dict]): _description_
        """
        key, data = profile 
        if key not in self.data: 
            self.data[key] = data
            self.signals.success.emit("profile added")
            self.signals.profileAdded.emit(key)
        else:
            self.signals.error.emit("duplicated profile name") 
    

    def delete(self, profilekey:str):
        """ delete a file from database 

        Args:
            profilekey (str): the profile key that identified the profile  
                              to be deleted
        """
        if profilekey not in self.data:
            self.signals.error.emit(KEYERROR) 
        else:
            del self.data[profilekey]
    
    def edit(self, profile: Tuple[str, dict]):
        """ update a file
        Args:
            profile (Tuple[key, dict]): a key that identified the profile 
                                        and new profile
        """
        key, data = profile
        if key not in self.data:
            self.signals.error.emit(KEYERROR)
        else:
            self.data[key] = data
    
    
    def get(self, profilekey:str):
        """ 
        Args:
            profilekey (str): _description_
        """
        if profilekey not in self.data:
            self.signals.error.emit(KEYERROR)
        else:
            self.signals.send.emit((profilekey,self.data[profilekey]))
from typing import Tuple

from util.Logger import makeLogger
from model.dummySettingData import dummySettingValues
from util.Error import ErrorMsg, DBExecption

from PyQt6.QtCore import QObject, pyqtSignal 

class Signals(QObject):
    """ signals sent by profile model """
    send    = pyqtSignal(tuple)
    delete  = pyqtSignal(str)  
    error   = pyqtSignal(str)
    success = pyqtSignal(str)
    profileAdded = pyqtSignal(str)
    
    
class ProfileModel:
    """ database for profile  """
    def __init__(self) -> None:
        
        self.logger = makeLogger("Database")
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
            self.signals.error.emit(ErrorMsg.KEYERROR)
            self.logger.error(ErrorMsg.KEYERROR)
        else:
            del self.data[profilekey]
    
    def edit(self, profile: Tuple[str, dict]):
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
    
    
    def get(self, profilekey:str):
        """ 
        Args:
            profilekey (str): _description_
        """
        try:
            if profilekey not in self.data:
                self.signals.error.emit(ErrorMsg.KEYERROR)
                self.logger.error(KeyError)
            else:
                self.signals.send.emit((profilekey, self.data[profilekey]))
        except:
            self.signals.error(ErrorMsg.GETERROR)
            self.logger.error(ErrorMsg.GETERROR)
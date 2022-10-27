from ast import Delete
from typing import TypedDict, Tuple

from model.dummySettingData import dummySettingForms, dummySettingValues
from PyQt6.QtCore import QObject, pyqtSignal 


KEYERROR = "profile not found"


class Signals(QObject):
    send = pyqtSignal(object)
    deleted  = pyqtSignal(str)  
    error = pyqtSignal(str)
    success = pyqtSignal(str)
    profileAdded = pyqtSignal(str)
    
    
class ProfileModel:
    def __init__(self) -> None:
        self.form = dummySettingForms
        self.data = dummySettingValues              #TODO: for testing delete 
        self.profilekeys = list(dummySettingValues) #TODO: for testing delete
        self.signals = Signals()
    
    def post(self, profile: Tuple[str, dict]):
        key, data = profile 
        if key not in self.data: 
            self.data[key] = data
            self.signals.success.emit("profile added")
            self.signals.profileAdded.emit(key)
        else:
            self.signals.error.emit("duplicated profile name") 
    

    def delete(self, profilekey:str):
        if profilekey not in self.data:
            self.signals.error.emit(KEYERROR) 
        else:
            del self.data[profilekey]
    
    def edit(self, profile: Tuple[str, dict]):
        key, data = profile
        if key not in self.data:
            self.signals.error.emit(KEYERROR)
        else:
            self.data[key] = data
    
    
    def get(self, profilekey:str):
        if profilekey not in self.data:
            self.signals.error.emit(KEYERROR)
        else:
            self.signals.send.emit(self.data[profilekey])
'''
File: SettingModel.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 9:49:48 am
Modified By:  Siara Small  & Vivian Li
-----
'''

""" to storing setting data
TODO: Create D.S to store user created setting profile
"""
from typing import Dict 
from model.dummySettingData import dummySettingValues, dummySettingForms

from PyQt6.QtCore import pyqtSignal, QObject

class Signals (QObject):
    error = pyqtSignal(str)
    newSetting = pyqtSignal(object)
    updateSetting = pyqtSignal(object)
    sendSetting = pyqtSignal(object)
    
    
class SettingModel:
    """ dummy setting data for testing setting page functionality """
    def __init__(self, settingOptions=None, settingForm=None):
      self.data = dummySettingValues # stores the user's setting data 
      self.form = dummySettingForms
      self.keys = [] # stores a list of keys 
      self.signals = Signals()

    
    def addUserSetting(self, settingkey:str, settingValues:Dict[str, dict]):
        if not settingkey in self.data:
            self.data[settingkey] == settingValues
            self.signals.newSetting.emit({settingkey:settingValues})
        else: 
            self.signals.error.emit("the profile name has been taken")
      
    def updateSetting(self, settingkey:str, settingValues:Dict[str, dict]):
        try:
            if settingkey not in self.data:
                raise KeyError
            else:
                self.data[settingkey] = settingValues
        except KeyError:
            self.signals.error("Profile is not found in the database")
        else: 
            self.signals.updateSetting.emit({settingkey:settingValues})
            
    def getSettings(self, settingkey:str):
        try:
            if settingkey not in self.data:
                raise KeyError
        except KeyError:
            self.signals.error("Profile is not found in the database")
        else:
            self.signals.sendSetting.emit(self.data[settingkey])
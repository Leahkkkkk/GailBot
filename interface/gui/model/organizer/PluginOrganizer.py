
'''
File: pluginDB.py
Project: GailBot GUI
File Created: Sunday, 30th October 2022 7:06:50 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Sunday, 13th November 2022 9:00:57 am
Modified By:  Siara Small  & Vivian Li
-----
Description: implementation of a the plugin database 
'''
from typing import TypedDict, Tuple

from gailbot.api import GailBot
from PyQt6.QtCore import QObject, pyqtSignal


class pluginObject(TypedDict):
    """ the scheme of a plugin data,
        a plugin is poste dto the database through a dictionary object 
        that follows this scheme 
    """
    Name:str 
    Path:str 

class Signals(QObject):
    """ 
        contains pyqtSignal to support communication between 
        plugin database and view 
    """
    send = pyqtSignal(object)
    pluginAdded = pyqtSignal(str)
    error = pyqtSignal(str)


class PluginOrganizer:
    """ Implementation of a plugin database that 
    
    Field:
    1. data: a dictionary that stores the plugin data
    2. signals: a signal object to support communication between the database
                and the caller, the caller should support the functionalities 
                from view to handle the signal emitted by the plugin database
    
    Plugin function:
    Database modifier:
        functions that delete or add file to the database
    1. post(self, plugin: Tuple[str, str]) -> None
    """
    def __init__(self, gbController: GailBot) -> None:
        self.data = dict()
        self.signals = Signals()
        self.gbCotroller = gbController
    
    def post(self, plugin: Tuple[str, str]) -> None: 
        """ add a new pugin to the data base

        Args:
            plugin (Tuple[str, str]): a tuple with the plugin name  and 
                                      the path to the plugin source
        """     
        name, path = plugin 
        if name not in self.data:
            self.data[name] = path
            self.signals.pluginAdded.emit(name)
        else:
            self.signals.error.emit("plugin name has been taken ")
    

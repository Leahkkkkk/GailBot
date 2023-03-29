
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
from controller.util.io import get_name
from controller.util.Error import ERR

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
    pluginDetail = pyqtSignal(object)


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
        self.gb = gbController
    
    def post(self, pluginSuitePath:str) -> None: 
        """ add a new pugin to the data base

        Args:
            pluginSuitePath: a string that stores the path to plugin suite
        """     
        # plugin = self.gb.register_plugin_suite(pluginSuitePath)
        plugin = get_name(pluginSuitePath) 
        if plugin:
            self.signals.pluginAdded.emit(plugin)
        else:
            self.signals.error.emit(ERR.ERROR_WHEN_DUETO.format(
                f"register plugin {get_name(pluginSuitePath)}", "invalid plugin suite"))

    def sendPluginSuiteDetail(self, pluginName:str) -> None:
        details = dict()
        details["suite name"] = pluginName
        details["metadata"] = self.gb.get_plugin_suite_metadata(pluginName)
        details["dependency graph"] = self.gb.get_plugin_suite_dependency_graph(pluginName)
        details["documentation"] = self.gb.get_plugin_suite_documentation_path(pluginName)
        self.signals.pluginDetail.emit(details)
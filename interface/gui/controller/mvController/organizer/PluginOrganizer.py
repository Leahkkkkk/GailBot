
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
from typing import TypedDict, Tuple, Dict

from gailbot.api import GailBot
from PyQt6.QtCore import QObject, pyqtSignal
from controller.util.io import get_name
from controller.util.Error import ERR

class Signals(QObject):
    """ 
        contains pyqtSignal to support communication between 
        plugin database and view 
    """
    send = pyqtSignal(object)
    pluginAdded = pyqtSignal(tuple)
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
    
    def addPlugin(self, pluginSuitePath:str) -> None: 
        """ add a new plugin to the data base

        Args:
            pluginSuitePath: a string that stores the path to plugin suite
        """     
        suite = self.gb.register_plugin_suite(pluginSuitePath)
        # suite = get_name(pluginSuitePath) 
        if suite:
            metaInfo = self.gb.get_plugin_suite_metadata(suite)
            self.signals.pluginAdded.emit((suite, metaInfo))
        else:
            self.signals.error.emit(ERR.ERROR_WHEN_DUETO.format(
                f"register plugin {get_name(pluginSuitePath)}", "invalid plugin suite"))

    def gerPluginSuiteDetail(self, pluginName:str) -> Dict[str, str]:
        details = dict()
        details["suite_name"] = pluginName
        details["metadata"] = self.gb.get_plugin_suite_metadata(pluginName)
        details["dependency_graph"] = self.gb.get_plugin_suite_dependency_graph(pluginName)
        details["documentation"] = self.gb.get_plugin_suite_documentation_path(pluginName)
        self.signals.pluginDetail.emit(details)
        return details

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
from view.Signals import PluginSignals 
from controller.Request import Request
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
    def __init__(self, gbController: GailBot, pluginSignals: PluginSignals) -> None:
        self.data = dict()
        self.signals = Signals()
        self.gb = gbController
        self.registerSignals(pluginSignals)
        
    def registerSignals(self, signals: PluginSignals):
        signals.addRequest.connect(self.addSuite)
        signals.detailRequest.connect(self.getPluginSuiteDetail)
        signals.deleteRequest.connect(self.deleteSuite)
        signals.viewSource.connect(self.viewPluginSuiteSourceCode)
        
    def addSuite(self, addRequest: Request) -> None: 
        """ add a new plugin to the data base

        Args:
            pluginSuitePath: a string that stores the path to plugin suite
        """     
        suites = self.gb.register_plugin_suite(addRequest.data)
        if isinstance(suites, list):
            for suite in suites:
                metaInfo = self.gb.get_plugin_suite_metadata(suite)
                isOfficial = self.gb.is_official_suite(suite)
                addRequest.succeed((suite, metaInfo, isOfficial))
        elif isinstance(suites, str):
            addRequest.fail(suites)
        else:
            self.signals.error.emit(ERR.ERROR_WHEN_DUETO.format(
                f"register plugin", "invalid plugin suite"))

    def deleteSuite(self, deleteRequest: Request) -> None:
        """ delete the plugin

        Args:
            deleteRequest (Request): _description_
        """
        if self.gb.is_suite_in_use(deleteRequest.data):
            deleteRequest.fail(ERR.PLUGIN_IN_USE.format(deleteRequest.data))
            return
        
        if self.gb.is_official_suite(deleteRequest.data):
            deleteRequest.fail(ERR.PLUGIN_OFFICIAL.format(deleteRequest.data))
            return
        
        deleted = self.gb.delete_plugin_suite(deleteRequest.data)
        if deleted:
            deleteRequest.succeed(deleteRequest.data)
        else:
            self.signals.error.emit(ERR.ERROR_WHEN_DUETO.format(
                f"delete plugin suite {deleteRequest.data}", "cannot be deleted"))
    
    def getPluginSuiteDetail(self, detailRequest: Request) -> Dict[str, str]:
        """get the plugin details

        Args:
            detailRequest (Request): _description_

        Returns:
            Dict[str, str]: _description_
        """
        details = dict()
        pluginName = detailRequest.data
        details["suite_name"] = pluginName
        details["metadata"] = self.gb.get_plugin_suite_metadata(pluginName)
        details["dependency_graph"] = self.gb.get_plugin_suite_dependency_graph(pluginName)
        details["documentation"] = self.gb.get_plugin_suite_documentation_path(pluginName)
        detailRequest.succeed(details)
        return details
    
    
    def viewPluginSuiteSourceCode(self, sourceRequest: Request):
        """ handle the request to view suite source code

        Args:
            sourceRequest (Request): the request object that stores the request 
                                      information and the succeed and failure 
                                      continuation 
        """
        try:
            path = self.gb.get_suite_source_path(sourceRequest.data)
            sourceRequest.succeed(path)
        except Exception as e:
            sourceRequest.fail(
                ERR.PLUGIN_SRC_COED.format(sourceRequest.data, str(e)))
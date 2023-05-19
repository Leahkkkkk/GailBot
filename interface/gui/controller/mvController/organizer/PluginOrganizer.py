'''
File: PluginOrganizer.py
Project: GailBot GUI
File Created: 2023/05
Author: Siara Small  & Vivian Li
-----
Last Modified:2023/05/06
Modified By:  Siara Small  & Vivian Li
-----
Description: implement plugin organizer to handle GUI request related to plugin data 
'''
from typing import  Dict
from gailbot.api import GailBot
from view.signal.interface import DataSignal 
from controller.Request import Request
from PyQt6.QtCore import QObject, pyqtSignal
from controller.util.Error import ERR
from gbLogger import makeLogger
from .DataOrganizer import DataOrganizer

class Signals(QObject):
    """ 
        contains pyqtSignal to support communication between 
        plugin database and view 
    """
    send = pyqtSignal(object)
    pluginAdded = pyqtSignal(tuple)
    error = pyqtSignal(str)
    pluginDetail = pyqtSignal(object)

class PluginOrganizer(DataOrganizer):
    def __init__(self, gb: GailBot, pluginSignals: DataSignal) -> None:
        """ 
        Args:
            gb (GailBot): an instance of GailBot api
            pluginSignals (DataSignal): an instance of DataSignal object 
                                       which will emit signal for request 
                                       related to plugin data 
        """
        super().__init__(gb, pluginSignals)
        
    def postHandler(self, addRequest: Request) -> None: 
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
            addRequest.fail(ERR.INVALID_PLUGIN)
    
    def editHandler():
        """
        NOTE: no edit function for plugin has been implemented 
              in the backend yet
        """
        pass 

    def deleteHandler(self, deleteRequest: Request) -> None:
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
            deleteRequest.fail(ERR.DELETE_PLUGIN)
    
    def getHandler(self, detailRequest: Request) -> Dict[str, str]:
        """get the plugin details

        Args:
            detailRequest (Request): _description_

        Returns:
            Dict[str, str]: _description_
        """
        try:
            details = dict()
            pluginName = detailRequest.data
            details["suite_name"] = pluginName
            details["metadata"] = self.gb.get_plugin_suite_metadata(pluginName)
            details["dependency_graph"] = self.gb.get_plugin_suite_dependency_graph(pluginName)
            details["documentation"] = self.gb.get_plugin_suite_documentation_path(pluginName)
            detailRequest.succeed(details)
        except Exception as e:
            detailRequest.fail(ERR.PLUGIN_DETAIL)
        return details
    
    
    def viewSourceHandler(self, sourceRequest: Request):
        """ handle the request to view suite source code

        Args:
            sourceRequest (Request): the request object that stores the request 
                                      information and the succeed and failure 
                                      continuation 
        """
        try:
            path = self.gb.get_suite_source_path(sourceRequest.data)
            assert path
            sourceRequest.succeed(path)
        except Exception as e:
            sourceRequest.fail(
                ERR.PLUGIN_SRC_CODE.format(sourceRequest.data))
        
        
    
    def getAllNamesHandler(self, request: Request) -> None:
        """ given a request that includes a success and failure continuation 
            response with the list of available Engine names 
            
            Args: 
                request(Request): an instance of request object that stores  
                                  success and failure continuation, 
                                  the success continuation will be a function 
                                  that expect to receive a list of available 
                                  engine names as the input argument
        """
        try:
            names = self.gb.get_all_plugin_suites()
            request.succeed(names)
        except Exception as e :
            request.fail(
                ERR.PLUGIN_NAMES
            )
            self.logger.error(e, exc_info=e)
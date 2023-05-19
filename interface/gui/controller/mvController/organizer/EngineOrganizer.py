'''
File: EngineOrganizer.py
Project: GailBot GUI
File Created: 2023/05/01
Author: Siara Small  & Vivian Li
-----
Last Modified:2023/05/06
Modified By:  Siara Small  & Vivian Li
-----
Description: handle GUI request for engine data 
'''
from view.signal.interface import DataSignal
from controller.Request import Request
from gailbot.api import GailBot
from gbLogger import makeLogger
from controller.util.Error import ERR
from .DataOrganizer import DataOrganizer

class EngineOrganizer(DataOrganizer):
    def __init__(self, gb: GailBot, engineSignal: DataSignal) -> None:
        """ 
        Args:
            gb (GailBot): an instance of GailBot api
            engineSignal (DataSignal): an instance of DataSignal object 
                                       which will emit signal for request 
                                       related to engine data 
        """
        super().__init__(gb, engineSignal)
    
    def postHandler(self, request: Request) -> None :
        """ post a file data to the backend database

        Args:
            request (Request): an instance of Request object that stores the 
                                   data to be posted as well as success and failure 
                                   continuation function
        """
        self.logger.info(f"received post request")
        name, data = request.data
        data = data.copy() 
        try:
            if self.gb.is_engine_setting(name): 
                request.fail(ERR.DUPLICATED_NAME.format(name)) 
                self.logger.error(ERR.DUPLICATED_NAME.format(name))
            elif not self.gb.add_new_engine(name, data):
                request.fail(ERR.INVALID_ENGINE.format(name)) 
                self.logger.error(ERR.INVALID_ENGINE.format(name))
            else:
                self.logger.info(f"New engine created {name}, {data}")
                request.succeed(request.data)
        except Exception as e:
            request.fail(ERR.POST_ENGINE.format(name))
            self.logger.error(f"Creating new engine error {e}", exc_info=e)
        
    def deleteHandler(self, request: Request) -> None :
        """ delete a file from database 

        Args:
            name (str): the engine setting name that identified the engine setting  
                              to be deleted
        """
        name = request.data
        self.logger.info(f"deleting engine setting {name}")
        if not self.gb.is_engine_setting(name):
            request.fail(ERR.ENGINE_NOT_FOUND.format(name))
            self.logger.error(ERR.ENGINE_NOT_FOUND.format(name))
        elif name == self.gb.get_default_engine_setting_name():
            request.fail(ERR.DELETE_DEFAULT)
            self.logger.error(ERR.DELETE_DEFAULT)
        elif self.gb.is_engine_setting_in_use(name):
            request.fail(ERR.ENGINE_IN_USE.format(name))
            self.logger.error(ERR.ENGINE_IN_USE.format(name)) 
        elif not self.gb.remove_engine_setting(name):
            request.fail(ERR.DELETE_ENGINE.format(name))
            self.logger.error(ERR.DELETE_ENGINE.format(name))
        else:
            request.succeed(name)
    
    def editHandler(self, request: Request) -> None :
        """ update a file
        """
        try:
            name, data = request.data
            if not self.gb.is_engine_setting(name):
                request.fail(ERR.ENGINE_NOT_FOUND.format(name))
                self.logger.error(ERR.ENGINE_NOT_FOUND.format(name))
            elif not self.gb.update_engine_setting(name, data):
                request.fail(ERR.ENGINE_EDIT.format(name))
                self.logger.error(ERR.ENGINE_EDIT.format(name))
        except Exception as e:
            request.fail(ERR.ENGINE_EDIT.format(name))
            self.logger.error(e, exc_info=e)
        else:
            request.succeed(request.data)
     
    def getHandler(self, request: Request) -> None:
        """ 
        Args: send a signal that stores the engine setting information
            name (str): the engine setting name that identifies a engine setting 
        """
        name = request.data
        try:
            if not self.gb.is_engine_setting(name):
                request.fail(ERR.ENGINE_NOT_FOUND.format(name))
                self.logger.error(KeyError)
            else:
                data = self.gb.get_engine_setting_data(name)
                request.succeed((name, data))
        except Exception as e:
            request.fail(ERR.GET_ENGINE.format(name))
            self.logger.error(e, exc_info=e)
            

    def viewSourceHandler(self, request: Request) -> None:
        """ given a request that specifies the name of the engine, 
            response with the path to the source file

        Args:
            request (Request): an instance of request object that 
                                  stores tha name of the source and the 
                                  success and failure continuation
        """ 
        name = request.data 
        try:
            path = self.gb.get_engine_src_path(name)
            request.succeed(path)
        except Exception as e:
            request.fail(
                ERR.ENGINE_SRC_CODE.format(request.data, str(e)))
            self.logger.error(e, exc_info=e)
    
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
            names = self.gb.get_engine_setting_names()
            request.succeed(names)
        except Exception as e :
            request.fail(
                ERR.GET_ENGINE.format("all engine names")
            )
            self.logger.error(e, exc_info=e)
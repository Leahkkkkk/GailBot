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

class EngineOrganizer:
    def __init__(self, gb: GailBot, engineSignal: DataSignal) -> None:
        """ 
        Args:
            gb (GailBot): an instance of GailBot api
            engineSignal (DataSignal): an instance of DataSignal object 
                                       which will emit signal for request 
                                       related to engine data 
        """
        self.logger = makeLogger()
        self.gb = gb
        self.logger.info(f"front end engine organizer initialized") 
        self.registerSignal(engineSignal)
    
    def registerSignal(self, signal: DataSignal):
       signal.postRequest.connect(self.postHandler)
       signal.deleteRequest.connect(self.deleteHandler)
       signal.getRequest.connect(self.getHandler)
       signal.editRequest.connect(self.editHandler)
       signal.viewSourceRequest.connect(self.viewSourceHandler)
        
    def postHandler(self, postRequest: Request) -> None :
        self.logger.info(f"received post request")
        name, data = postRequest.data
        data = data.copy() 
        try:
            if self.gb.is_engine_setting(name): 
                postRequest.fail(ERR.DUPLICATED_NAME.format(name)) 
                self.logger.error(ERR.DUPLICATED_NAME.format(name))
            elif not self.gb.add_new_engine(name, data):
                postRequest.fail(ERR.INVALID_ENGINE.format(name)) 
                self.logger.error(ERR.INVALID_ENGINE.format(name))
            else:
                self.logger.info(f"New engine created {name}, {data}")
                postRequest.succeed(postRequest.data)
        except Exception as e:
            postRequest.fail(ERR.POST_ENGINE.format(name))
            self.logger.error(f"Creating new engine error {e}", exc_info=e)
        
    def deleteHandler(self, deleteRequest: Request) -> None :
        """ delete a file from database 

        Args:
            name (str): the engine setting name that identified the engine setting  
                              to be deleted
        """
        name = deleteRequest.data
        self.logger.info(f"deleting engine setting {name}")
        if not self.gb.is_engine_setting(name):
            deleteRequest.fail(ERR.ENGINE_NOT_FOUND.format(name))
            self.logger.error(ERR.ENGINE_NOT_FOUND.format(name))
        elif name == self.gb.get_default_engine_setting_name():
            deleteRequest.fail(ERR.DELETE_DEFAULT)
            self.logger.error(ERR.DELETE_DEFAULT)
        elif self.gb.is_engine_setting_in_use(name):
            deleteRequest.fail(ERR.ENGINE_IN_USE.format(name))
            self.logger.error(ERR.ENGINE_IN_USE.format(name)) 
        elif not self.gb.remove_engine_setting(name):
            deleteRequest.fail(ERR.DELETE_ENGINE.format(name))
            self.logger.error(ERR.DELETE_ENGINE.format(name))
        else:
            deleteRequest.succeed(name)
    
    def editHandler(self, editRequest: Request) -> None :
        """ update a file
        """
        try:
            name, data = editRequest.data
            if not self.gb.is_engine_setting(name):
                editRequest.fail(ERR.ENGINE_NOT_FOUND.format(name))
                self.logger.error(ERR.ENGINE_NOT_FOUND.format(name))
            elif not self.gb.update_engine_setting(name, data):
                editRequest.fail(ERR.ENGINE_EDIT.format(name))
                self.logger.error(ERR.ENGINE_EDIT.format(name))
        except Exception as e:
            editRequest.fail(ERR.ENGINE_EDIT.format(name))
            self.logger.error(e, exc_info=e)
        else:
            editRequest.succeed(editRequest.data)
     
    def getHandler(self, getRequest: Request) -> None:
        """ 
        Args: send a signal that stores the engine setting information
            name (str): the engine setting name that identifies a engine setting 
        """
        name = getRequest.data
        try:
            if not self.gb.is_engine_setting(name):
                getRequest.fail(ERR.ENGINE_NOT_FOUND.format(name))
                self.logger.error(KeyError)
            else:
                data = self.gb.get_engine_setting_data(name)
                getRequest.succeed((name, data))
        except Exception as e:
            getRequest.fail(ERR.GET_ENGINE.format(name))
            self.logger.error(e, exc_info=e)
            

    def viewSourceHandler(self, viewRequest: Request) -> None:
        name = viewRequest.data 
        try:
            path = self.gb.get_engine_src_path(name)
            viewRequest.succeed(path)
        except Exception as e:
            viewRequest.fail(
                ERR.PROFILE_SRC_CODE.format(viewRequest.data, str(e)))
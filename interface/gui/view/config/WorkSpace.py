
'''
     File   : GailBotDataParser.py
     Project: GailBot GUI
File Created: Sunday, 6th November 2022 12: 10: 00 pm
     Author : Siara Small  & Vivian Li
-----
Last     Modified: Sunday, 6th November 2022 1: 11: 46 pm
Modified By      : Siara Small  & Vivian Li
-----
'''

""" accesses gailbot configuration values from given dictionaries """
import os 
from typing import TypedDict
from dataclasses import dataclass
from dict_to_dataclass import field_from_dict, DataclassFromDict
from view.util.io import write_toml, is_directory
import toml 
from config_frontend import FRONTEND_CONFIG_ROOT
from config_frontend.ConfigPath import WorkSpaceConfigPath
import userpaths

@dataclass 
class WorkSpacePathData(DataclassFromDict): 
    backend                             : str = field_from_dict()
    frontend                            : str = field_from_dict()
    logFiles                            : str = field_from_dict()
    frontendLogFiles                    : str = field_from_dict()
    backendLogFiles                     : str = field_from_dict()

@dataclass
class LogManageData(DataclassFromDict):
    AUTO_DELETE_TIME: int = field_from_dict() 


class FileManagementData(TypedDict):
    UPLOAD_SRC_DIR: str
    UPLOAD_PLUGIN_DIR: str 
    OUTPUT_DIR: str 

def getWorkBasePath() -> str:
    """  return the base directory of the gailbot workspace """
    userBaseDir = os.path.join(userpaths.get_profile(), "GailBot")
    return userBaseDir

def getWorkPaths() -> WorkSpacePathData:
    """ return the data contains workspace directory  """
    # get the user's defined base directory
    userBaseDir = getWorkBasePath()
    # get the path to the sub directory     
    data = toml.load(os.path.join(FRONTEND_CONFIG_ROOT, WorkSpaceConfigPath.wsStructure))
    for key, value in data.items():
        data[key] = os.path.join(userBaseDir, value)
    WorkSpace = WorkSpacePathData.from_dict(data)
    return WorkSpace

def getLogManagementData() -> LogManageData: 
    fileManage = toml.load(os.path.join(FRONTEND_CONFIG_ROOT, WorkSpaceConfigPath.logManagement))
    FileManage = LogManageData.from_dict(fileManage)
    return FileManage

def getFileManagementData(key) -> str: 
    fileManage = toml.load(os.path.join(FRONTEND_CONFIG_ROOT, WorkSpaceConfigPath.fileManagement))
    path = fileManage[key] 
    if path and is_directory(path):
        return path
    else:
        path = userpaths.get_desktop()
        updateSavedUploadFileDir(path)
        return path
    
def updateFileManagementData(key, path):
    configFile = os.path.join(FRONTEND_CONFIG_ROOT, WorkSpaceConfigPath.fileManagement)
    data = toml.load(configFile)
    data[key] = path
    write_toml(configFile, data)

def getSavedUploadFileDir():
    return getFileManagementData("UPLOAD_SRC_DIR")

def getSavedUploadPluginDir():
    return getFileManagementData("UPLOAD_PLUGIN_DIR")

def getSavedOutputDir():
    return getFileManagementData("OUTPUT_DIR")

def updateSavedUploadFileDir(path:str):
    updateFileManagementData("UPLOAD_SRC_DIR", path) 

def updateSavedUploadSuiteDir(path:str):
    updateFileManagementData("UPLOAD_PLUGIN_DIR", path)
    
def updateSavedOutputDir(path:str):
    updateFileManagementData("OUTPUT_DIR", path)
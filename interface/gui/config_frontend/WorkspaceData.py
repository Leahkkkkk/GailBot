
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
from dataclasses import dataclass
from dict_to_dataclass import field_from_dict, DataclassFromDict

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
class FileManageData(DataclassFromDict):
    AUTO_DELETE_TIME: int = field_from_dict() 

def getWorkBasePath() -> str:
    """  return the base directory of the gailbot workspace """
    userBaseDir = os.path.join(userpaths.get_profile(), "GailBot")
    return userBaseDir

def getWorkPath() -> WorkSpacePathData:
    """ return the data contains workspace directory  """
    # get the user's defined base directory
    userBaseDir = getWorkBasePath()
    # get the path to the sub directory     
    data = toml.load(os.path.join(FRONTEND_CONFIG_ROOT, WorkSpaceConfigPath.wsStructure))
    for key, value in data.items():
        data[key] = os.path.join(userBaseDir, value)
    WorkSpace = WorkSpacePathData.from_dict(data)
    return WorkSpace

def getFileManagementData() -> FileManageData: 
    fileManage = toml.load(os.path.join(FRONTEND_CONFIG_ROOT, WorkSpaceConfigPath.fileManageData))
    FileManage = FileManageData.from_dict(fileManage)
    return FileManage
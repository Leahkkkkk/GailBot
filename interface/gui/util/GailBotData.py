'''
File: GailBotData.py
Project: GailBot GUI
File Created: Sunday, 6th November 2022 12:10:00 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Sunday, 6th November 2022 1:10:02 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: implement a visual component to display progress 
'''
import os 
from dataclasses import dataclass
import toml 
from util.Path import getProjectRoot
from util.ConfigParser.GailBotDataParser import (
    CredentialData, 
    DirectoryData, 
    ProfileConfigData, 
    PluginData, 
    ThreadData,
    WorkSpacePathData,
    WorkSpaceBaseDirData,
    FileManageData
)
from config.ConfigPath import BackEndDataPath

import userpaths

basedir = getProjectRoot()

config = toml.load(os.path.join(basedir, BackEndDataPath.gailBotData))
fileManage = toml.load(os.path.join(basedir, BackEndDataPath.fileManageData))
Credential = CredentialData.from_dict(config["credential"])
ProfileConfig = ProfileConfigData.from_dict(config["profileConfig"])
Plugin = PluginData.from_dict(config["plugin"])
ThreadControl = ThreadData.from_dict(config["threadControl"])
FileManage = FileManageData.from_dict(fileManage)

def getWorkPath() -> WorkSpacePathData:
    """ return the data contains workspace directory  """
    # get the user's defined base directory
    if os.path.exists(os.path.join(basedir,BackEndDataPath.workSpaceData)):
        data = toml.load(os.path.join(basedir,BackEndDataPath.workSpaceData))
        userBaseDir = WorkSpaceBaseDirData.from_dict(data).WORK_SPACE_BASE_DIRECTORY
    else:
        userBaseDir = userpaths.get_profile()
        
    # get the path to the sub directory     
    data = toml.load(os.path.join(basedir, BackEndDataPath.defaultWorkSpaceData))
    for key, value in data.items():
        data[key] = os.path.join(userBaseDir, value)
    WorkSpacePath = WorkSpacePathData.from_dict(data)
    
    return WorkSpacePath


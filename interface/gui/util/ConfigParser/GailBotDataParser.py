
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

from dataclasses import dataclass
from typing import List 
import toml 
from dict_to_dataclass import field_from_dict, DataclassFromDict

from config.ConfigPath import BackEndDataPath

@dataclass
class CredentialData(DataclassFromDict): 
    """ data for watson credential """
    WATSON_API_KEY        : str = field_from_dict()
    WATSON_LANG_CUSTOM_ID : str = field_from_dict()
    WATSON_REGION         : str = field_from_dict()
    WATSON_BASE_LANG_MODEL: str = field_from_dict()
    
@dataclass 
class ProfileConfigData(DataclassFromDict): 
    """ data for creating profile """
    SETTINGS_PROFILE_NAME     : str = field_from_dict()
    SETTINGS_PROFILE_EXTENSION: str = field_from_dict()

@dataclass 
class DirectoryData(DataclassFromDict): 
    """ data for path to directories"""
    PLUGIN_DOWNLOADS        : str = field_from_dict()
    WORKSPACE_DIRECTORY_PATH: str = field_from_dict()
    
@dataclass
class PluginData(DataclassFromDict): 
    """ data for plugin sources """
    PLUGINS_TO_APPLY: List[str] = field_from_dict()
    HIL_PLUGIN_URL  : str       = field_from_dict()

@dataclass 
class ThreadData(DataclassFromDict): 
    """ data for thread control """
    maxThread: int = field_from_dict()

@dataclass 
class WorkSpacePathData(DataclassFromDict): 
    workSpace: str = field_from_dict()
    plugin : str = field_from_dict()
    frontend: str = field_from_dict()
    logFiles: str = field_from_dict()

@dataclass 
class WorkSpaceBaseDirData(DataclassFromDict):
    WORK_SPACE_BASE_DIRECTORY : str = field_from_dict()

@dataclass
class FileManageData(DataclassFromDict):
    AUTO_DELETE_TIME: int = field_from_dict() 
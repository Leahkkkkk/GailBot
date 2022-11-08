'''
File: GailBotData.py
Project: GailBot GUI
File Created: Sunday, 6th November 2022 12:10:00 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Sunday, 6th November 2022 1:10:02 pm
Modified By:  Siara Small  & Vivian Li
-----
'''


'''
File: GailBotData.py
Project: GailBot GUI
File Created: Sunday, 6th November 2022 12:10:00 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Sunday, 6th November 2022 1:11:46 pm
Modified By:  Siara Small  & Vivian Li
-----
'''


from dataclasses import dataclass
from typing import List 
import toml 
from dict_to_dataclass import field_from_dict, DataclassFromDict


config = toml.load("config/backend/gailbot.toml")

@dataclass
class CrendentialData(DataclassFromDict):
    """ data for watson credential """
    WATSON_API_KEY: str =  field_from_dict()
    WATSON_LANG_CUSTOM_ID: str =  field_from_dict()
    WATSON_REGION: str =  field_from_dict()
    WATSON_BASE_LANG_MODEL: str =  field_from_dict()
    
@dataclass 
class ProfileConfigData(DataclassFromDict):
    """ data for creating profile """
    SETTINGS_PROFILE_NAME: str =  field_from_dict()
    SETTINGS_PROFILE_EXTENSION: str =  field_from_dict()

@dataclass 
class DirectoryData(DataclassFromDict):
    """ data for path to directories"""
    PLUGIN_DOWNLOADS: str =  field_from_dict()
    WORKSPACE_DIRECTORY_PATH: str =  field_from_dict()
    

@dataclass
class PluginData(DataclassFromDict):
    """ data for plugin sources """
    PLUGINS_TO_APPLY: List[str] =  field_from_dict()
    HIL_PLUGIN_URL: str  =  field_from_dict()

Crendential = CrendentialData.from_dict(config["credential"])
Directory = DirectoryData.from_dict(config["directory"])
ProfileConfig = ProfileConfigData.from_dict(config["profileConfig"])
Plugin = PluginData.from_dict(config["plugin"])
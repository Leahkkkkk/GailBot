from dataclasses import dataclass
from typing import List 

# from util.Path import getProjectRoot
from os.path import exists
import toml 
from dict_to_dataclass import field_from_dict, DataclassFromDict


config = toml.load("/config/gailBot.toml")



@dataclass
class CrendentialData(DataclassFromDict):
    WATSON_API_KEY: str =  field_from_dict()
    WATSON_LANG_CUSTOM_ID: str =  field_from_dict()
    WATSON_REGION: str =  field_from_dict()
    WATSON_BASE_LANG_MODEL: str =  field_from_dict()
    WORKSPACE_DIRECTORY_PATH: str =  field_from_dict()
    
@dataclass 
class ProfileConfigData(DataclassFromDict):
    SETTINGS_PROFILE_NAME: str =  field_from_dict()
    SETTINGS_PROFILE_EXTENSION: str =  field_from_dict()

@dataclass 
class DirectoryData(DataclassFromDict):
    PLUGIN_DOWNLOADS: str =  field_from_dict()
    WORKSPACE_DIRECTORY_PATH: str =  field_from_dict()
    

@dataclass
class PluginData(DataclassFromDict):
    PLUGIN_TO_APPLY: List[str] =  field_from_dict()
    HIL_PLUGIN_URL: str  =  field_from_dict()

Crendential = CrendentialData.from_dict(config["credential"])
Directory = DirectoryData.from_dict(config["directory"])
ProfileConfig = ProfileConfigData.from_dict(config["profileConfig"])
Plugin = PluginData.from_dict(config["plugin"])
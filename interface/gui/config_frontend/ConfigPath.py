'''
     File   : configPath.py
     Project: GailBot GUI
File Created: Sunday, 13th November 2022 11: 18: 01 am
     Author : Siara Small  & Vivian Li
-----
Last     Modified: Sunday, 13th November 2022 11: 54: 49 am
Modified By      : Siara Small  & Vivian Li
-----
Description: Provides dataclass that stores all paths to configuration files 
'''

import os 
import toml 
from dataclasses import dataclass
from dict_to_dataclass import field_from_dict, DataclassFromDict
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
FRONTEND_CONFIG_ROOT = os.path.join (os.path.dirname (os.path.dirname(__file__)), "config_frontend")
data    = toml.load(os.path.join (FRONTEND_CONFIG_ROOT, "configpath.toml"))

@dataclass 
class WorkSpaceData(DataclassFromDict): 
    wsStructure                   : str = field_from_dict()
    fileManageData                : str = field_from_dict()


@dataclass 
class StyleData(DataclassFromDict): 
    dimension                   : str = field_from_dict()
    fontFamily                  : str = field_from_dict()
    currentColor                : str = field_from_dict()
    darkColor                   : str = field_from_dict()
    lightColor                  : str = field_from_dict()
    currentFontSize             : str = field_from_dict()
    largeFontSize               : str = field_from_dict()
    smallFontSize               : str = field_from_dict()
    mediumFontSize              : str = field_from_dict()

@dataclass 
class TextData(DataclassFromDict): 
    string                     : str = field_from_dict()
    form                       : str = field_from_dict()
    about                      : str = field_from_dict()

@dataclass 
class SettingData(DataclassFromDict): 
    profilePreset               : str = field_from_dict()
    systemSetting               : str = field_from_dict()
    defaultSetting              : str = field_from_dict()

WorkSpaceConfigPath  = WorkSpaceData.from_dict(data["workspace"])
StyleDataPath    = StyleData.from_dict(data["style"])
TextDataPath     = TextData.from_dict(data["text"])
SettingDataPath  = SettingData.from_dict(data["setting"])

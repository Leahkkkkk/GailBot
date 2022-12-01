'''
     File   : configPath.py
     Project: GailBot GUI
File Created: Sunday, 13th November 2022 11: 18: 01 am
     Author : Siara Small  & Vivian Li
-----
Last     Modified: Sunday, 13th November 2022 11: 54: 49 am
Modified By      : Siara Small  & Vivian Li
-----
Description: 
'''

import os 
import toml 
from util.Path import getProjectRoot
from dataclasses import dataclass
from dict_to_dataclass import field_from_dict, DataclassFromDict

basedir = getProjectRoot()
data    = toml.load(os.path.join (basedir, "config/configpath.toml"))

@dataclass 
class BackEndData(DataclassFromDict): 
    gailBotData                  : str = field_from_dict()
    workSpaceData                : str = field_from_dict()
    defaultWorkSpaceData         : str = field_from_dict()
    fileManageData               : str = field_from_dict()

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
class PresetData(DataclassFromDict): 
    profilePreset               : str = field_from_dict()

BackEndDataPath = BackEndData.from_dict(data["backend"])
StyleDataPath   = StyleData.from_dict(data["style"])
TextDataPath    = TextData.from_dict(data["text"])
PresetDataPath  = PresetData.from_dict(data["preset"])

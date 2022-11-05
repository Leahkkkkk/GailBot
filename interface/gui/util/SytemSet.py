from dataclasses import dataclass
from typing import List 
import os 
import toml 
from dict_to_dataclass import DataclassFromDict, field_from_dict

config = toml.load("config/default.toml")

@dataclass 
class SysColorData(DataclassFromDict):
    maintext: str = field_from_dict()
    background: str = field_from_dict()
    subBackground: str = field_from_dict()
    
@dataclass 
class SysImagesData(DataclassFromDict):
    homeBackground: str = field_from_dict()
    subPageBackground: str = field_from_dict()

@dataclass 
class SysFonsizeData(DataclassFromDict):
    body: str = field_from_dict()
@dataclass 
class SysStyleSheetData(DataclassFromDict):
    basic: str = field_from_dict()
    
SysColor     = SysColorData.from_dict(config["sysColor"])
SysImage     = SysImagesData.from_dict(config["sysImages"])
SysFontSize  = SysFonsizeData.from_dict(config["sysFontSize"])
SysStyleSheet = SysStyleSheetData.from_dict(config["sysStyleSheet"])
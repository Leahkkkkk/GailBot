"""
File: Forms.py
Project: GailBot GUI
File Created: Tuesday, 1st November 2022 3:59:15 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Saturday, 18th March 5:04:12 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: Dataclasses that stores the profile form as dictionary 
"""
import toml
import os
from dataclasses import dataclass
from view.config.Style import Color
from dict_to_dataclass import DataclassFromDict, field_from_dict
from config_frontend.ConfigPath import TextDataPath, FRONTEND_CONFIG_ROOT

forms  = toml.load(os.path.join(FRONTEND_CONFIG_ROOT, TextDataPath.form))

@dataclass
class ProfileSetting(DataclassFromDict):
    """class holding the text for the setting page"""
    RequiredSetting: dict = field_from_dict()
    PostTranscribe : dict = field_from_dict() 
    Plugins        : dict = field_from_dict()

@dataclass 
class EngineSetting(DataclassFromDict):
    """class holding the text for the engine setting page"""
    Engine: dict = field_from_dict()

ProfileSettingForm = ProfileSetting.from_dict(forms["profile form"])
EngineSettingForm  = EngineSetting.from_dict(forms["profile form"]["RequiredSetting"])
SystemSettingForm  = forms["system setting form"]
LOG_DELETE  = forms["log deletion"]
RECORD_FORM         = forms["record form"]
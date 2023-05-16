'''
File: Preset.py
Project: GailBot GUI
File Created: Sunday, 13th November 2022 11:29:22 am
Author: Siara Small  & Vivian Li
-----
Last Modified: Sunday, 13th November 2022 11:59:48 am
Modified By:  Siara Small  & Vivian Li
-----
Description: contain instance of data class with preset data 
'''


import os 
import toml 
from config_frontend.ConfigPath import SettingDataPath, FRONTEND_CONFIG_ROOT
ProfilePreset  = toml.load(os.path.join(FRONTEND_CONFIG_ROOT, SettingDataPath.profilePreset))
SystemSetting  = toml.load(os.path.join(FRONTEND_CONFIG_ROOT, SettingDataPath.systemSetting))
DefaultSetting = toml.load(os.path.join(FRONTEND_CONFIG_ROOT, SettingDataPath.defaultSetting))
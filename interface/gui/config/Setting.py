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
from config.Path import getProjectRoot
from config_gui.ConfigPath import SettingDataPath

basedir = getProjectRoot()
ProfilePreset =  toml.load(os.path.join(basedir, SettingDataPath.profilePreset))
SystemSetting = toml.load(os.path.join(basedir, SettingDataPath.systemSetting))
DefaultSetting = toml.load(os.path.join(basedir, SettingDataPath.defaultSetting))
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
import os 
import toml 
from util.Path import getProjectRoot
from util.ConfigParser.GailBotDataParser import (
    CredentialData, 
    DirectoryData, 
    ProfileConfigData, 
    PluginData, 
    ThreadData
)
from config.ConfigPath import BackEndDataPath

basedir = getProjectRoot()
config = toml.load(os.path.join(basedir,BackEndDataPath.gaiBotData))
Credential = CredentialData.from_dict(config["credential"])
Directory = DirectoryData.from_dict(config["directory"])
ProfileConfig = ProfileConfigData.from_dict(config["profileConfig"])
Plugin = PluginData.from_dict(config["plugin"])
ThreadControl = ThreadData.from_dict(config["threadControl"])
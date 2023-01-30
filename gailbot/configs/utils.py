# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-10 12:37:45
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-15 16:07:38


""" reading the toml file and initialize the instances of the dataclass  
    whose interfaces are provided by the configparser 
"""
from gailbot.configs.configparser import engines, settings 

WATSON_DATA = engines.Watson() 
SETTING_DATA = settings.Setting

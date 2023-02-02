# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-31 15:29:08
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-31 15:37:25

from ..confs.paths import PATH, CONFIG_ROOT
from .core.engines.watson import load_watson_config 
from .core.engines.google import load_google_config
from .core.setting.defaults import load_default_config
from .core.util.logger import load_log_config
import os 

""" TODO: change to all like this  """
watson_config_loader = lambda : load_watson_config(os.path.join(CONFIG_ROOT, PATH.watson))
google_config_loader = lambda : load_google_config(os.path.join(CONFIG_ROOT, PATH.google))
default_config_loader = lambda: load_default_config(os.path.join(CONFIG_ROOT, PATH.default))
log_config_loader = lambda: load_log_config(os.path.join(CONFIG_ROOT, PATH.log))
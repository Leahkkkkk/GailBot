# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-31 15:29:08
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-31 15:37:25

from ..confs.paths import PATH, CONFIG_ROOT
from .core.engines.watson import load_watson_config 
from .core.engines.google import load_google_config
from .core.setting.defaults import load_default_config
import os 
WATSON_DATA = load_watson_config(os.path.join(CONFIG_ROOT, PATH.watson))
GOOGLE_DATA = load_google_config(os.path.join(CONFIG_ROOT, PATH.google))
DEFAULT_DATA = load_default_config(os.path.join(CONFIG_ROOT, PATH.default))
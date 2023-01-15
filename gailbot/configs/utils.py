# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-10 12:37:45
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-15 16:07:38

import sys
import os
from typing import Dict

def get_root_dir() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_config_dir() -> str :
    return os.path.dirname(os.path.abspath(__file__))

def get_base_conf_path() -> str:
    return os.path.join(get_config_dir(),"conf.toml")

def get_base_conf() -> Dict:
    pass

def get_engine_conf(engine_name : str) -> Dict:
    pass
# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-10 12:37:45
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-10 12:54:43

import sys
import os
from typing import Dict

def get_root_dir() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_config_dir() -> str :
    return os.path.dirname(os.path.abspath(__file__))

def get_base_conf_path() -> str:
    return os.path.abspath("./conf.toml")

def get_base_conf() -> Dict:
    pass
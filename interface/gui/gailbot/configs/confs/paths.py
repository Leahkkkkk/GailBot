# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-31 15:31:51
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-31 15:32:00

from dataclasses import dataclass 
from dict_to_dataclass import field_from_dict, DataclassFromDict
import toml 
import os
import logging

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
CONFIG_ROOT = os.path.join(PROJECT_ROOT, "config_backend")

logging.info(CONFIG_ROOT)
@dataclass 
class ConfigPath(DataclassFromDict):
    """
    Loads paths to engine configuration files
    """
    watson          : str = field_from_dict()
    whisper         : str = field_from_dict()
    google          : str = field_from_dict()
    log             : str = field_from_dict()
    ws_root         : str = field_from_dict()
    paths_config    : str = field_from_dict()
    services        : str = field_from_dict()
    default_setting : str = field_from_dict()
    valid_plugin    : str = field_from_dict()
    format_md       : str = field_from_dict()

path_dict = toml.load(os.path.join(CONFIG_ROOT, "paths.toml"))
PATH = ConfigPath.from_dict(path_dict["paths"]) 
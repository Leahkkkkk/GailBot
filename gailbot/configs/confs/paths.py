# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-31 15:31:51
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-31 15:32:00

from dataclasses import dataclass 
from dict_to_dataclass import field_from_dict, DataclassFromDict
import toml 
import os

CONFIG_ROOT = os.path.dirname(__file__)

@dataclass 
class EnginePath(DataclassFromDict):
    watson: str = field_from_dict()
    whisper: str = field_from_dict()
    google: str = field_from_dict()
    default: str = field_from_dict()



path_dict = toml.load(os.path.join(CONFIG_ROOT, "paths.toml"))
PATH = EnginePath.from_dict(path_dict["engines"]) 
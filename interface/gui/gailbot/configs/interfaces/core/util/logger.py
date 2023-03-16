import os
from dataclasses import dataclass
from dict_to_dataclass import field_from_dict, DataclassFromDict
import toml 


@dataclass 
class LogConfig(DataclassFromDict):
    formatter: str = field_from_dict()
    sub_dir_prefix: str = field_from_dict()
    log_dir: str = field_from_dict()

def load_log_config(path):
    d = toml.load(path)
    return LogConfig.from_dict(d["log"])
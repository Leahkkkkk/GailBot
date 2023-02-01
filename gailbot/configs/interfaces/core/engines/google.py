from dataclasses import dataclass
from dict_to_dataclass import field_from_dict, DataclassFromDict
from typing import Dict 
import toml 


@dataclass 
class GoogleConfig(DataclassFromDict):
    defaults: Dict = field_from_dict()
    name: str      = field_from_dict()
    workspace: str = field_from_dict()

def load_google_config(path: str):
    d = toml.load(path)
    return GoogleConfig.from_dict(d["google"])

def load_google_defaults(path: str):
    d = toml.load(path)
    return GoogleConfig.from_dict(d["google.defaults"])
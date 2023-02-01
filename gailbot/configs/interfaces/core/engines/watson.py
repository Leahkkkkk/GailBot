from dataclasses import dataclass
from dict_to_dataclass import field_from_dict, DataclassFromDict
from typing import Dict 
import toml 

@dataclass
class WatsonConfig(DataclassFromDict):
    max_file_size_bytes: float = field_from_dict()
    regions_uris: Dict = field_from_dict()
    format_to_content: Dict = field_from_dict()
    defaults: Dict = field_from_dict()
    name: str      = field_from_dict()
    workspace: str = field_from_dict()


def load_watson_config(path: str):
    d = toml.load(path)
    return WatsonConfig.from_dict(d["watson"])
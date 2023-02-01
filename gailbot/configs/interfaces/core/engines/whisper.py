from dataclasses import dataclass
from dict_to_dataclass import field_from_dict, DataclassFromDict
from typing import Dict 

@dataclass 
class WhisperConfig(DataclassFromDict):
    defaults: Dict = field_from_dict()
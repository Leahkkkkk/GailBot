from dataclasses import dataclass
from dict_to_dataclass import field_from_dict, DataclassFromDict
import toml 
from typing import List

@dataclass
class FileExtensions(DataclassFromDict):
    supported: List = field_from_dict()
    output: str = field_from_dict()
    saveGB: str = field_from_dict()

class ConversationDirText(DataclassFromDict):
    dir: str = field_from_dict()

class TransDirTest(DataclassFromDict):
    transDir: str = field_from_dict()


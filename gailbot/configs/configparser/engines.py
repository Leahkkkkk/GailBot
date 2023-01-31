from dataclasses import dataclass, field
from dict_to_dataclass import field_from_dict, DataclassFromDict
from typing import Dict 
import os 

from gailbot.configs.conf_path import ENGINE_PATH, CONFIG_ROOT

import toml 

@dataclass
class WatsonRegionsUris(DataclassFromDict):
    dallas: str = field_from_dict()
    washington: str = field_from_dict()
    frankfurt: str = field_from_dict()
    sydney: str = field_from_dict()
    tokyo: str = field_from_dict()
    london: str = field_from_dict()
    seoul: str = field_from_dict()
    
@dataclass
class FormatToContent(DataclassFromDict):
    flac: str = field_from_dict()
    mp3: str = field_from_dict()
    mpeg: str = field_from_dict()
    wav: str = field_from_dict()
    webm: str = field_from_dict()
    ogg: str = field_from_dict()
    opus: str = field_from_dict()

    

watson_data = toml.load(os.path.join(CONFIG_ROOT, ENGINE_PATH.watson))["watson"]
watson_region_uris = WatsonRegionsUris.from_dict(watson_data["regions"]["uris"])
watson_format_to_content = FormatToContent.from_dict(watson_data["format_to_content"])

@dataclass
class Watson:
    def __init__(self) -> None:
        self.max_file_size_bytes = watson_data["max_file_size_bytes"]
        self.regions_uris: Dict[str, str] = watson_data["regions"]["uris"]
        self.format_to_content: Dict[str, str] = watson_data["format_to_content"]
        self.defaults: Dict[str, str] = watson_data["defaults"]
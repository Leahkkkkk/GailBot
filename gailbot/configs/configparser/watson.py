from dataclasses import dataclass
from typing import Dict 
import os 
from gailbot.configs.conf_path import ENGINE_PATH, CONFIG_ROOT
import toml 

watson_data = toml.load(os.path.join(CONFIG_ROOT, ENGINE_PATH.watson))["watson"]
@dataclass
class Watson:
    def __init__(self) -> None:
        self.max_file_size_bytes = watson_data["max_file_size_bytes"]
        self.regions_uris: Dict[str, str] = watson_data["regions"]["uris"]
        self.format_to_content: Dict[str, str] = watson_data["format_to_content"]
        self.defaults: Dict[str, str] = watson_data["defaults"]
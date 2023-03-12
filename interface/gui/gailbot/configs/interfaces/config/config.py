import os
from dataclasses import dataclass
from dict_to_dataclass import field_from_dict, DataclassFromDict
import toml 

@dataclass
class WorkSpace(DataclassFromDict): 
      log_files                   : str = field_from_dict()
      watson_workspace            : str = field_from_dict()
      google_workspace            : str = field_from_dict()
      whisper_workspace           : str = field_from_dict()
      plugin_workspace            : str = field_from_dict()

@dataclass
class Output(DataclassFromDict): 
      audio                    : str = field_from_dict()
      transcript               : str = field_from_dict()

@dataclass
class Organizer(DataclassFromDict):
    num_threads: int = field_from_dict()
    
@dataclass
class Plugin(DataclassFromDict):
    num_threads: int = field_from_dict()
@dataclass
class Config:
    def __init__(self, config_path: str, root_path:str) -> None:
        config_d = toml.load(config_path)
        self.workspace : WorkSpace = WorkSpace.from_dict(config_d["workspace_path"])
        self.output    : Output = Output.from_dict(config_d["output_path"])
        self.organizer : Organizer = Organizer.from_dict(config_d["organizer"])
        self.plugin    : Plugin = Plugin.from_dict(config_d["plugin"])
        self.root      : str       = toml.load(root_path)["root"]
        
def load_top_config(config_path: str, root_path:str) -> Config:
    return Config(config_path, root_path)
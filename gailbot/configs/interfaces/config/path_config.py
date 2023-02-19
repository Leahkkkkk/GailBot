import os 
import shutil
from dataclasses import dataclass
from dict_to_dataclass import field_from_dict, DataclassFromDict
import toml 
from typing import Dict


@dataclass
class Temporary(DataclassFromDict):
    root: str = field_from_dict()
    transcribe_ws: str = field_from_dict()
    format_ws: str = field_from_dict()
    analysis_ws: str = field_from_dict()

@dataclass
class Temporary_folder:
    """ a dataclass that stores the paths for an audio file's temporary folder
        and creates the directory for the file
    """
    def __init__(self, file_name, structure: Temporary, root) -> None:
        self.transcribe_ws = os.path.join(
            root, structure.root, file_name, structure.transcribe_ws)
        self.format_ws = os.path.join(
            root, structure.root, file_name, structure.format_ws)
        self.analysis_ws = os.path.join(
            root, structure.root, file_name, structure.analysis_ws)
        os.makedirs(self.transcribe_ws, exist_ok=True)
        os.makedirs(self.format_ws, exist_ok=True)
        os.makedirs(self.analysis_ws, exist_ok=True)

@dataclass
class GailBotData(DataclassFromDict):
    root: str = field_from_dict()
    setting_src: str = field_from_dict()
    plugin_src: str = field_from_dict()

@dataclass 
class WorkSpace:
    def __init__(self, config_path: str, root_path:str) -> None:
        self.root: str = toml.load(root_path)["root"]
        config_d = toml.load(config_path)["workspace"]
        self.gailbot_data : GailBotData =  GailBotData.from_dict(
            add_root (config_d["gailbot_data"], self.root))
        self.log_dir: str = os.path.join(self.root, config_d["log"]["root"])
        self.temporary_ws: Temporary = Temporary.from_dict(config_d["temporary"])
    
    def get_temp_space(self, name:str)-> Temporary_folder:
        return Temporary_folder(name, self.temporary_ws, self.root)


def load_path_config(config_path, root_path) -> WorkSpace:
    """ public function that load the workspace data and return it """
    return WorkSpace(config_path, root_path)


def add_root(data: Dict[str, str], root: str) -> Dict[str, str]:
    """ given a dictionary that stores all the file paths, append root to the
       start of each path, and return the dictionary  
    """
    for key in data.keys():
        data[key] = os.path.join(root, data[key])
    return data
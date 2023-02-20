import os 
import shutil
from dataclasses import dataclass
from dict_to_dataclass import field_from_dict, DataclassFromDict
import toml 
from typing import Dict

@dataclass 
class OutputFolder(DataclassFromDict):
    transcribe_result: str = field_from_dict()
    analysis_result: str = field_from_dict()
    format_result: str = field_from_dict()
    media_file: str = field_from_dict()

@dataclass
class TemporaryFolder(DataclassFromDict):
    root: str = field_from_dict()
    transcribe_ws: str = field_from_dict()
    format_ws: str = field_from_dict()
    analysis_ws: str = field_from_dict()
    data_copy: str = field_from_dict()

@dataclass
class GailBotData(DataclassFromDict):
    root: str = field_from_dict()
    setting_src: str = field_from_dict()
    plugin_src: str = field_from_dict()

@dataclass 
class PathConfig:
    def __init__(self, config_path: str, root_path:str) -> None:
        self.root: str = toml.load(root_path)["root"]
        self.output_d: Dict = toml.load(config_path)["output"]
        self.workspace_d: Dict = toml.load(config_path)["workspace"]
        self.gailbot_data : GailBotData =  GailBotData.from_dict(
            add_root (self.workspace_d["gailbot_data"], self.root))
        self.log_dir: str = os.path.join(self.root, self.workspace_d["log"]["root"])
        self.temporary_ws: TemporaryFolder = TemporaryFolder.from_dict(self.workspace_d["temporary"])
    
    def get_temp_space(self, name:str)-> TemporaryFolder:
        temp_dir: Dict[str, str] = self.workspace_d["temporary"].copy()
        temp_dir["root"] = os.path.join(self.root, temp_dir["root"])
        os.makedirs(temp_dir["root"], exist_ok=True)
        for key, value in temp_dir.items():
            if key != "root":
                temp_dir[key] = os.path.join(temp_dir["root"], name, value)
                os.makedirs(temp_dir[key], exist_ok=True)
        return TemporaryFolder.from_dict(temp_dir)   

    def get_output_space(self, root: str, name: str) -> OutputFolder:
        new_output_dir = self.output_d.copy()
        for key, value in new_output_dir.items():
            new_output_dir[key] = os.path.join(root, name, value)
            os.makedirs(new_output_dir[key], exist_ok=True)
        return OutputFolder.from_dict(new_output_dir)
        

def load_path_config(config_path, root_path) -> PathConfig:
    """ public function that load the workspace data and return it """
    return PathConfig(config_path, root_path)


def add_root(data: Dict[str, str], root: str) -> Dict[str, str]:
    """ given a dictionary that stores all the file paths, append root to the
       start of each path, and return the dictionary  
    """
    for key, value in data.items():
        data[key] = os.path.join(root, value)
    return data

    
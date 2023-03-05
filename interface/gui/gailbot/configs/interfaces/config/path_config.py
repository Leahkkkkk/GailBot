import os 
import shutil
from dataclasses import dataclass
from dict_to_dataclass import field_from_dict, DataclassFromDict
import toml 
from typing import Dict
@dataclass 
class OutputFolder(DataclassFromDict):
    root: str = field_from_dict()
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
class GailBotData():
    def __init__(self, user_root: str, path_dict: Dict[str,  str]) -> None:
        self.root:        str = path_dict["root"]
        self.setting_src: str = os.path.join(user_root, self.root, path_dict["setting_src"])
        self.plugin_src:  str = os.path.join(user_root, self.root, path_dict["plugin_src"])
        self.logfiles:    str = os.path.join(user_root, self.root, path_dict["logfiles"])

@dataclass 
class PathConfig:
    def __init__(self, config_path: str, user_root:str) -> None:
        self._output_d: Dict = toml.load(config_path)["output"]
        self._workspace_d: Dict = toml.load(config_path)["workspace"]
        self._user_root = user_root 
        self.workspace_root = os.path.join(self._user_root, self._workspace_d["root"])
        self.tempspace_root = os.path.join(
            self.workspace_root, self._workspace_d["temporary"]["root"])
        self.gailbot_data: GailBotData = GailBotData(
            self.workspace_root, self._workspace_d["gailbot_data"] )
    
    def get_temp_space(self, name:str)-> TemporaryFolder:
        """ Given a name of the source, return a dataclass object that stores
            the temporary directory structures of source, including the 
            full paths to every subdirectory in the temporary directory 

        Args:
            name (str): the name of the source

        Returns:
            TemporaryFolder: a dataclass object that stores the full paths 
            of every subdirectories within the temporary folders for a 
            particular source
        """
        temp_dir: Dict[str, str] = self._workspace_d["temporary"].copy()
        for key, value in temp_dir.items():
                temp_dir[key] = os.path.join(self.tempspace_root, name, value)
        temp_dir["root"] = os.path.join(self.tempspace_root, name)
        return TemporaryFolder.from_dict(temp_dir)   

    def get_output_space(self, root: str, name: str) -> OutputFolder:
        """ Given a name of the source,  and the user selected output directory 
            root, return a dataclass object that stores
            the output directory structures of source, including the 
            full paths to every subdirectory in the output directory 

        Args:
            root (str): the root the directory of the output
            name (str): the name of the source

        Returns:
            OutputFolder: a dataclass object that stores the full paths 
            of every subdirectories within the output folders for a 
            particular source
        """
        new_output_dir = self._output_d.copy()
        for key, value in new_output_dir.items():
            new_output_dir[key] = os.path.join(root, name, value)
        new_output_dir["root"] = os.path.join(root, name)
        return OutputFolder.from_dict(new_output_dir)
        
def load_path_config(config_path, user_root) -> PathConfig:
    """ public function that load the workspace data and return it """
    return PathConfig(config_path, user_root)


    
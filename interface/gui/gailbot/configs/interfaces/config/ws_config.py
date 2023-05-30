import os
from dataclasses import dataclass
from dict_to_dataclass import field_from_dict, DataclassFromDict
import toml
from typing import Dict

@dataclass
class OutputFolder(DataclassFromDict):
    root: str = field_from_dict()
    transcribe_result: str = field_from_dict()
    analysis_result: str = field_from_dict()
    metadata: str = field_from_dict()
    media_file: str = field_from_dict()
    format_result: str = field_from_dict()

@dataclass
class TemporaryFolder(DataclassFromDict):
    root: str = field_from_dict()
    transcribe_ws: str = field_from_dict()
    format_ws: str = field_from_dict()
    analysis_ws: str = field_from_dict()
    data_copy: str = field_from_dict()

@dataclass
class FileExtensions(DataclassFromDict):
    temp: str = field_from_dict()
    output: str = field_from_dict()

@dataclass
class EngineWS():
    def __init__(self, ws_root:str, path_dict: Dict[str, str]) -> None:
        self.whisper = os.path.join(ws_root, path_dict["whisper"])
        self.google = os.path.join(ws_root, path_dict["google"])
        self.watson = os.path.join(ws_root, path_dict["watson"])
        self.google_api = os.path.join(ws_root, path_dict["google_api"])

@dataclass
class GailBotData():
    def __init__(self, ws_root: str, path_dict: Dict[str,  str]) -> None:
        self.root:        str = path_dict["root"]
        self.setting_src: str = os.path.join(ws_root, self.root, path_dict["setting_src"])
        self.plugin_src:  str = os.path.join(ws_root, self.root, path_dict["plugin_src"])
        self.engine_src:  str = os.path.join(ws_root, self.root, path_dict["engine_setting"])
        self.root:        str = os.path.join(ws_root, self.root)

@dataclass
class WorkSpaceConfig:
    def __init__(self, config_path: str, ws_root:str) -> None:
        d = toml.load(config_path)
        self._output_d: Dict = d["output"]
        self._workspace_d: Dict = d["workspace"]
        self._extension_d: Dict = d["file_extensions"]
        self._ws_root = ws_root
        # public path data
        self.workspace_root = os.path.join(self._ws_root, self._workspace_d["ws_root"])
        self.tempspace_root = os.path.join(
            self.workspace_root, self._workspace_d["temporary"]["root"])
        self.gailbot_data: GailBotData = GailBotData(
            self.workspace_root, self._workspace_d["gailbot_data"])
        self.file_extension : FileExtensions = FileExtensions.from_dict(self._extension_d)
        self.engine_ws: EngineWS = EngineWS(self.workspace_root, self._workspace_d["engine"])

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

    def get_output_space(self, root) -> OutputFolder:
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
            new_output_dir[key] = os.path.join(root, value)
        new_output_dir["root"] = root
        return OutputFolder.from_dict(new_output_dir)

    def get_output_structure(self) -> OutputFolder:
        return OutputFolder.from_dict(self._output_d)

def load_workspace_config(config_path, ws_root) -> WorkSpaceConfig:
    """ public function that load the workspace data and return it """
    return WorkSpaceConfig(config_path, ws_root)




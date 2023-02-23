
from typing import TypedDict, List, Dict
from gailbot.core.utils.general import (
    write_toml, 
    write_json, 
    get_name, 
    make_dir,
    copy, 
    read_toml, 
    read_json, 
    subdirs_in_dir, 
    paths_in_dir, 
    is_directory, 
    is_file)
from gailbot.core.utils.logger import makelogger
import os 
from .resultInterface import ResultInterface

logger = makelogger("transcribe_result")

class UttDict(TypedDict):
    speaker: str 
    start_time: str 
    end_time:str 
    text:str 
    
class UttResult(ResultInterface):
    def __init__(self, workspace: str, data: Dict[str, List[UttDict]] = None) -> None:
        self.workspace = os.path.join(workspace, "temporary_result")
        make_dir(self.workspace, overwrite=True)
        self.max_size = 1000 # TODO: move to toml 
        self.data = data 
        self.saved_to_disk: bool = False
            
    def save_data(self, data: Dict[str, List[UttDict]]) -> bool:
        try: 
            for name, result in data.items():
                write_json(os.path.join(self.workspace, f"{name}.toml"), result)
            self.saved_to_disk = True
            return True
        except Exception as e:
            logger.error(e)
            return False
           
    def output(self, path) -> None:
        try:
            if self.saved_to_disk:
                copy(self.workspace, path)
            else: 
                write_json(path, self.data)
            return True
        except Exception as e:
            logger.error(e)
        return True
    
    def get_data(self) -> Dict[str, List[UttDict]]:
        if self.saved_to_disk:
            return self._read_from_dir(self.workspace)
        else:
            return self.data 
    
    def load_result(self, path: str) -> Dict[str, List[UttDict]]:
        if is_file(path):
            return self._read_from_file(path)
        else:
            return self._read_from_dir(path)
            
    def _read_from_dir(self, path) -> Dict[str, List[UttDict]]:
        files = paths_in_dir(path, ["toml"])
        res = dict()
        for file in files: 
            res[get_name(file)] = read_json(file)
        return res 
        
    def _read_from_file(self, path: str) -> Dict[str, List[UttDict]]:
        return {get_name(path): read_json(path)}
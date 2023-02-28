
from typing import TypedDict, List, Dict, Union
from gailbot.core.utils.general import (
    write_csv, 
    read_csv,
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

""" TODO by FEB 24:
1. test the functions involve in I/O 

TODO: 
use .pickle to store temporary file to save memory
"""
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
                write_json(os.path.join(self.workspace, f"{name}.json"), result)
            self.saved_to_disk = True
            return True
        except Exception as e:
            logger.error(e)
            return False
           
    def output(self, path) -> None:
        try:
            if self.saved_to_disk:
                data = self.get_data()
            else: 
                data = self.data 
                
            for name, result in data.items():
                logger.info(path)
                logger.error(name)
                logger.error(path)
                write_csv(os.path.join(path, name + ".csv"), result)
            return True
        except Exception as e:
            logger.error(f"the path is {path}")
            logger.error(f"the name is {name}")
            logger.error(e)
        return False
    
    def get_data(self) -> Dict[str, List[UttDict]]:
        if self.saved_to_disk:
            files = paths_in_dir(self.workspace, ["json"])
            res = dict()
            for file in files: 
                res[get_name(file)] = read_json(file)
            return res 
        else:
            return self.data 
    
    def load_result(self, path: str) -> bool:
        if is_file(path):
            return self._read_from_file(path)
        elif is_directory(path):
            return self._read_from_dir(path)
        else: 
            return False
    
    def _read_from_dir(self, path) -> Dict[str, List[UttDict]]:
        try:
            files = paths_in_dir(path, ["csv"])
            res = dict()
            for file in files:
                res[get_name(file)] = read_csv(file)
            if res:
                assert self.save_data(res)
            return True 
        except Exception as e:
            logger.error(e)
            return False
        
    def _read_from_file(self, path: str) -> Dict[str, List[UttDict]]:
        try:
            res = {get_name(path): read_csv(path)}
            assert self.save_data(res)
        except Exception as e:
            logger.error(e)
            return False
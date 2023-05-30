
import os 
from typing import TypedDict, List, Dict

from gailbot.core.utils.general import (
    write_csv, 
    read_csv,
    write_json, 
    get_name, 
    make_dir,
    read_json, 
    paths_in_dir, 
    is_directory, 
    is_file)
from gailbot.core.utils.logger import makelogger
from gailbot.configs import service_config_loader
from .resultInterface import ResultInterface

SERVICE_CONFIG = service_config_loader()
logger = makelogger("transcribe_result")

"""
TODO: 
use .pickle to store temporary file to save memory
"""
class UttDict(TypedDict):
    """
    Defines a class for the utterance dictionary
    """
    speaker: str 
    start_time: str 
    end_time:str 
    text:str 
    
class UttResult(ResultInterface):
    """
    Defines a class containing the utterance results of a transcription
    """
    def __init__(self, workspace: str, data: Dict[str, List[UttDict]] = None) -> None:
        self.workspace = os.path.join(workspace, SERVICE_CONFIG.directory_name.temp_result)
        make_dir(self.workspace, overwrite=True)
        self.max_size = 1000 # TODO: move to toml 
        self.data = data 
        self.filenames :  Dict [str, str] = dict()
        self.saved_to_disk: bool = False
            
    def save_data(
        self, 
        data: Dict[str, List[UttDict]]
    ) -> bool:
        """
        Saves the given data to the output directory

        Args:  
            data: Dict[str, List[UttDict]]: data to save
        
        Returns:
            bool: True if successfully saved, false if not
        """
        if len(data) == 0: 
            logger.error("the result is empty")
            return False
        try: 
            for name, result in data.items():
                path = os.path.join(self.workspace, f"{name}.json")  
                write_json(path, result)
                if name not in self.filenames:
                    self.filenames[name] = path
            self.saved_to_disk = True
            return True
        except Exception as e:
            logger.error(e, exc_info=e)
            return False
           
    def output(self, path) -> bool:
        """
        Outputs the result to the output directory

        Args:
            path: output directory path
        
        Returns:
            bool: True if successfully outputted, false if not
        """
        try:
            if self.saved_to_disk:
                data = self.get_data()
            else: 
                data = self.data 
            for name, result in data.items():
                logger.info(path)
                logger.info(name)
                write_csv(os.path.join(path, name + ".csv"), result)
            return True
        except Exception as e:
            logger.error(f"the path is {path}")
            logger.error(e, exc_info=e)
        return False
    
    def get_data(self) -> Dict[str, List[UttDict]]:
        """
        Accesses and returns the data of the current transcription result

        Returns:
            Data in the form Dict[str, List[UttDict]]
        """
        if self.saved_to_disk:
            files = paths_in_dir(self.workspace, ["json"])
            res = dict()
            for file in files: 
                res[get_name(file)] = read_json(file)
            return res 
        else:
            return self.data 
   
    def get_one_file_data(self, name:str) -> Dict[str, List[UttDict]]:
        """
        Accesses and return the data of one file 

        Args: 
            name: the filename of one file 
            
        Return: a dictionary that contains the utterance data, the key of the 
                dictionary will be the file name, and the value will be the 
                list of utterance dictionary that stores the utterance data
        """ 
        res = dict()
        path = self.filenames[name]
        res[name] = read_json(path)
        return res 
        
        
    def load_result(self, path: str) -> bool:
        """
        Loads the transcription result

        Args:
            Path:str: path to the input 

        Returns: 
            Result in the form Dict[str, List[UttDict]] or false if not 
            successfully accessed
        """
        if is_file(path):
            return self._read_from_file(path)
        elif is_directory(path):
            return self._read_from_dir(path)
        else: 
            return False
    
    def _read_from_dir(self, path) -> Dict[str, List[UttDict]]:
        """
        Processes the result of a directory input

        Args:
            path: path to the directory to process
        
        Returns:
            Dict[str, List[UttDict]]: dictionary containing the processed input
        """
        try:
            files = paths_in_dir(path, ["csv"])
            res = dict()
            for file in files:
                res[get_name(file)] = read_csv(file)
            if res:
                assert self.save_data(res)
            return True 
        except Exception as e:
            logger.error(e, exc_info=e)
            return False
        
    def _read_from_file(self, path: str) -> Dict[str, List[UttDict]]:
        """
        Processes the result of a file input

        Args:
            path: path to the file to process
        
        Returns:
            Dict[str, List[UttDict]]: dictionary containing the processed input
        """
        try:
            res = {get_name(path): read_csv(path)}
            assert self.save_data(res)
        except Exception as e:
            logger.error(e, exc_info=e)
            return False
    

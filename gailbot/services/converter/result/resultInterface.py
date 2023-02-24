from typing import TypedDict, List, Dict
from dataclasses import dataclass
from .processingStatus import ProcessingStats
from gailbot.core.utils.logger import makelogger

logger = makelogger("result_interface")
""" .pickle , use efficient way to save the file """

class ResultInterface:
    def __init__(self, workspace: str, data = None) -> None:
        self.workspace = workspace 
        self.data = data 
        self.processingStats = None 
       
    def set_processing_stats(self, stats: ProcessingStats):
        try:
            assert stats 
            self.processingStats = stats 
            return True
        except Exception as e:
            logger.error(e)
            return False
            
    def save_data(self, data) -> bool:
        raise NotImplementedError
   
    def output(self, path:str) -> bool:
        raise NotImplementedError   
     
    def get_data(self) -> Dict:
        raise NotImplementedError
    
    
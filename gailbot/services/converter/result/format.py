from typing import TypedDict, List, Dict
from dataclasses import dataclass
from .resultInterface import ResultInterface, ProcessingStats


""" TODO:
1. update the interface after the pipeline is able to output the result
"""
class FormatResultDict(TypedDict):
   process_stats: Dict[str, str]

class FormatResult(ResultInterface):
    def __init__(self, data: Dict[str, ProcessingStats] = None) -> None:
        self.data = data 
    
    def save_data(self, data: Dict[str, ProcessingStats]):
        try:
            self.data = data 
            return True
        except Exception as e:
            return False
        
    def get_data(self):
        return self.data
    
    def output(self, path: str) -> bool:
        """ TODO: currently no data will be written as format result """
        return True 
from typing import TypedDict, List, Dict
from dataclasses import dataclass
from .resultInterface import ResultInterface


""" TODO:
1. update the interface after the pipeline is able to output the result
"""
class FormatResultDict(TypedDict):
   name: str 
   process_stats: Dict[str, str]
class FormatResult(ResultInterface):
    def __init__(self, data: Dict[str, FormatResultDict] = None) -> None:
        self.data = data 
    
    def save_data(self, data: Dict[str, FormatResultDict]):
        try:
            self.data = data 
            return True
        except Exception as e:
            return False
        
    def get_data(self):
        return self.data
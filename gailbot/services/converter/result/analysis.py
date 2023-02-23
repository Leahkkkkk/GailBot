from typing import TypedDict, List, Dict
from dataclasses import dataclass
from .resultInterface import ResultInterface

class AnalysisResultDict(TypedDict):
    """ TODO:  """
    pass 


class AnalysisResult(ResultInterface):
    def __init__(self, data: Dict[str, AnalysisResultDict] = None):
        self.data = data 
    
    def save_data(self, data: Dict[str, AnalysisResultDict]) -> bool:
        self.data = data 
        return True

    def output(self, path) -> None:
        pass
        return True
    
    def get_data(self):
        return self.data 

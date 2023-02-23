from typing import TypedDict, List, Dict
from dataclasses import dataclass
from .resultInterface import ResultInterface

class FormatResultDict(TypedDict):
    """ TODO:  """
    pass


class FormatResult(ResultInterface):
    def __init__(self, data: Dict[str, FormatResultDict] = None) -> None:
        self.data = data 
    
    def save_data(self, data: Dict[str, FormatResultDict]):
        try:
            self.data = data 
            return True
        except Exception as e:
            return False
        
    def output(self, path) -> None:
        pass
        raise NotImplementedError()
    
    def get_data(self):
        return self.data
from typing import TypedDict, List, Dict
from dataclasses import dataclass


""" .pickle , use efficient way to save the file """

class UttDict(TypedDict):
    speaker: str 
    start_time: str 
    end_time:str 
    text:str 
class FormatResultDict(TypedDict):
    """ TODO:  """
    pass
class AnalysisResultDict(TypedDict):
    """ TODO:  """
    pass 
    
class UttResult:
    def __init__(self, data: Dict[str, List[UttDict]] = None) -> None:
        self.data = data

    def set_data(self, data: Dict[str, List[UttDict]]) -> None:
        self.data = data 
        
    def output(self, path) -> None:
        pass
        raise NotImplementedError()
   
    def to_dict(self):
        return self.data 
    
    def read_result(self, path: str) -> List[UttDict]:
        pass
        return NotImplementedError()


class AnalysisResult:
    def __init__(self, data: Dict[str, AnalysisResultDict] = None) -> None:
        self.data = data 
    
    def set_data(self, data: Dict[str, AnalysisResultDict]) -> None:
        self.data = data 

    def output(self, path) -> None:
        pass
        raise NotImplementedError()

    def to_dict(self):
        return self.data 


class FormatResult:
    def __init__(self, data: Dict[str, FormatResultDict] = None) -> None:
        self.data = data 
    
    def set_data(self, data: Dict[str, FormatResultDict]):
        self.data = data 
        
    def output(self, path) -> None:
        pass
        raise NotImplementedError()
    
    def to_dict(self):
        return self.data
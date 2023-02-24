from typing import TypedDict, List, Dict
from dataclasses import dataclass
from .resultInterface import ResultInterface
from gailbot.core.utils.general import write_toml, write_json, write_txt

""" TODO:
1. update the interface after the plugin suite is connected 
"""
class AnalysisResultDict(TypedDict):
    name: str
    plugin_suite: str
    result: Dict[str, str]
class AnalysisResult(ResultInterface):
    def __init__(self, data: Dict[str, AnalysisResultDict] = None):
        self.data = data 
    
    def save_data(self, data: Dict[str, AnalysisResultDict]) -> bool:
        self.data = data 
        return True

    def output(self, path) -> bool:
        try:
            write_json(self.data, path)
            return True
        except Exception as e:
            return False
    
    def get_data(self):
        return self.data 

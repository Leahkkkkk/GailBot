from typing import TypedDict, List, Dict
from dataclasses import dataclass
from .resultInterface import ResultInterface
from gailbot.core.utils.general import write_toml, write_json, write_txt
from gailbot.core.utils.logger import makelogger
import os 
logger = makelogger("analysis-result")

""" TODO:
1. update the interface after the plugin suite is connected 
"""
class AnalysisResultDict(TypedDict):
    name: str
    plugin_suite: str
    result: Dict[str, str]

class AnalysisResult(ResultInterface):
    """
    Defines a class for the analysis result
    """
    def __init__(self, data: Dict[str, AnalysisResultDict] = None):
        self.data = data 
    
    def save_data(self, data: Dict[str, AnalysisResultDict]) -> bool:
        """
        Saves the inputted data

        Args:
            data: Dict[str, AnalysisResultDict]: data to save, in the form 
            of a dictionary mapping strings to analysis results

        Returns:
            Bool: True if successfully saved, false if not
        """
        self.data = data 
        return True

    def output(self, path) -> bool:
        """ NOTE: currently no data for analysis will be written """
        try:
            # write_json(self.data, os.path.join(path, "analysis.json"))
            return True
        except Exception as e:
            logger.error(e, exc_info=e)
            return True
        
    def get_data(self):
        """
        Accesses and object's data

        Returns:
            Data in the form Dict[str, AnalysisResultDict]
        """
        return self.data 

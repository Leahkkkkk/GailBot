from typing import TypedDict, List, Dict
from dataclasses import dataclass

""" .pickle , use efficient way to save the file """

class ResultInterface:
    def __init__(self, workspace: str, data = None) -> None:
        self.workspace = workspace 
        self.data = data 
        
    def save_data(self, data) -> bool:
        raise NotImplementedError
   
    def output(self, path:str) -> bool:
        raise NotImplementedError   
     
    def get_data(self) -> Dict:
        raise NotImplementedError
    
    
from abc import ABC
from typing import List, Dict 
from enum import Enum

class PayLoadStatus(Enum):
    INITIALIZED = 0 
    TRANSCRIBING = 1
    TRANSCRIBED = 2
    ANALYZING = 3
    ANALYZED = 4
    FORMATTING = 5
    FORMATTED = 6 

class PayLoadObject(ABC):
    original_source : str  
    data_files: List[str]
    engine_setting: Dict [str, str] # TODO: does profile setting refer to engine setting?
    plugin_setting: Dict [str, str]
    
    status: str 
    
    workspace: str 
    output_space: str 
    
    transcription_result: List [Dict[str, str]]
    format_result: Dict 
    analysis_result: Dict 
    
    def __init__(self, source) -> None:
        raise NotImplementedError()
    
    @staticmethod
    def is_supported(file_path: str) -> bool:
        raise NotImplementedError()
    
    @property
    def supported_format(self) -> str:
        raise NotImplementedError()
    
    @property
    def transcribed(self) -> bool:
        raise NotImplementedError()
    
    @property
    def analyzed(self) -> bool:
        raise NotImplementedError()
    
    @property 
    def formatted(self) -> bool:
        raise NotImplementedError()
    
    def get_status(self):
        raise NotImplementedError()
    
    def get_transcription_result():
        raise NotImplementedError()
    
    def get_format_result(self):
        raise NotImplementedError()
    
    def get_analyze_result(self):
        raise NotImplementedError()
    
    def get_data(self):
        raise NotImplementedError()
    
    def output_transcription_result(self, out_dir: str = output_space) -> str: 
        raise NotImplementedError()
    
    def output_transcription_result(self, out_dir: str = output_space) -> str:
        raise NotImplementedError()
    
    def load_data_files(file_path: str):
        raise NotImplementedError()
    
    def _copy_source(self) -> bool:
        raise NotImplementedError()
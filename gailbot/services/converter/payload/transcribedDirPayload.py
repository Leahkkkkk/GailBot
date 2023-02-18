from .payloadObject import PayLoadObject, PayLoadStatus
from typing import List, Dict 
from enum import Enum

class TranscribedDirPayload(PayLoadObject):
    original_source : str   # path to original source, should not be modified 
    data_files: List[str]   # a list of path to data files that is free to work with
    engine_setting: Dict [str, str] 
    plugin_setting: Dict [str, str] 
    
    status: PayLoadStatus 
    
    workspace: str     # workspace for storing temporary file , will be deleted afterward
    output_space: str  # directory where all the output will be stored 
    
    # payload result
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
    
    def set_transcription_result(self, result):
        raise NotImplementedError()
    
    def set_format_result(self, result):
        raise NotImplementedError()
    
    def set_analysis_result(self, result):
        raise NotImplementedError()
    
    def get_transcription_result(self):
        raise NotImplementedError()
    
    def get_format_result(self):
        raise NotImplementedError()
    
    def get_analyze_result(self):
        raise NotImplementedError()
    
    def get_data(self):
        raise NotImplementedError()
    
    def output_transcription_result(self, out_dir: str = output_space) -> str: 
        raise NotImplementedError()
   
    
    def load_data_files(file_path: str):
        raise NotImplementedError()
    
    def save(self):
        raise NotImplementedError()
    
    
    def _copy_source(self) -> bool:
        raise NotImplementedError()
   

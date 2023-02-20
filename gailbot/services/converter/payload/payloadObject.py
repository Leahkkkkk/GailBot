from abc import ABC
from typing import List, Dict 
from enum import Enum 
from ...organizer import TemporaryFolder, OutputFolder
from ..interfaces.resultInterface import Utt, AnalysisResult, FormatResult


class PayLoadStatus(Enum):
    """ For tracking the status of the file in the payload """
    INITIALIZED = 0 
    TRANSCRIBING = 1
    TRANSCRIBED = 2
    ANALYZING = 3
    ANALYZED = 4
    FORMATTING = 5
    FORMATTED = 6 

class PayLoadObject(ABC):
    """ super class of the payloadObject, interface includes necessary method 
        that subclass needs to implement. 
        Payload object contains the source that is waiting to be processed, 
        keeps track of the stage of the processes, and provides methods 
        for pipeline to run functions to transcribe, analyze and format 
        the data stored in payload. 
    """
    original_source : str   # path to original source, should not be modified 
    data_files: List[str]   # a list of path to data files that is free to work with
    """ we can abstract setting from pipeline, 
        but transcribe component will need to have access to the interfaces 
    
    """
    engine_setting: Dict [str, str] 
    plugin_setting: Dict [str, str] 
    
    status: PayLoadStatus 
    
    workspace: TemporaryFolder = None     # workspace for storing temporary file , will be deleted afterward
    output_space: OutputFolder = None # directory where all the output will be stored 
    
    
    # payload result
    transcription_result: List [Dict[str, str]] = None
    format_result: Dict = None
    analysis_result: Dict = None
    
    def __init__(self, source) -> None:
        raise NotImplementedError()
    
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
    
    def set_transcription_result(self, result: Dict[str, List[Utt]]):
        raise NotImplementedError()
    
    def set_format_result(self, result: Dict[str, FormatResult]):
        raise NotImplementedError()
    
    def set_analysis_result(self, result: Dict[str, AnalysisResult]):
        raise NotImplementedError()
    
    def get_transcription_result(self) -> Dict[str, List[Utt]]:
        raise NotImplementedError()
    
    def get_format_result(self) -> Dict[str, FormatResult]:
        raise NotImplementedError()
    
    def get_analyze_result(self) -> Dict[str, AnalysisResult]:
        raise NotImplementedError()

    def output_transcription_result(self, out_dir: str = output_space) -> str: 
        raise NotImplementedError()
    
    def output_transcription_result(self, out_dir: str = output_space) -> str:
        raise NotImplementedError()
    
    def load_data_files(file_path: str):
        raise NotImplementedError()
    
    def save(self):
        raise NotImplementedError()
    
    def _copy_source(self) -> bool:
        raise NotImplementedError()
    

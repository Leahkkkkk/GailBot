from abc import ABC
from typing import List, Dict 
import os 
from enum import Enum 
from gailbot.configs import path_config_loader, OutputFolder, TemporaryFolder
from gailbot.core.utils.logger import makelogger
from ...organizer.source import SourceObject
from ...organizer.settings import SettingObject
from ..result import (
    UttResult, 
    AnalysisResult, 
    FormatResult, 
    UttDict,
    AnalysisResultDict,
    FormatResultDict,
    ProcessingStats
)
from gailbot.core.utils.general import is_directory, make_dir, delete
from ...workspace import WorkspaceManager
logger = makelogger("payloadobject")

""" TODO by Feb 24:
1. move all name strings to configuration  
2. test save function and any functions involve i/o 
"""
PATH_CONFIG = path_config_loader()
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
    original_source : str       # path to original source, should not be modified 
    data_files: List[str]       # stores the path to the source that is safe to be used
    """ we can abstract setting from pipeline, 
        but transcribe component will need to have access to the interfaces 
    """
    
    name: str
    engine_setting: Dict [str, str] 
    plugin_setting: Dict [str, str] 
    
    status: PayLoadStatus 
    
    workspace: TemporaryFolder  # workspace for storing temporary file , will be deleted afterward
    out_dir: OutputFolder       # directory where all the output will be stored 
    
    # payload result
    
    def __init__(self, source: SourceObject) -> None:
        self.name = source.name
        self.original_source: str = source.source_path()
        self.setting: SettingObject = source.setting
        self.workspace: TemporaryFolder = \
            WorkspaceManager.get_file_temp_space(self.name)        
        self.out_dir: OutputFolder = \
            WorkspaceManager.get_output_space(source.output, self.name)
        self.transcription_result:  UttResult = UttResult(self.workspace.transcribe_ws)
        self.format_result: FormatResult = FormatResult(self.workspace.format_ws)
        self.analysis_result: AnalysisResult = AnalysisResult(self.workspace.analysis_ws)
        self._set_initial_status()
        self._copy_file() 
        
    def _set_initial_status(self) -> None: 
        raise NotImplementedError()
    
    def _copy_file(self) -> None:
        raise NotImplementedError()
        
    def is_supported(file_path: str) -> bool:
        raise NotImplementedError()
    
    @staticmethod
    def supported_format() -> str:
        raise NotImplementedError()
    
    # functions that has been implemented on abstract class 
    def get_source(self) -> List[str]:
        return self.data_files
    
    @property
    def transcribed(self) -> bool:
        return self.status == PayLoadStatus.TRANSCRIBED

    @property
    def analyzed(self) -> bool:
        return self.status == PayLoadStatus.ANALYZED 
    
    @property 
    def formatted(self) -> bool:
        return self.status == PayLoadStatus.FORMATTED
    
    def set_transcribed(self):
        self.status = PayLoadStatus.TRANSCRIBED
    
    def set_analyzed(self):
        self.status = PayLoadStatus.ANALYZED
        
    def set_formatted(self):
        self.status = PayLoadStatus.FORMATTED
   
    def get_engine(self) -> str:
        return self.setting.engine_setting.engine
   
    def get_engine_init_setting(self) -> Dict[str, str]:
        return self.setting.engine_setting.get_init_kwargs()
     
    def get_engine_transcribe_setting(self) -> Dict[str, str]:
        return self.setting.engine_setting.to_kwargs_dict()
    
    def get_plugin_setting(self) -> List[str]:
        """ TODO: check the plugin setting return types   """
        return self.setting.plugin_setting.get_data()
    
    def get_status(self) -> PayLoadStatus:
        return self.status
    
    def set_transcription_result(self, result: Dict[str, List[UttDict]])-> bool:
        try:
            self.transcription_result.save_data(result)
            return True 
        except Exception as e:
            logger.error(e)
            return False
    
    def set_format_result(self, result: Dict[str, FormatResultDict]) -> bool:
        try:
            self.format_result.save_data(result)
            return True
        except Exception as e:
            logger.error(e)
            return False
    
    def set_analysis_result(self, result: Dict[str, AnalysisResultDict]) -> bool:
        try:
            self.analysis_result.save_data(result)
            return True
        except Exception as e:
            logger.error(e)
            return False
        
    def set_transcription_process_stats(self, stats:ProcessingStats) -> Dict[str, List[UttDict]]:
        return self.transcription_result.set_processing_stats(stats)
    
    def set_analysis_process_stats(self, stats:ProcessingStats) -> Dict[str, List[UttDict]]:
        return self.analysis_result.set_processing_stats(stats)

    def set_format_process_stats(self, stats:ProcessingStats) -> Dict[str, List[UttDict]]:
        return self.format_result.set_processing_stats(stats)
    
    def get_transcription_result(self) -> Dict[str, List[UttDict]]:
        return self.transcription_result.get_data()
    
    def get_format_result(self) -> FormatResultDict:
        return self.format_result.get_data()
    
    def get_analyze_result(self) -> Dict[str, AnalysisResultDict]:
        return self.analysis_result.get_data()
    
    def output_transcription_result(self) -> bool: 
        try:
            self.transcription_result.output(self.out_dir.transcribe_result)
            return True
        except Exception as e:
            return False
        
    def output_format_result(self) -> bool:
       try:
           self.format_result.output(self.out_dir.format_result)
           return True 
       except Exception as e:
           return False
    
    def output_analysis_result(self) -> bool:
        try:
            self.analysis_result.output(self.out_dir.analysis_result)
            return True
        except Exception as e:
            return False
    
    def save(self):
        assert self.output_analysis_result()
        assert self.output_format_result()
        assert self.output_transcription_result()
        delete(self.workspace.root)
        with open(os.path.join(self.out_dir.root, ".gailbot"), "w+") as f:
            f.write(f"{self.name}")
    
    def __repr__(self) -> str:
        return f"payload object {self.name}"
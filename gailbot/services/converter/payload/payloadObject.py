from abc import ABC
from typing import List, Dict 
import os 
from enum import Enum 
from gailbot.configs import path_config_loader, OutputFolder, TemporaryFolder
from gailbot.core.utils.logger import makelogger
from ...organizer.source import SourceObject
from ...organizer.settings import SettingObject
from ..interfaces.resultInterface import (
    UttResult, 
    AnalysisResult, 
    FormatResult, 
    UttDict,
    AnalysisResultDict,
    FormatResultDict)
from gailbot.core.utils.general import (is_directory, make_dir, delete)
logger = makelogger("payloadobject")

""" TODO: move all name strings to configuration  """
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
    data_files: List[str]             # stores the path to the source that is safe to be used
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
    transcription_result:  UttResult = UttResult()
    format_result: FormatResult = FormatResult()
    analysis_result: AnalysisResult = AnalysisResult()
    
    def __init__(self, source: SourceObject) -> None:
        self.name = source.name
        self.original_source: str = source.source_path()
        self.setting: SettingObject = source.setting
        self.workspace: TemporaryFolder =  PATH_CONFIG.get_temp_space(
            f"{self.name}_temp"
        )
        
        self.out_dir: OutputFolder = PATH_CONFIG.get_output_space(
            source.output, f"{self.name}_gb_output"
        )
        
        # create the directory 
        for path in self.workspace.__dict__.values():
            if not is_directory(path):
                make_dir(path, True)
        
        for path in self.out_dir.__dict__.values():
            if not is_directory(path):
                make_dir(path, True)
                
        self._set_initial_status()
        self._copy_file() 
        
    def _set_initial_status(self) -> None: 
        raise NotImplementedError()
    
    def _copy_file(self) -> None:
        raise NotImplementedError()
        
    def is_supported(file_path: str) -> bool:
        raise NotImplementedError()
    
    
    @property
    def supported_format(self) -> str:
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
    
    def get_engine_setting(self) -> Dict[str, str]:
        return self.setting.engine_setting.to_kwargs_dict()
    
    def get_plugin_setting(self) -> List[str]:
        """ TODO: check the plugin setting return types   """
        return self.setting.plugin_setting.get_data()
    
    def get_status(self) -> PayLoadStatus:
        return self.status
    
    def set_transcription_result(self, result: Dict[str, List[UttDict]])-> bool:
        try:
            self.transcription_result.set_data(result)
            return True 
        except Exception as e:
            logger.error(e)
            return False
    
    def set_format_result(self, result: Dict[str, FormatResultDict]) -> bool:
        try:
            self.format_result.set_data(result)
            return True
        except Exception as e:
            logger.error(e)
            return False
    
    def set_analysis_result(self, result: Dict[str, AnalysisResultDict]) -> bool:
        try:
            self.analysis_result.set_data(result)
            return True
        except Exception as e:
            logger.error(e)
            return False
        
    def get_transcription_result(self) -> Dict[str, List[UttDict]]:
        return self.transcription_result.to_dict()
    
    def get_format_result(self) -> FormatResultDict:
        return self.format_result.to_dict()
    
    def get_analyze_result(self) -> Dict[str, AnalysisResultDict]:
        return self.analysis_result.to_dict()
    
    def output_transcription_result(self) -> str: 
        try:
            self.transcription_result.output(self.out_dir.transcribe_result)
            return True
        except Exception as e:
            return False
        
    def output_format_result(self) -> str:
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
        self.output_analysis_result()
        self.output_format_result()
        self.output_transcription_result()
        delete(self.workspace.root)
        with open(os.path.join(self.out_dir.root, ".gailbot"), "w+") as f:
            f.write(f"{self.name}")
    
    

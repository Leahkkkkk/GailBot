from .payloadObject import PayLoadObject, PayLoadStatus
from ...organizer.source import SourceObject
from ...organizer.settings import SettingObject
from typing import List, Dict 
from ...organizer import PATH_CONFIG, TemporaryFolder
from gailbot.core.utils.general import (
    get_extension, 
    get_name, 
    copy,
    write_toml, 
    write_json, 
    write_txt)
from gailbot.core.utils.logger import makelogger
import os 

logger = makelogger("audioPayload")

def load_audio_payload(source: SourceObject) -> PayLoadObject:
    if not source.setting: return False
    if not AudioPayload.is_supported(source.source_path): return False 
    # TODO: improve the logic of validating the format based on different engine
    try:
        return AudioPayload(source)
    except:
        return False

class AudioPayload(PayLoadObject):
    original_source : str   # path to original source, should not be modified 
    data_files: List[str]   # a list of path to data files that is free to work with
    setting: SettingObject
    status: PayLoadStatus 
    
    # payload result
    transcription_result: List [Dict[str, str]]
    format_result: Dict 
    analysis_result: Dict 
    
    def __init__(self, source: SourceObject) -> None:
        self.name = source.name
        self.original_source = source.source_path
        self.setting = source.setting
        self.status = PayLoadStatus.INITIALIZED 
        self.workspace = PATH_CONFIG.get_temp_space(
            f"{self.name}_temp")
        self.output_space = PATH_CONFIG.get_output_space(
            source.output, f"{self.name}_gb_output")
        extension = get_extension(self.original_source)
        tgt_path =os.path.join(self.workspace.data_copy, f"{self.name},{extension}")
        copy(self.original_source, os.path.join(self.workspace.data_copy, tgt_path))
        self.data_files = [tgt_path]
    
    
    def is_supported(self, file_path: str) -> bool:
        return get_extension(file_path) in self.supported_format
    
    @property
    def supported_format(self) -> str:
        return ["wav", "mp3", "opus"]
        
    @property
    def transcribed(self) -> bool:
        return self.status == PayLoadStatus.TRANSCRIBED
    
    @property
    def analyzed(self) -> bool:
        return self.status == PayLoadStatus.ANALYZED 
    
    @property 
    def formatted(self) -> bool:
        return self.status == PayLoadStatus.FORMATTED
    
    def get_status(self) -> PayLoadStatus:
        return self.status 
    
    def set_transcription_result(self, result):
        self.transcription_result = result
    
    def set_format_result(self, result):
        self.format_result = result
        
    def set_analysis_result(self, result):
        self.analysis_result = result
    
    def get_format_result(self):
        return self.format_result
    
    def get_analyze_result(self):
        return self.analysis_result
    
    def output_transcription_result(self) -> bool: 
        try:
            write_toml(
                self.transcription_result, 
                self.output_space.transcribe_result)
            return True
        except Exception as e:
            logger.error(e)
            return False
        
    def output_format_result(self) -> bool:
        try:
            write_txt(self.format_result, self.output_space.format_result)
            return True
        except Exception as e:
            logger.error(e)
            return False
    
    def output_analysis_result(self) -> bool:
        try:
            write_json(
                self.format_result, 
                self.output_space.analysis_result)
            return True
        except Exception as e:
            logger.error(e)
            return False
    
    def save(self):
        self.output_analysis_result()
        self.output_format_result()
        self.output_transcription_result()
   
    def _chunk_source(self):
        raise NotImplementedError() 


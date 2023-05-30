from abc import ABC
from typing import List, Dict 
import os 
from enum import Enum 
from datetime import datetime
from gailbot.core.utils.general import write_json, copy, is_file
from gailbot.configs import  OutputFolder, TemporaryFolder
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
from gailbot.core.utils.general import delete
from gailbot.workspace import WorkspaceManager
from gailbot.configs import service_config_loader
MERGED_FILE_NAME = "merged"
SERVICE_CONFIG = service_config_loader()
OUTPUT_MARKER = SERVICE_CONFIG.directory_name.hidden_file
logger = makelogger("payload object")
class PayLoadStatus(Enum):
    """ For tracking the status of the file in the payload """
    INITIALIZED = 0 
    TRANSCRIBING = 1
    TRANSCRIBED = 2
    ANALYZING = 3
    ANALYZED = 4
    FORMATTING = 5
    FORMATTED = 6
    FAILED = 7 

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
    data_file_format : str
    """ we can abstract setting from pipeline, 
        but transcribe component will need to have access to the interfaces 
    """
    
    name: str
    engine_setting: Dict [str, str] 
    plugin_setting: Dict [str, str] 
    
    status: PayLoadStatus 
    
    workspace: TemporaryFolder  # workspace for storing temporary file , will be deleted afterward
    out_dir: OutputFolder       # directory where all the output will be stored 
    merged_audio: str 
    # payload result
    def __init__(self, source: SourceObject, workspace: WorkspaceManager) -> None:
        """ initialize a payload object

        Args:
            source (SourceObject): A source object that stores the source data 
            workspace (WorkspaceManager): a workspace manager that provide 
                                          functions to initialize payload output
                                          directory and payload temporary workspace
            
        """ 
        self.name = source.name
        self.original_source: str = source.source_path()
        self.setting: SettingObject = source.setting
        self.workspace: TemporaryFolder = \
            workspace.get_file_temp_space(self.name)        
        self.out_dir: OutputFolder = \
            workspace.get_output_space(source.output)
        self.progress_display = source.progress_display
        self.transcription_result: UttResult = UttResult(self.workspace.transcribe_ws)
        self.analysis_result: AnalysisResult = AnalysisResult()
        self.format_result: FormatResult = FormatResult(self.workspace.format_ws)
        logger.info(f"ouputspace {self.out_dir.transcribe_result}")
        self._set_initial_status()
        self._copy_file() 
        self._merge_audio()
    
    def _merge_audio(self):
        raise NotImplementedError()
     
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
        """
        Accesses and returns a list of the current sources
        """
        return self.data_files
    
    @property
    def transcribed(self) -> bool:
        """
        Check if payload object is transcribed

        Returns:
            bool: true if transcribed, false if not
        """
        return self.status == PayLoadStatus.TRANSCRIBED

    @property
    def analyzed(self) -> bool:
        """
        Check if payload object is analyzed

        Returns:
            bool: true if analyzed, false if not
        """
        return self.status == PayLoadStatus.ANALYZED 
    
    @property 
    def formatted(self) -> bool:
        """
        Check if payload object is formatted

        Returns:
            bool: true if formatted, false if not
        """
        return self.status == PayLoadStatus.FORMATTED
    
    @property 
    def failed(self) -> bool:
        """ 
        Check if payload object failed
        
        Returns:
            bool: true if failed, false if not
        """
        return self.status == PayLoadStatus.FAILED
    
    def set_transcribed(self):
        """
        Sets status of payload object to TRANSCRIBED
        """
        self.status = PayLoadStatus.TRANSCRIBED
    
    def set_analyzed(self):
        """
        Sets status of payload object to ANALYZED
        """
        self.status = PayLoadStatus.ANALYZED
        
    def set_formatted(self):
        """
        Sets status of payload object to FORMATTED
        """
        self.status = PayLoadStatus.FORMATTED
   
    def set_failure(self):
        """ 
        set the status of the payload object to be FAILED
        """
        self.status = PayLoadStatus.FAILED
        
        
    def get_engine(self) -> str:
        """
        Accesses and returns the current engine setting

        Returns:
            Current engine as a string
        """
        return self.setting.engine_setting.engine
   
    def get_engine_init_setting(self) -> Dict[str, str]:
        """
        Accesses and returns the engine's initial settings

        Returns:
            Initial settings in the form of a dictionary
        """
        return self.setting.engine_setting.get_init_kwargs()
     
    def get_engine_transcribe_setting(self) -> Dict[str, str]:
        """
        Accesses and returns the engine's transcription settings

        Returns:
            Transcription settings in the form of a dictionary
        """
        return self.setting.engine_setting.get_transcribe_kwargs()
    
    def get_plugin_setting(self) -> List[str]:
        """
        Accesses and returns the plugin settings as a list

        Returns:
            List of strings of the current settings
        """
        return self.setting.plugin_setting.get_data()
    
    def get_status(self) -> PayLoadStatus:
        """
        Accesses and returns the payload's status

        Returns:
            Current PayLoadStatus
        """
        return self.status
    
    def set_transcription_result(
        self, 
        result: Dict[str, List[UttDict]]
    )-> bool:
        """
        Sets the transcription result to a given dictionary

        Args:
            result: Dict[str, List[UttDict]]: result to set

        Returns:
            bool: True if successfully set, false if not
        """
        try:
            self.transcription_result.save_data(result)
            return True 
        except Exception as e:
            logger.error(e, exc_info=e)
            return False
    
    def set_format_result(
        self, 
        result: Dict[str, FormatResultDict]
    ) -> bool:
        """
        Sets the format result to a given dictionary

        Args:
            result: Dict[str, FormatResultDict]: result to set

        Returns:
            bool: True if successfully set, false if not
        """
        try:
            self.format_result.save_data(result)
            return True
        except Exception as e:
            logger.error(e, exc_info=e)
            return False
    
    def set_analysis_result(
        self, 
        result: Dict[str, AnalysisResultDict]
    ) -> bool:
        """
        Sets the analysis result to a given dictionary

        Args:
            result: Dict[str, FormatResultDict]: result to set

        Returns:
            bool: True if successfully set, false if not
        """
        try:
            self.analysis_result.save_data(result)
            return True
        except Exception as e:
            logger.error(e, exc_info=e)
            return False
        
    def set_transcription_process_stats(
        self, 
        stats: ProcessingStats
    ) -> Dict[str, List[UttDict]]:
        """
        Sets the transcription processing stats.

        Args:
            stats:ProcessingStats: stats to set
        """
        return self.transcription_result.set_processing_stats(stats)
    
    def set_analysis_process_stats(
        self, 
        stats:ProcessingStats
    ) -> Dict[str, List[UttDict]]:
        """
        Sets the analysis processing stats.

        Args:
            stats:ProcessingStats: stats to set
        """
        return self.analysis_result.set_processing_stats(stats)

    def set_format_process_stats(
        self, 
        stats:ProcessingStats
    ) -> Dict[str, List[UttDict]]:
        """
        Sets the formal processing stats.

        Args:
            stats:ProcessingStats: stats to set
        """
        return self.format_result.set_processing_stats(stats)
    
    def get_transcription_result(self) -> Dict[str, List[UttDict]]:
        """
        Accesses the result of the current transcription

        Returns:
            Transcription result in the form of a dictionary mapping strings 
            to lists of utterance dictionaries
        """
        return self.transcription_result.get_data()
    
    def get_format_result(self) -> FormatResultDict:
        """
        Accesses the result of the current formatting

        Returns:
            Transcription result in the form of a FormatResultDict
        """
        return self.format_result.get_data()
    
    def get_analyze_result(self) -> Dict[str, AnalysisResultDict]:
        """
        Accesses the result of the current analysis

        Returns:
            Transcription result in the form of a dictionary mapping strings 
            to AnalysisResultDicts
        """
        return self.analysis_result.get_data()
    
    def output_transcription_result(self) -> bool: 
        """
        Outputs the current transcription result to the output directory

        Returns:
            bool: true if successfully outputted, false if not
        """
        try:
            logger.info(self.out_dir.transcribe_result)
            assert self.transcription_result.output(self.out_dir.transcribe_result)
            return True
        except Exception as e:
            logger.error(e, exc_info=e)
            return False
        
    def output_meta_result(self) -> bool:
        """
        Outputs the current formatting result to the output directory

        Returns:
            bool: true if successfully outputted, false if not
        """
        metadata = {
            "Profile Setting": self.setting.get_data(),
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Source": self.original_source,
            "Raw Audio": self.data_files,
            "Plugin Results": self.analysis_result.get_data(), 
        }
        try:
            write_json(self.out_dir.metadata, metadata)
            return True 
        except Exception as e:
            logger.error(e, exc_info=e)
            return False
    
    def output_analysis_result(self) -> bool:
        """
        Outputs the current analysis result to the output directory

        Returns:
            bool: true if successfully outputted, false if not
        """
        try:
            assert self.analysis_result.output(self.out_dir.analysis_result)
            return True
        except Exception as e:
            logger.error(e, exc_info=e)
            return False
        
    def output_format_result(self) -> bool:
        """ 
        Outputs the current format result to the output directory
        """
        try:
            assert self.format_result.output(self.out_dir.format_result)
            return True 
        except Exception as e:
            logger.error(e, exc_info=e)
            return False
        
    def save(self):
        """
        Saves the file and outputs all results to output directory
        """
        logger.info("saving the file")
        logger.info(self.out_dir.root)
        assert self.output_analysis_result()
        assert self.output_meta_result()
        assert self.output_transcription_result()
        assert self.output_format_result()
        with open(os.path.join(self.out_dir.root, OUTPUT_MARKER), "w+") as f:
            f.write(f"{self.name}")
        for file in self.data_files:
            if is_file(file):
                copy(file, os.path.join(self.out_dir.media_file, os.path.basename(file)))
        
    def clear_temporary_workspace(self):
        delete(self.workspace.root)
    
    def __repr__(self) -> str:
        return f"payload object {self.name}"
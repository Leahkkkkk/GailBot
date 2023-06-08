
from ..engine import Engine
from ...engines import exception as Err
from ..google.core import GoogleCore
from typing import Any, List, Dict
from typing import Dict, List, Union
from gailbot.core.utils.logger import makelogger 

logger = makelogger("google engine")
class Google(Engine):
    """ 
    An Engine that connect to Google Cloud STT, provide function to transcribe 
    audio file with Google Cloud STT

    Inheritance:
        Engine 
    """
    ENGINE_NAME = "Google"
    def __init__(self, google_api_key:str):
        logger.info("google engine initialized")
        self.core = GoogleCore(google_api_key)
        self.transcribe_success = False
    
    def __repr__(self):
        return self.ENGINE_NAME
    
    @property
    def supported_formats(self) -> List[str]:
        """ 
        a list of supported format that can be transcribe with the STT engine 
        """
        return self.core.supported_formats
    
    def transcribe(self, audio_path: str, payload_workspace:str) -> List[Dict[str, str]] :
        """ use Google engine to transcribe the audio file 

        Args:
            audio_path (str): path to audio source
            output_directory (str): path to output directory 

        Raises:
            Err.TranscriptionError

        Returns:
            A list of dictionary that contains the utterance data of the 
            audio file, each part of the audio file is stored in the format 
            {speaker: , start_time: , end_time: , text: }
        """
        res = self.core.transcribe(audio_path, payload_workspace)
        self.transcribe_success = True
        return res
    
    def is_file_supported(self, file_path: str) -> bool:
        """ 
        given a file path, return true if the file format is supported by 
        the Google STT engine 
        """
        return self.core.is_file_supported(file_path)
    
    def get_supported_formats(self) -> List[str]:
        """ 
        return a list of supported format that can be 
        transcribe with the STT engine 
        """
        return self.core.supported_formats
    
    def get_engine_name(self) -> str:
        return self.ENGINE_NAME
    
    def was_transcription_successful(self) -> bool:
        return self.transcribe_success
    

    @staticmethod 
    def is_valid_google_api(google_api_key) -> bool:
        engine = GoogleCore.is_valid_google_api(google_api_key)
        return True if engine else False
from ..engine import Engine
from ...engines import exception as Err
from ..google.core import GoogleCore
from typing import Any, List, Dict 

class Google(Engine):
    ENGINE_NAME = "Google"
    def __init__(self, api_key: Dict = None, *args, **kwargs):
        self.apikey = api_key
        self.core = GoogleCore(self.apikey)
        self.transcribe_success = False
    
    def __repr__(self):
        return self.ENGINE_NAME
    
    @property
    def supported_formats(self) -> List[str]:
        return self.core.supported_formats
    
    def transcribe(self, audio_path: str, output_directory: str) -> Any :
        try:
            res = self.core.transcribe(audio_path, output_directory)
        except:
            raise Err.TranscriptionError
        else:
            self.transcribe_success = True
            return res
    
    def is_file_supported(self, file_path: str) -> bool:
        return self.core.is_file_supported(file_path)
    
    def get_supported_formats(self) -> List[str]:
        return self.core.supported_formats
    
    def get_engine_name(self) -> str:
        return self.ENGINE_NAME
    
    def was_transcription_successful(self) -> bool:
        return self.transcribe_success
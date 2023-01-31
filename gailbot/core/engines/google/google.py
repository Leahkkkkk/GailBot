from ..engine import Engine
from typing import Any, List 

class Google(Engine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ENGINE_NAME = "Google"
        self.transcribe_success = False
        raise NotImplementedError 
    
    def __repr__(self):
        return "Google Speech To Text Engine"
    
    def transcribe(self, *args, **kwargs) -> Any :
        return super().transcribe(*args, **kwargs)
    
    def is_file_supported(self, file_path: str) -> bool:
        return super().is_file_supported(file_path)
    
    def get_supported_formats(self) -> List[str]:
        return super().get_supported_formats()
    
    def get_engine_name(self) -> str:
        return self.ENGINE_NAME
    
    def was_transcription_successful(self) -> bool:
        return self.transcribe_success
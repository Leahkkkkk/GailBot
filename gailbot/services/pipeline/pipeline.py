from typing import List 
from converter import PayLoadObject

class PipelineService:
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def __call__(self, payloads: List[PayLoadObject]):
        raise NotImplementedError()
    
    def check_source_status(self, source_name: str) -> str:
        raise NotImplementedError()
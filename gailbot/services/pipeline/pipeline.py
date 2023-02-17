from typing import List 
from converter import PayLoadObject

class PipelineService:
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def __call__(self, parloads: List[PayLoadObject]):
        raise NotImplementedError()
from typing import List 
from ..converter import PayLoadObject

class PipelineService:
    def __init__(self) -> None:
        pass
    def __call__(self, payloads: List[PayLoadObject]):
        raise NotImplementedError()
    
# Standard library imports 
from typing import List
# Local imports
from .engine import Engine
from .watson import WatsonEngine
from .sphinx import SphinxEngine
from ..io import IO
from ..network import Network
from ...utils.exceptions import ExceptionUnexpected
# Third party imports 

class Engines:

    supported_engines = ("watson", "sphinx")
    
    def __init__(self, engine_type : str, io : IO, network : Network) -> None:
        ### Params
        # Engine type must be supported. 
        self.ready = engine_type in self.supported_engines
        self.engine_type = engine_type
        self.io = io 
        self.network = network
        self.engine_configurations = {}

    #### GETTERS 

    def is_ready(self) -> bool:
        return self.ready

    def get_engine_type(self) -> str:
        return self.engine_type

    def get_supported_engines(self) -> List[str]:
        return list(self.supported_engines) 

    #### SETTERS

    def configure_engine(self) -> bool:
        pass 
    
    #### OTHERS

    def transcribe_conversation(self) -> None:
        pass 

    def _initialize_engine(self, engine_type : str) -> Engine:
        if engine_type == "watson":
            return WatsonEngine()
        elif engine_type == "sphinx":
            return SphinxEngine()
        else:
            raise ExceptionUnexpected


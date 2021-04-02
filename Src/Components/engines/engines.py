# Standard library imports 
from typing import List, Dict
# Local imports
from .engine import Engine
from .watson import WatsonEngine
from ..io import IO
from ..network import Network
from ...utils.exceptions import ExceptionUnexpected
# Third party imports 

class Engines:
    """
    Manages different speech to text engines and provides initialized engines 
    to users. 
    """

    def __init__(self, io : IO, network : Network) -> None:
        self.engines = {
            "watson" : WatsonEngine
        } 
        self.io = io 
        self.network = network 

    def get_supported_engines(self) -> List[str]:
        """
        Obtain a list of supported speech to text engines. 

        Returns:
            (List[str]): Names of supported engines.
        """
        return list(self.engines.keys()) 

    def engine(self, engine_type : str) -> Engine:
        """
        Obtain an initialized engine of the specified type.
        Raises ExceptionUnexpected if the engine_type is not supported.

        Args:
            engine_type (str): Type of the engine. Must be a supported engine.

        Returns:
            (Engine)
        """
        if not engine_type in self.engines.keys():
            raise ExceptionUnexpected 
        return self.engines[engine_type](self.io, self.network)

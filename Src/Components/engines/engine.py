# Standard library imports 
from abc import ABC,abstractmethod
# Local imports 
from ..io import IO 
from ..network import Network
# Third party imports 

class Engine(ABC):
    
    @abstractmethod
    def __init__(self, io : IO, network : Network) -> None:
        pass

    ### SETTERS

    @abstractmethod
    def configure_service(self, *args, **kwargs) -> bool:
        pass 

    ### GETTERS


    ### OTHERS









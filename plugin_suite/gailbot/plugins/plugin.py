from pydantic import BaseModel
from typing import TypedDict
from typing import Dict, Union, List, Any
import os 



class Plugin:
    """
    Template superclass for any plugin.
    """

    def __init__(self) -> None:
        self.name = self.__class__
        self.successful = False
        pass

    @property
    def is_successful(self) -> bool:
        return self.successful

    def apply(
        self,
        dependency_outputs : Dict[str, Any],
        methods,
        *args,
        **kwargs
    ) -> Any:
        """
        Wrapper for plugin algorithm that has access to dependencies =,
        Args:
            dependency_outputs (Dict[str,Any]):
                Mapping from all plugins this plugin is dependant on and their
                outputs.
        """
        raise NotImplementedError()
    
    def __repr__(self) -> str:
        return f"plugin {self.name}"


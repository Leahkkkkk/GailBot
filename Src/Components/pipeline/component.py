# Standard library imports
from enum import Enum
from typing import Any
# Local imports
from .stream import Stream
# Third party imports

class ComponentState(Enum):
    successful = "successful"
    failed = "failed"
    ready = "ready"

class Component:

    def __init__(self, name : str, instantiated_obj : object) -> None:
        self.state = ComponentState.ready
        self.name = name
        self.instantiated_obj = instantiated_obj
        self.runtime = 0
        self.result = None

    def get_state(self) -> ComponentState:
        return self.state

    def get_name(self) -> str:
        return self.name

    def get_instantiated_object(self) -> object:
        return self.instantiated_obj

    def get_result(self) -> Stream:
        return self.result

    def get_runtime(self) -> float:
        return self.runtime

    def set_state(self, state : ComponentState) -> None:
        self.state = state

    def set_result(self, result : Stream) -> None:
        self.result = result

    def set_runtime(self, runtime : float) -> None:
        self.runtime = runtime


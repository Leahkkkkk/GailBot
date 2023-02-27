# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:13:08
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-07 16:24:35
# Standard library imports
from enum import Enum
from typing import Any
# Local imports
from .stream import Stream
# Third party imports


class ComponentState(Enum):
    """
    States that a Component can have.
    """
    successful = "successful"
    failed = "failed"
    ready = "ready"


class Component:
    """
    Represents an internal object that is used by the Pipeline.
    """

    def __init__(self, name: str, instantiated_obj: object) -> None:
        """
        Args:
            name (str): Name of the component.
            instantiated_obj (object): Object the component represents.
        """
        self.state = ComponentState.ready
        self.name = name
        self.instantiated_obj = instantiated_obj
        self.runtime = 0
        self.result = None

    def get_state(self) -> ComponentState:
        """
        Obtain the current state of the component.

        Returns:
            (ComponentState)
        """
        return self.state

    def get_name(self) -> str:
        """
        Obtain the name of the component

        Returns:
            (str): Name of the component.
        """
        return self.name

    def get_instantiated_object(self) -> object:
        """
        Obtain the instantiated object the component represents.

        Returns:
            (object)
        """
        return self.instantiated_obj

    def get_result(self) -> Stream:
        """
        Obtain the result of executing the component.

        Returns:
            (Stream): Component result wrapped as a Stream.
        """
        return self.result

    def get_runtime(self) -> float:
        """
        Obtain the runtime, in seconds, of the component.

        Returns:
            (float): Runtime in seconds.
        """
        return self.runtime

    def set_state(self, state: ComponentState) -> bool:
        """
        Set the state of the component

        Args:
            state (ComponentState)

        Returns:
            (bool): True if successfully set. False otherwise.
        """
        self.state = state
        return True

    def set_result(self, result: Stream) -> bool:
        """
        Set the result of executing the component

        Args:
            result (Stream)

        Returns:
            (bool): True if successfully set. False otherwise.
        """
        self.result = result
        return True

    def set_runtime(self, runtime: float) -> None:
        """
        Set the runtime of the component

        Args:
            runtime (float): Runtime, must be greater than or equal to  0.

        Returns:
            (bool): True if successfully set. False otherwise.
        """
        if runtime < 0:
            return False
        self.runtime = runtime
        return True

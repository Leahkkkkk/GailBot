# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 12:54:35
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-15 15:33:47


from enum import Enum
from dataclasses import dataclass
from typing import Any, Dict

class ComponentState(Enum):
    """
    Class containing the status of a component object.
    """
    READY   = 0
    SUCCESS = 1
    FAILED  = 2

@dataclass
class ComponentResult:
    """
    Class containing the result of a component object.
    """
    state   : ComponentState = ComponentState.FAILED
    result  : Any            = None
    runtime : float          = 0

class Component:
    """
    Wrapper for a function that is run in the pipeline.
    Should be subclassed.
    """

    def __init__(self, *args, **kwargs):
        pass

    def __repr__(self):
        raise NotImplementedError()

    def __call__(
        self,
        dependency_outputs : Dict[str, ComponentResult] ,
        *args,
        **kwargs
    ) -> ComponentState:
        raise NotImplementedError()
    

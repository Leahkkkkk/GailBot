# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 12:52:37
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-08 15:49:05

from typing import List, Dict, Any
from dataclasses import dataclass

from .component import Component


@dataclass
class DataStream:
    data : Any = None

class Pipeline:

    def __init__(
        self,
        dependency_map : Dict[str, str],
        components : List[Component]
    ):
        """
        Dependency map describes the execution order.
        """
        pass

    def __repr__(self) -> str:
        pass

    def __call__(
        self,
        base_input : Any
    ):
        """
        Execute the pipeline by running all components in order of the dependency
        graph. This wraps data as DataStream before passing it b/w components.
        The base input is passed to all components.
        Additionally, each component receives the output of its dependencies
        """
        pass

    def get_components(
        self,
        component_names : List[str] = None
    ) -> List[Component]:
        """
        Get component objects for specific names.
        If None, return all components
        """
        pass

    def component_names(self) -> List[str]:
        """Get names of all components"""
        pass

    def component_dependencies(self, component_name : str) -> List[str]:
        """Dependencies of specific component"""
        pass

    def dependency_graph(self) -> Dict:
        """Return the entire dependency graph as a dictionary"""
        pass





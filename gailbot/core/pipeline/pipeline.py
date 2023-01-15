# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 12:52:37
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-15 13:36:20

import sys
import os
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
import networkx as nx
from copy import deepcopy
from .component import Component, ComponentState


@dataclass
class DataStream:
    data : Any = None

class Pipeline:

    def __init__(
        self,
        dependency_map : Dict[str, List[str]],
        components : Dict[str, Component]
    ):
        """
        Dependency map describes the execution order.
        """

        self.dependency_map = dependency_map
        self.components = components
        self._generate_dependency_graph(
            dependency_map, components
        )


    def __repr__(self) -> str:
        return str(self.get_dependency_graph())

    def __call__(
        self,
        base_component_kwargs : Dict
        # NOTE: base_input is passed only to the first component.
    ) -> Dict[str, ComponentState]:

        """
        Execute the pipeline by running all components in order of the dependency
        graph. This wraps data as DataStream before passing it b/w components.
        Additionally, each component receives the output of its dependencies.

        NOTE: The components themselves are responsible for checking whether
        the parent components executed successfully.
        """

        successors = self.get_dependency_graph()
        results = dict()
        while True:
            executables = [
                c for c, d in self.dependency_graph.in_degree if d == 0
            ]
            # Stop if no nodes left.
            if len(executables) == 0:
                break

            # TODO: All of these should be run in threads in parallel.
            for executable in executables:
                exe_name = self.component_to_name[executable]
                if len(successors[exe_name]) > 0:
                    inputs = {
                        k : results[k] for k in successors[exe_name]
                    }
                else:
                    inputs = {
                        "base" : base_component_kwargs
                    }
                res = executable(inputs)
                results[exe_name] = res
                self.dependency_graph.remove_node(executable)

        # Regenerate graph
        self._generate_dependency_graph(
            self.dependency_map, self.components
        )

        return {
            k : v.state for k, v in results.items()
        }

    def component_names(self) -> List[str]:
        """Get names of all components"""
        return list(self.name_to_component.keys())

    def is_component(self, name : str) -> bool:
        return name in self.component_names()

    def component_parents(self, name : str) -> List[str]:
        """
        Get component this component is dependant on.
        """
        if not self.is_component(name):
            raise Exception(f"No component named {name}")
        edges = list(self.dependency_graph.in_edges(self.name_to_component[name]))
        return [self.component_to_name[e[0]] for e in edges]

    def component_children(self, name : str) -> List[str]:
        """
        Get components that are dependant on this component
        """
        if not self.is_component(name):
            raise Exception(f"No component named {name}")
        edges = list(self.dependency_graph.out_edges(self.name_to_component[name]))
        return [self.component_to_name[e[1]] for e in edges]

    def get_dependency_graph(self) -> Dict:
        """
        Return a map from each component to the components it is dependant on
        """
        view = dict()
        for name in self.name_to_component:
            view[name] = self.component_parents(name)
        return view

    #####
    # PRIVATE METHODS
    ####

    def _does_cycle_exist(self, graph: nx.Graph) -> bool:
        """
        Return True if there are any cycles in the graph. False otherwise.
        """
        try:
            nx.find_cycle(graph, orientation="original")
            return True
        except:
            return False

    def _generate_dependency_graph(
        self,
        dependency_map : Dict[str, List[str]],
        components : Dict[str, Component]
    ) -> None:
        # Graph views
        # NOTE: These are graphs of Components, not str!
        self.dependency_graph = nx.DiGraph()
        self.name_to_component = dict()
        # self.executed_graph_view = nx.DiGraph()

        # Verify that the same keys exist in both dicts
        assert dependency_map.keys() == components.keys(), \
            f"Component and dependency maps should have similar keys"

        # # Mapping from component name to dependencies
        # # NOTE: Assuming that the dependency_map keys are in order i.e,
        # # a component will be seen as a key before it is seen as a dependency.
        # self.name_to_dependency_node : Dict[str, Component] = dict()

        for name, dependencies in dependency_map.items():

            # This node must exist as a Component
            if not name in components:
                raise Exception(
                    f"Node does not exist in the component map: {name}"
                )

            # Component cannot be added twice
            if self.is_component(name):
                raise Exception(f"Repeated component {name}")

            # Create a component and add to main graph
            self.dependency_graph.add_node(components[name])


            # We want to add directed edges from all the dependencies to the
            # current node. This implies that the dependencies should already
            # exist as nodes.
            for dep in dependencies:
                if not self.is_component(dep):
                    raise Exception(
                        f"Unseen component added as dependency {dep}"
                    )
                self.dependency_graph.add_edge(components[dep], components[name])

            # NOTE: Cycles are not supported
            if self._does_cycle_exist(self.dependency_graph):
                raise Exception(f"Cycle found in execution logic")

            self.name_to_component[name] = components[name]

        self.component_to_name = {
            v : k for k,v in self.name_to_component.items()
        }





# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 12:52:37
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-15 16:04:52
from typing import List, Dict, Any
from dataclasses import dataclass

from .component import Component, ComponentState, ComponentResult
from gailbot.core.utils.threads import ThreadPool
from gailbot.core.utils.logger import makelogger

import networkx as nx

Failure = ComponentResult(ComponentState.FAILED, None, 0)
logger = makelogger("pipeline")
@dataclass
class DataStream:
    data : Any = None
    
class Pipeline:
    """
    Defines a class for the pipeline that runs the dependency map.
    """
    def __init__(
        self,
        dependency_map : Dict[str, List[str]],
        components : Dict[str, Component],
        num_threads: int 
    ):
        """
        Dependency map describes the execution order.
        """
        self.dependency_map = dependency_map
        self.components = components
        self.threadpool = ThreadPool(num_threads)
        self._generate_dependency_graph(
            dependency_map, components
        )
    
    def __repr__(self) -> str:
        """
        Accesses the pipeline's dependency graph.

        Args:
            self
        
        Returns:
            String representation of the pipeline's dependency graph.d
        """
        return str(self.get_dependency_graph())

    def __call__(
        self,
        base_input : Any,
        additional_component_kwargs : Dict = dict()
        # NOTE: base_input is passed only to the first component.
    ) -> Dict[str, ComponentState]:
        """
        Execute the pipeline by running all components in order of the dependency
        graph. This wraps data as DataStream before passing it b/w components.
        Additionally, each component receives the output of its dependencies. 

        Args:
            base_input: 
                a list of input arguments that will be passed to the first 
                component of the graph 
                
            Additional_component_kwargs: 
                passed as a dereferenced dictionary to each component.

        Returns:
            Dictionary containing keys mapping to the component states 
            corresponding to the result of each task.
            
        Note: 
            each component is contained in a Component class
        """
        successors = self.get_dependency_graph()
        logger.info(successors) 
        logger.info(self.dependency_graph)
        logger.info(self.components)
        
        name_to_results : Dict[str, ComponentResult] = dict()   # map component name to result
       
        while True:
            # executables is a list of Component who currently has no dependent node 
            executables: List[Component] = [
                c for c, d in self.dependency_graph.in_degree if d == 0
            ]
            
            # exit the loop if no nodes left.
            if len(executables) == 0:
                break
            
            for executable in executables:
                threadkey_to_exe: Dict[str, Component] = dict()       # map thread key to executable
                exe_name: str = self.component_to_name[executable]
                dependency_resolved = True
                
                # check the result output of exe_name's dependency component 
                if len(successors[exe_name]) > 0:
                    dep_outputs : Dict[str, ComponentResult] = {
                        k : name_to_results[k] for k in successors[exe_name]
                    }
                else:
                    dep_outputs = {
                        "base" : ComponentResult(
                            state=ComponentState.SUCCESS,
                            result=base_input,
                            runtime=0
                        )
                    }
                    
                for res in dep_outputs.values():
                    if res.state == ComponentState.FAILED:
                        name_to_results[exe_name] = Failure
                        if self.dependency_graph.has_node(executable):
                            self.dependency_graph.remove_node(executable)
                        dependency_resolved = False
 
                args = [dep_outputs]          
                              
                if dependency_resolved:                    
                    key = self.threadpool.add_task(
                        executable, 
                        args = args, 
                        kwargs = additional_component_kwargs) 
                    logger.info(f" the component {executable} get the thread key {key}")
                    threadkey_to_exe[key] = executable           

            # wait until all tasks finishes before next iteration
            # self.threadpool.wait_for_all_completion(error_fun=lambda:None)
            
            for key, exe in threadkey_to_exe.items():
                # get the task result from the thread pool
                logger.info(key)
                logger.info(exe)
                exe_res = self.threadpool.get_task_result(key)
                self.dependency_graph.remove_node(exe)
                name = self.component_to_name[exe]
               
                if exe_res and exe_res.state == ComponentState.SUCCESS:
                    # add to result if success
                    name_to_results[name] = exe_res
                else:
                    # add the failed result on failure
                    name_to_results[name] = Failure
        
                 
        # Regenerate graph
        self._generate_dependency_graph(
            self.dependency_map, self.components
        )

        return {
            k : v.state for k, v in name_to_results.items()
        }

    def component_names(self) -> List[str]:
        """
        Gets names of all components in the dependency map.
        
        Args:
            self
        
        Returns:
            List of strings containing components.
        """
        return list(self.name_to_component.keys())

    def is_component(self, name : str) -> bool:
        return name in self.component_names()

    def component_parents(self, name : str) -> List[str]:
        """
        Get the component(s) that the given component is dependent on.

        Args:
            name: string containing the name of the child component.

        Returns:
            List of strings of the names of the given component's parent 
            components.

            Raises exception if the given name doesn't correspond to an 
            existing component.
        """
        if not self.is_component(name):
            raise Exception(f"No component named {name}")
        edges = list(self.dependency_graph.in_edges(self.name_to_component[name]))
        return [self.component_to_name[e[0]] for e in edges]

    def component_children(self, name : str) -> List[str]:
        """
        Gets component(s) that are dependent on the given component.

        Args:
            name: string containing the name of the child component.

        Returns:
            List of strings of the names of components that are dependent on the 
            given component.

            Raises exception if the given name doesn't correspond to an 
            existing component.
        """
        if not self.is_component(name):
            raise Exception(f"No component named {name}")
        edges = list(self.dependency_graph.out_edges(self.name_to_component[name]))
        return [self.component_to_name[e[1]] for e in edges]

    def get_dependency_graph(self) -> Dict:
        """
        Returns a map from each component to the components it is dependent on.

        Args:
            self
        
        Returns:
            Dictionary mapping the given component to the components it is dependent upon.
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
        Determines if there are existing cycles in the given graph.

        Args:
            graph: graph in which to determine if there are cycles.
        
        Returns:
            True if there are any cycles in the given graph, false if not.
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
        """
        Generates a dependency graph containing components from a given dictionary.
        Assumes that the dependency_map keys are in order i.e, a component will 
        be seen as a key before it is seen as a dependency.

        Args:
            dependency_map: dictionary containing lists of strings to map between.
            components: dictionary containing components to insert into the newly 
                created dependency graph.

        Returns:
            A graph of components mapping from the component's name to its dependencies.

            Raises exception if an element of the dependency graph does not correspond
                to a valid element.

        """
        self.dependency_graph = nx.DiGraph()
        self.name_to_component = dict()

        # Verify that the same keys exist in both dicts
        assert dependency_map.keys() == components.keys(), \
            f"Component and dependency maps should have similar keys"

        # # Mapping from component name to dependencies
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
                if not dep in components:
                    logger.error("not seen")
                    raise Exception(
                        f"Unseen component added as dependency {dep}"
                    )
                self.dependency_graph.add_edge(components[dep], components[name])

            # NOTE: Cycles are not supported
            if self._does_cycle_exist(self.dependency_graph):
                raise Exception(f"Cycle found in execution logic")

            self.name_to_component[name] = components[name]

        self.component_to_name : Dict[Component, name] = {
            v : k for k,v in self.name_to_component.items()
        }





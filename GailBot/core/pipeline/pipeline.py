# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:13:08
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-02-17 09:46:18
# Standard library imports
from typing import List, Any, Dict, Tuple
import time

# Local imports
from .logic import Logic
from .stream import Stream
from .component import Component, ComponentState
from ..utils.threads import ThreadPool
# Third party imports
import networkx as nx


class Pipeline:
    """
    Component that can be used to connect and execute dependant components,
    maintaining as much concurrency as possible.
    """

    def __init__(self, name: str, num_threads: int = 10) -> None:
        """
        Args:
            name (str): Name of the pipeline.
            num_threads (int): Number of threads that can be used.
        """
        self.thread_pool = ThreadPool(num_threads)
        self.thread_pool.spawn_threads()
        self.dependency_graph = nx.DiGraph()
        self.executed_graph_view = nx.DiGraph()
        # Mapping from component name to node in dependency graph
        self.name_to_dependency_node = dict()
        self.pipeline_name = name
        self.logic = None
        self.base_input = None

    def set_logic(self, logic: Logic) -> bool:
        """
        Set an instantiated logic component that defines the overall logic
        for the pipeline.

        Args:
            logic (Logic)

        Returns:
            (bool): True if successfully set. False otherwise.
        """
        self.logic = logic
        return True

    def set_base_input(self, data: Any) -> bool:
        """
        Set the base input that is passed to every component. This is useful
        for components that might need an external input.

        Args:
            data (Any): External input to components.

        Returns:
            (bool): True if successfully set. False otherwise.
        """
        self.base_input = Stream(data)
        return True

    def add_component(self, name: str, instantiated_object: object,
                      source_components: List[str] = []) -> bool:
        """
        Add a component to the pipeline.
        Note that the Logic for the pipeline must be set before components
        can be added and the logic must support, by name, the component
        that is being added. A component will not be added if it creates a
        dependency cycle with another component.

        Args:
            name (str):
                Name of the component. Must be the same as the component name
                defined in the logic.
            instantiated_object (object):
                Instantiated component that will be passed to
                Logic.get_processor at runtime.
            source_components (List[str]):
                List of the names of components, that have already been added,
                whose output this component is dependant on.

        Raises:
            (Exception):
                If logic is undefined, source component is invalid, or
                component is not supported in the logic.

        Returns:
            (bool): True if the component is added. False otherwise.
        """
        if self.logic == None:
            raise Exception("Logic must be defined before adding components")
        if not all([source in self.name_to_dependency_node.keys()
                    for source in source_components]):
            raise Exception("Source component is invalid")
        if not self.logic.is_component_supported(name):
            raise Exception("Component not supported in logic")
        # Component cannot be re-added
        if name in self.name_to_dependency_node:
            raise Exception("Component {} already exists and cannot be "
                            "re-added".format(name))
        # Component cannot have a circular dependency
        if name in source_components:
            raise Exception("Cannot have circular dependency on component")
        component = self._create_component(name, instantiated_object)
        self.dependency_graph.add_node(component)
        for source in source_components:
            self.dependency_graph.add_edges_from([
                (component, self.name_to_dependency_node[source])])
        if self._does_cycle_exist(self.dependency_graph):
            self.dependency_graph.remove_node(component)
            return False
        self.name_to_dependency_node[name] = component
        return True

    def get_name(self) -> str:
        """
        Obtain name of the pipeline.

        Returns:
            (str): Name of the pipeline
        """
        return self.pipeline_name

    def get_component_names(self) -> List[str]:
        """
        Obtain the name of all components that have been added.

        Returns:
            (List[str]): Name of all components that have been added.
        """
        return list(self.name_to_dependency_node.keys())

    def get_component_dependencies(self, component_name: str) -> List[str]:
        """
        Obtain all the components that the specified component is dependant on.

        Args:
            component_name (str): Name of the component.

        Raises:
            (Exception): If the component is not defined.

        Returns:
            (List[str]): Names of the component that the specified component
            is dependant on.
        """
        if not component_name in self.name_to_dependency_node:
            raise Exception("Invalid component")
        dependencies = list(self.dependency_graph.neighbors(
            self.name_to_dependency_node[component_name]))
        return [dependency.get_name() for dependency in dependencies]

    def get_number_of_dependencies(self, component_name: str) -> int:
        """
        Obtain the number of dependencies of the specified component.

        Args:
            component_name (str): Name of the component.

        Raises:
            (Exception): If the component is not defined.

        Returns:
            (int): Number of dependencies.
        """
        return len(self.get_component_dependencies(component_name))

    def get_execution_summary(self) -> Dict:
        """
        Obtain an execution summary for the pipeline that describes the
        result, runtime, and state of all components in the pipeline.

        Returns:
            (Dict):
                Mapping from the name of a component to a dictionary with the
                keys: result, runtime_seconds, and state. State can be one of
                successful, ready, or failed.
        """
        results = dict()
        for component in self.executed_graph_view:
            results[component.get_name()] = {
                "result": component.get_result(),
                "runtime_seconds": component.get_runtime(),
                "state": component.get_state().value}
        return results

    def get_successful_components(self) -> List[str]:
        """
        Obtain names of all components that were successfully executed.

        Returns:
            (List[str]): Names of all components that have state successful.
        """
        try:
            return [component.get_name() for component in
                    self.executed_graph_view.nodes
                    if component.get_state() == ComponentState.successful]
        except:
            return list()

    def get_failed_components(self) -> List[str]:
        """
        Obtain names of all components that failed execution.

        Returns:
            (List[str]): Names of all components that have state failed.
        """
        try:
            return [component.get_name() for component in
                    self.executed_graph_view.nodes
                    if component.get_state() == ComponentState.failed]
        except:
            return list()

    def get_executed_components(self) -> List[str]:
        """
        Obtain names of all components that started execution.

        Returns:
            (List[str]):
                Names of all components that have state successful or failed.
        """
        result = self.get_successful_components()
        result.extend(self.get_failed_components())
        return result

    def get_unexecuted_components(self) -> List[str]:
        """
        Obtain names of all components whose execution was not started.

        Returns:
            (List[str]): Names of all components that have state ready.
        """
        try:
            return [component.get_name() for component in
                    self.executed_graph_view.nodes
                    if component.get_state() == ComponentState.ready]
        except:
            return list()

    def print_dependency_graph(self) -> None:
        """
        Print a graph showing the dependencies of all components in the pipeline.
        """
        for name in self.name_to_dependency_node.keys():
            print("{} -- dependant on --> {}".format(
                name, self.get_component_dependencies(name)))

    def execute(self) -> None:
        """
        Execute all the components in the pipeline.

        Raises:
            (Exception): If the Logic is not set.
        """
        self._reset_dependency_graph_after_execution()
        if self.logic == None:
            raise Exception("Logic for pipeline undefined")
        execution_graph, name_to_dependency_mapping = \
            self._generate_execution_graph(self.dependency_graph)
        while True:
            executable_components = self._get_executables(execution_graph)
            if len(executable_components) == 0:
                self.executed_graph_view = self.dependency_graph.copy()
                #self.executed_graph_view = deepcopy(self.dependency_graph)
                return
            for component in executable_components:
                self.thread_pool.add_task(
                    self._execute_component,
                    [component, name_to_dependency_mapping,
                     self.base_input], {})
            self.thread_pool.wait_completion()
            self._cut_completed_vertices(execution_graph)

    def reset_pipeline(self) -> bool:
        """
        Reset the pipeline, removing any components, Logic, and base input
        that were added.

        Returns:
            (bool): True if successfully reset. False otherwise.
        """
        self.dependency_graph = nx.DiGraph()
        self.executed_graph_view = nx.DiGraph()
        self.name_to_dependency_node = dict()
        self.logic = None
        self.base_input = None
        return True

    ########################### PRIVATE METHODS #############################

    def _create_component(self, name: str, instantiated_object: object) \
            -> Component:
        """
        Initialize a Component.

        Args:
            name (str): Name of the component.
            instantiated_object (object)

        Returns:
            (Component): Instantiated object.
        """
        return Component(name, instantiated_object)

    def _get_executables(self, graph: nx.Graph) -> List[Component]:
        """
        Obtain all the components that can be executed i.e., all components
        that do not have any failed or ready dependencies.

        Args:
            graph (nx.Graph)

        Returns:
            (List[Component]):
                All components that can be executed and whose dependencies have
                been fullfilled.
        """
        executables = list()
        for component, val in graph.out_degree:
            if val == 0 and component.get_state() == ComponentState.ready:
                executables.append(component)
        return executables

    def _cut_completed_vertices(self, graph: nx.Graph) -> None:
        """
        Remove all components that are successfull and do not have any
        failed or ready dependencies from the dependency graph.

        Args:
            graph (nx.Graph)
        """
        out_view = list(graph.out_degree)
        for component, val in out_view:
            if component.get_state() == ComponentState.successful and val == 0:
                graph.remove_node(component)

    def _execute_component(self, component: Component,
                           name_to_dependency_node: Dict[str, Component],
                           base_input: Any) -> None:
        """
        Execute the given component by running it through the pre_processor,
        processor, and post-processor.
        Sets the state to successfull if the component is executed fully.
        Otherwise sets the state to Failed.

        Args:
            component (Component): Reference to component to execute.
            name_to_dependency_node (Dict[str,Component]):
                Mapping from name to component ref for the given graph.
            base_input (Any): Base input to the pipeline.
        """
        try:
            pre_processor = self.logic.get_preprocessor(component.get_name())
            processor = self.logic.get_processor(component.get_name())
            post_processor = self.logic.get_postprocessor(component.get_name())
            start_time = time.time()
            inputs = {
                "base": base_input}
            dependency_names = self.get_component_dependencies(
                component.get_name())
            for name in dependency_names:
                dependency = name_to_dependency_node[name]
                inputs[dependency.get_name()] = dependency.get_result()
            result_stream = \
                post_processor(
                    processor(
                        component.get_instantiated_object(),
                        pre_processor(inputs)))
            component.set_runtime(time.time() - start_time)
            component.set_state(ComponentState.successful)
            component.set_result(result_stream)
        except Exception:
            component.set_state(ComponentState.failed)
        finally:
            self._sync_execution_with_dependency_graph(component)

    def _sync_execution_with_dependency_graph(self, component: Component) \
            -> None:
        """
        Given a component, syncs all its results to the component with
        the same name in self.dependency_graph

        Args:
            component (Component): Component whose values are to be copied.
        """
        dep_node = self.name_to_dependency_node[component.get_name()]
        dep_node.set_runtime(component.get_runtime())
        dep_node.set_state(component.get_state())
        dep_node.set_result(component.get_result())

    def _reset_dependency_graph_after_execution(self) -> None:
        """
        Resets all the component nodes in the dependency graph.
        """
        for component in self.name_to_dependency_node.values():
            component.set_state(ComponentState.ready)
            component.set_runtime(0)
            component.set_result(None)

    def _does_cycle_exist(self, graph: nx.Graph) -> bool:
        """
        Return True if there are any cycles in the graph. False otherwise.
        """
        try:
            nx.find_cycle(graph, orientation="original")
            return True
        except:
            return False

    def _generate_execution_graph(self, graph: nx.Graph) \
            -> Tuple[nx.Graph, Dict[str, Component]]:
        """
        Generate an execution graph based on the provided graph.

        Args:
            graph (nx.Graph): Original graph that execution graph is based on.

        Returns:
            (Tuple[nx.Graph,Dict[str,Component]]):
                execution graph + mapping of component names to reference in
                execution graph.
        """
        name_to_node_mapping = dict()
        execution_graph = graph.copy(as_view=False)
        #execution_graph = deepcopy(graph)
        for node in execution_graph.nodes:
            name_to_node_mapping[node.get_name()] = node
        return (execution_graph, name_to_node_mapping)

# Standard library imports
from typing import List, Any, Dict
import time
# Local imports
from .logic import Logic
from .stream import Stream
from .component import Component, ComponentState
from ...utils.threads import ThreadPool
# Third party imports
import networkx as nx

class Pipeline:

    def __init__(self, name : str, num_threads : int = 10) -> None:
        self.name = name
        self.logic = None
        self.thread_pool = ThreadPool(num_threads)
        spawned = self.thread_pool.spawn_threads()
        self.base_input = None
        self.graph = nx.DiGraph()
        self.components = dict()

    def set_logic(self, logic  : Logic) -> bool:
        self.logic = logic
        return True

    def set_base_input(self, data : Any) -> bool:
        self.base_input = Stream(data)
        return True

    def add_component(self, name : str, instantiated_object : object,
            input_sources : List[str] = []) -> bool:

        if self.logic == None:
            raise Exception("Logic must be defined before adding components")
        if not all([source in self.components.keys() \
                for source in input_sources]):
            raise Exception("Component input source invalid")
        if not self.logic.is_component_supported(name):
            raise Exception("Component not supported in logic")
        component = self._create_component(name, instantiated_object)
        self.components[name] = component
        self.graph.add_node(component)
        for source in input_sources:
            self.graph.add_edges_from([
                (component,self.components[source])])
        if self._does_cycle_exist():
            self.graph.remove_node(component)
            return False
        return True

    def get_name(self) -> str:
        return self.name

    def get_component_names(self) -> List[str]:
        return list(self.components.keys())

    def get_component_dependencies(self, component_name : str) -> List[str]:
        if not component_name in self.components:
            raise Exception("Invalid component")
        dependencies =  list(self.graph.neighbors(
            self.components[component_name]))
        return [dependency.get_name() for dependency in dependencies]

    def get_execution_summary(self) -> Dict:
        results = dict()
        for component in self.components.values():
            results[component.get_name()] = {
                "result" : component.get_result(),
                "runtime_seconds" : component.get_runtime(),
                "state" : component.get_state().value}
        return results

    def get_successful_components(self) -> List[str]:
        return [component.get_name() for component in self.components.values() \
                    if component.get_state() == ComponentState.successful]

    def get_failed_components(self) -> List[str]:
        return [component.get_name() for component in self.components.values() \
                    if component.get_state() == ComponentState.failed]

    def get_executed_components(self) -> List[str]:
        return self.get_successful_components().extend(
            self.get_failed_components())

    def get_unexecuted_components(self) -> List[str]:
        return [component.get_name() for component in self.components.values() \
                    if component.get_state() == ComponentState.ready]

    def print_dependency_graph(self) -> None:
        for name in self.components.keys():
            print("{} -- dependant on --> {}".format(
                name, self.get_component_dependencies(name)))

    def execute(self) -> None:
        if self.logic == None:
            raise Exception("Logic for pipeline undefined")
        while True:
            executables = self._get_executables()
            if len(executables) == 0:
                return
            for executable in executables:
                self.thread_pool.add_task(
                    self._execute_component,[executable],{})
            self.thread_pool.wait_completion()
            self._cut_completed_vertices()

    ########################### PRIVATE METHODS #############################

    def _create_component(self, name : str, instantiated_object  : object) \
            -> Component:
        return Component(name,instantiated_object)

    def _get_executables(self) -> List[Component]:
        executables = list()
        for component, val in self.graph.out_degree:
            if val == 0 and component.get_state() == ComponentState.ready:
                executables.append(component)
        return executables

    def _cut_completed_vertices(self) -> None:
        out_view = list(self.graph.out_degree)
        for component, val in out_view:
            if component.get_state() == ComponentState.successful and val == 0:
                self.graph.remove_node(component)

    def _execute_component(self, component : Component) -> None:
        pre_processor = self.logic.get_preprocessor(component.get_name())
        processor = self.logic.get_processor(component.get_name())
        post_processor = self.logic.get_postprocessor(component.get_name())
        try:
            start_time = time.time()
            result_stream = \
                post_processor(
                    processor(
                        component.get_instantiated_object(),
                        pre_processor({"base" : self.base_input})))
            component.set_runtime(time.time() - start_time)
            component.set_state(ComponentState.successful)
            component.set_result(result_stream)
        except Exception:
            component.set_state(ComponentState.failed)

    def _does_cycle_exist(self) -> bool:
        try:
            nx.find_cycle(self.graph,orientation="original")
            return False
        except:
            return True


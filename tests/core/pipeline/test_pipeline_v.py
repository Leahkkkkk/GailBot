
from gailbot.core.pipeline import (
    Pipeline, Component, ComponentResult, ComponentState 
)
import time 
from typing import Dict 
from gailbot.core.utils.logger import makelogger
import pytest 


logger = makelogger("test_pipeline_vivian")

class TestComponent(Component):
    def __init__(self, name: str, sleeptime: int ):
        self.name = name 
        self.sleeptime = sleeptime
        
    def __call__(self, 
                 dependency_outputs: Dict[str, ComponentResult], 
                 *args, **kwargs) -> ComponentState:
        logger.info(self.name)
        time.sleep(self.sleeptime)
        return ComponentResult(
            state=ComponentState.SUCCESS, 
            result=self.name, 
            runtime=self.sleeptime
        )
    
    def __repr__(self):
        return f"Component {self.name}"

    @property
    def __name__(self):
        return self.name


class ErrorComponent(Component):
    def __init__(self, name: str, *args, **kwargs):
        self.name = name 
    
    def __call__(self, dependency_outputs: Dict[str, ComponentResult], *args, **kwargs) -> ComponentState:
        raise Exception("Component Execution Failed")
    
    @property
    def __name__(self):
        return self.name

def test_pipeline_has_cycle():
    components = {
        str(i): TestComponent(i, 3 * i) for i in range(1,6)
    } 
    
    with pytest.raises(Exception) as e :
        pipe = Pipeline(
            dependency_map={
            "1" : ["2"],
            "2" : ["1"],
            "3" : ["1"],
            "4" : ["1"],
            "5" : ["1"]
            }, 
            components=components,
            num_threads=1,
        )
    
        pipe._generate_dependency_graph(pipe.dependency_map)
        graph = pipe.get_dependency_graph()
        logger.info(e)

def test_pipeline_sequence():
    components = {
        str(i): TestComponent(i, i) for i in range(1,11)
    } 
     
    pipe = Pipeline(
        dependency_map={
            "1": [],
            "2": ["1"],
            "3": ["2"],
            "4": ["3"],
            "5": ["4"],
            "6": ["5"],
            "7": ["6"],
            "8": ["7"],
            "9": ["8"],
            "10":["9"],
        },
        components=components,
        num_threads=10
    )   
    
    res = pipe({})
    logger.info(res)
    
def test_thread_performance():
    components = {
        str(i): TestComponent(i, 10) for i in range( 1, 11)
    }
    pipe = Pipeline(
        dependency_map={ str(i) : [] for i in range(1,11)},
        components=components,
        num_threads=10
    )
    
    res = pipe({})
    for i in range(1, 11):
        assert res[str(i)] == ComponentState.SUCCESS
    

def test_pipeline_fail():
    components = {
        str(i): TestComponent(i, 1) 
                if i != 4
                else ErrorComponent(i) 
                for i in range(1,17)
    }
    
    pipe = Pipeline(
        dependency_map={
            "1": [], 
            "2": ["1"],
            "3": ["1"],
            "4": ["1"],
            "5": ["2", "1"],
            "6": [],
            "7": ["2", "5", "6"],
            "8": ["7", "6"],
            "9": ["2", "7", "8"],
            "10":["1", "4"],
            "11":["4", "1"],
            "12":["10","2"],
            "13":["10"],
            "14":["13"],
            "15":["14"],
            "16":["15"]
        },
        components=components,
        num_threads=3
    )
    
    res = pipe({})
    
    for i in range(1, 10):
        if i != 4:
            assert(res[str(i)] == ComponentState.SUCCESS) 
        else:
            assert(res[str(i)]) == ComponentState.FAILED
    
    for i in range(10, 16):
        assert(res[str(i)] == ComponentState.FAILED)
    logger.info(res)
    


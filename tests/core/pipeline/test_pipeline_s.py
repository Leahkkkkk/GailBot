from gailbot.core.pipeline import (
    Pipeline, Component, ComponentResult, ComponentState 
)
import time 
from typing import Dict 
from gailbot.core.utils.logger import makelogger
import pytest 


logger = makelogger("test_pipeline_siara")

class TestComponent(Component):
    def __init__(self, name: str, sleeptime: int):
        self.name = name 
        self.sleeptime = sleeptime
        
    def __call__(self, 
                 dependency_outputs: Dict[str, ComponentResult], 
                 msg: str = "Not Passed in",
                 *args, **kwargs) -> ComponentState:
        logger.info(self.name)
        logger.info(msg)
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
    
def test_pipeline():
    pass 

def test_result():
    """ create components """
    components = dict()
    for i in range (1, 6):
        components[str(i)] = TestComponent(i, i)
   
    pipe = Pipeline(
        dependency_map={
            "1" : [],
            "2" : ["1"],
            "3" : ["1"],
            "4" : ["1"],
            "5" : ["1"]       
        },
        components=components,
        num_threads=3      
    )
    res = pipe({"msg": "test_result function"})
    logger.info(res)
    
def test_component_info():
    """  test function to access component info 
    1. component_names
    2. is_component
    3. component_parents
    4. component_children
    """
    for i in range (1, 6):
        comp = TestComponent(f"test_comp #{i}", (1 * i))
        comp.__call__(comp)
        logger.info(f"component {i}: name: {comp.name}, is_component: {comp.is_component(comp.name)}, component_parents: {comp.component_parents(comp.name)}, component_children: {comp.component_children(comp.name)}")
        with pytest.raises(Exception) as e:
            logger.info(e)


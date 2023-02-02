from gailbot.core.pipeline import (
    Pipeline, Component, ComponentResult, ComponentState 
)
import time 
from typing import Dict 
from gailbot.core.utils.logger import makelogger


logger = makelogger("test_pipeline")


class TestComponent(Component):
    def __init__(self, name: str, testmsg: str, sleeptime: int ):
        self.name = name 
        self.testmsg = testmsg
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
    
    
    def test_pipeline():
        pass 
    
    
    def test_pipeline_has_cycle():
        pass 
    
    
    def test_component_info():
        """  test function to access component info 
        1. component_names
        2. is_component
        3. component_parents
        4. component_children
        """
        pass
    
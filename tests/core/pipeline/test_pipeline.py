# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-15 12:02:59
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-15 13:32:42

from gailbot.core.pipeline import (
    Pipeline, Component, ComponentResult, ComponentState
)
from typing import Dict, List, Any
from gailbot.core.utils.logger import makelogger
import time 

logger = makelogger("test-pipeline")

class FirstComponent(Component):
    def __init__(self, name):
        self.name = name 
        
    def __call__(
        self,
        base1,
        base2, 
        base3,
        base4,
        dependency_outputs : Dict[str, Any] = None 
    ) -> ComponentState:
        """Get a source and the associated settings objects and transcribe"""
        logger.info(base1)
        logger.info(base2)
        logger.info(base3)
        logger.info(base4)
        
        logger.info(f"Running component {self.name}")
        logger.info(f"Dependency outputs {dependency_outputs}")
        return ComponentResult(
            state=ComponentState.SUCCESS,
            result=self.name,
            runtime=0
        ) 

class TestComponent(Component):
    """
    Class for a component on which to run tests. Defines initialization 
        and calling functions.
    """
    def __init__(self, name : str):
        self.name = str(name)

    def __repr__(self):
        return self.name

    def __call__(
        self,
        dependency_outputs : Dict[str, Any] = None 
    ) -> ComponentState:

        """Get a source and the associated settings objects and transcribe"""
        logger.info(f"Running component {self.name}")
        logger.info(f"Dependency outputs {dependency_outputs}")
        return ComponentResult(
            state=ComponentState.SUCCESS,
            result=self.name,
            runtime=0
        )

    @property
    def __name__(self):
        return self.name

def test_pipeline():
    # 2 and 4 should run together
    components = {
        "1" : FirstComponent(1)
    }
    components.update ({
        str(i) : TestComponent(i) for i in range(2,6)
    })
    pipeline = Pipeline(
        dependency_map={
            "1" : [],
            "2" : [],
            "3" : [],
            "4" : [],
            "5" : []
        },
        components=components,
        num_threads=1
    )
    res = pipeline(base_input= ["hello"], additional_component_kwargs={})
    logger.info(res)

def test_base_input():
    components = {
        "1" : FirstComponent(1)
    }
    components.update ({
        str(i) : TestComponent(i) for i in range(2,10)
    })
    pipeline = Pipeline(
        dependency_map={
            "1" : [],
            "2" : ["1"],
            "3" : ["1"],
            "4" : ["2", "3"],
            "5" : ["3"],
            "6" : [],
            "7" : ["6"],
            "8" : [],
            "9" : ["8"]
        },
        components=components,
        num_threads=1
    )
    res = pipeline(
        base_input= ["base1", "base2", "base3", "base4"], 
        additional_component_kwargs={})
    logger.info(res) 
"""
Testing script for the pipeline component.
"""

# Standard library imports
from typing import Callable, Any, List, Dict
import time
# Local imports
from ..suites import TestSuite
from Src.Components.pipeline import Pipeline, Logic, Stream
# Third party imports


############################### GLOBALS #####################################

########################## TEST DEFINITIONS ##################################

### Logic class definition

class TestPipelineLogic(Logic):

    def __init__(self) -> None:
        super().__init__()
        # Adding all logic methods
        self._add_component_logic(
            "c1",self._preprocessor,self._processor_c1,self._post_processor)
        self._add_component_logic(
            "c2",self._preprocessor,self._processor_c2,self._post_processor)
        self._add_component_logic(
            "c3",self._preprocessor,self._processor_c3,self._post_processor)
        self._add_component_logic(
            "c4",self._preprocessor,self._processor_c4,self._post_processor)

    ########################### PRIVATE METHODS #############################


    def _preprocessor(self, streams : Dict[str,Stream]) -> Dict:
        return streams

    def _processor_c1(self, instantiated_obj : object, preprocessed_data : Dict) \
            -> Dict:
        print("Processing c1".format(instantiated_obj), preprocessed_data)
        return preprocessed_data

    def _processor_c2(self, instantiated_obj : object, preprocessed_data : Dict) \
            -> Dict:
        print("Processing c2".format(instantiated_obj), preprocessed_data)
        return preprocessed_data

    def _processor_c3(self, instantiated_obj : object, preprocessed_data : Dict) \
            -> Dict:
        print("Processing c3".format(instantiated_obj), preprocessed_data)
        raise Exception("c3 failed")
        #return preprocessed_data

    def _processor_c4(self, instantiated_obj : object, preprocessed_data : Dict) \
            -> Dict:
        print("Processing c4".format(instantiated_obj), preprocessed_data)
        return preprocessed_data

    def _post_processor(self, processed_data : Dict) -> Stream:
        return processed_data["base"]

### Pipeline tests

def pipeline_set_logic() -> bool:
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    return p.set_logic(logic)

def pipeline_set_base_input() -> bool:
    p = Pipeline("Test_pipeline")
    return p.set_base_input(list(range(1,100)))

def pipeline_add_component() -> bool:
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    s1 = p.add_component("c1",None,[])
    s2 = p.add_component("c2",None,["c1"])
    try:
        p.add_component("c10",None,[])
        p.add_component("c1", None, ["c10"])
        return False
    except:
        return s1 and s2

def pipeline_get_name() -> bool:
    name = "Test_pipeline"
    p = Pipeline(name)
    return p.get_name() == name

def pipeline_get_component_names() -> bool:
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1",None,[])
    p.add_component("c2",None,["c1"])
    try:
        p.add_component("c10",None,[])
        p.add_component("c1", None, ["c10"])
        return False
    except:
        return p.get_component_names() == ["c1","c2"]

def pipeline_get_component_dependencies() -> bool:
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1",None,[])
    p.add_component("c2",None,["c1"])
    try:
        p.add_component("c10",None,[])
        p.add_component("c1", None, ["c10"])
        return False
    except:
        return p.get_component_dependencies("c1") == [] and \
            p.get_component_dependencies("c2") == ["c1"]

def pipeline_get_execution_summary() -> bool:
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1",None,[])
    p.add_component("c2",None,["c1"])
    return type(p.get_execution_summary()) == dict

def pipeline_get_successful_components() -> bool:
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1",None)
    p.add_component("c2",None,["c1"])
    p.execute()
    return p.get_successful_components() == ["c1","c2"]

def pipeline_get_failed_components() -> bool:
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1",None)
    p.add_component("c2",None,["c1"])
    p.add_component("c3",None)
    p.execute()
    return p.get_failed_components() == ["c3"]

def pipeline_get_executed_components() -> bool:
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1",None)
    p.add_component("c2",None,["c1"])
    p.add_component("c3",None)
    p.execute()
    return p.get_executed_components() == ["c1","c2","c3"]

def pipeline_get_unexecuted_components() -> bool:
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1",None)
    p.add_component("c2",None,["c1"])
    p.add_component("c3",None)
    p.add_component("c4",None,["c3"])
    p.execute()
    return p.get_unexecuted_components() == ["c4"]

def pipeline_execute() -> bool:
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1",None)
    p.add_component("c2",None)
    p.add_component("c3",None,["c1","c2"])
    p.add_component("c4",None,["c2","c3"])
    p.execute()
    print(p.get_execution_summary())
    return True
####################### TEST SUITE DEFINITION ################################

def define_pipeline_test_suite() -> TestSuite:
    suite = TestSuite()
    # suite.add_test("pipeline_set_logic", (), True, True, pipeline_set_logic)
    # suite.add_test(
    #     "pipeline_set_base_input", (), True, True, pipeline_set_base_input)
    # suite.add_test(
    #     "pipeline_add_component", (), True, True, pipeline_add_component)
    # suite.add_test("pipeline_get_name", (), True, True, pipeline_get_name)
    # suite.add_test("pipeline_get_component_names", (), True, True,
    #     pipeline_get_component_names)
    # suite.add_test("pipeline_get_component_dependencies", (), True, True,
    #     pipeline_get_component_dependencies)
    # suite.add_test("pipeline_get_execution_summary", (), True, True,
    #     pipeline_get_execution_summary)
    # suite.add_test("pipeline_get_successful_components", (), True, True,
    #     pipeline_get_successful_components)
    # suite.add_test("pipeline_get_failed_components", (), True, True,
    #     pipeline_get_failed_components)
    # suite.add_test("pipeline_get_executed_components", (), True, True,
    #     pipeline_get_executed_components)
    # suite.add_test("pipeline_get_unexecuted_components", (), True, True,
    #     pipeline_get_unexecuted_components)
    suite.add_test("pipeline_execute",(), True, True, pipeline_execute)
    return suite




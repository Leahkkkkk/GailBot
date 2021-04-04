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
    pass

def pipeline_set_base_input() -> bool:
    pass

def pipeline_add_component() -> bool:
    pass

def pipeline_get_name() -> bool:
    pass

def pipeline_get_component_dependencies() -> bool:
    pass

def pipeline_print_dependency_graph() -> bool:
    pass

def pipeline_execute() -> bool:
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1",None)
    p.add_component("c2",None)
    p.add_component("c3",None,["c1"])
    p.add_component("c4",None,["c2","c3"])
    p.print_dependency_graph()
    p.execute()
    print(p.get_execution_summary())


####################### TEST SUITE DEFINITION ################################


def define_pipeline_test_suite() -> TestSuite:
    suite = TestSuite()
    suite.add_test("pipeline_execute",(), True, True, pipeline_execute)
    return suite




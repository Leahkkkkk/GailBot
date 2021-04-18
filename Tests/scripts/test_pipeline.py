"""
Testing script for the pipeline component.
"""

# Standard library imports
from typing import Callable, Any, List, Dict
import time
# Local imports
from ..suites import TestSuite
from Src.Components.pipeline import Pipeline, Logic, Stream, Component, ComponentState
from Src.Components.engines.google import GoogleCore, GoogleEngine
from Src.Components.io import IO
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

class TestPipelineLogic2(Logic):
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
        self._add_component_logic(
            "c5",self._preprocessor,self._processor_c5,self._post_processor)
    
    def _preprocessor(self, streams : Dict[str,Stream]) -> Dict:
        return streams

    def _processor_c1(self, instantiated_obj : object, preprocessed_data : Dict) \
            -> Dict:
        print("Processing c1".format(instantiated_obj), preprocessed_data)
        preprocessed_data["base"] = "hello!"
        return preprocessed_data

    def _processor_c2(self, instantiated_obj : object, preprocessed_data : Dict) \
            -> Dict:
        print("Processing c2".format(instantiated_obj), preprocessed_data)
        if preprocessed_data["c1"] == "hello!":
            print("c1 sucessfully changed base data and sent to to c2")
        return preprocessed_data
    
    def _processor_c3(self, instantiated_obj : object, preprocessed_data : Dict) \
            -> Dict:
        print("Processing c3".format(instantiated_obj), preprocessed_data)
        preprocessed_data["base"] = "world!"
        return preprocessed_data

    def _processor_c4(self, instantiated_obj : object, preprocessed_data : Dict) \
            -> Dict:
        print("Processing c4".format(instantiated_obj), preprocessed_data)
        if preprocessed_data["c1"] == "hello!" and preprocessed_data["c3"] == "world!":
            print("c1 sucessfully changed base data and sent to to c4, and c3 did the same")
        return preprocessed_data
    
    def _processor_c5(self, instantiated_obj : object, preprocessed_data : Dict) \
            -> Dict:
        print("Processing c5".format(instantiated_obj), preprocessed_data)
        raise Exception("c5 failed")
    
    def _post_processor(self, processed_data : Dict) -> Stream:
        return processed_data["base"]


class TestPipelineLogic3(Logic):
    def __init__(self) -> None:
        super().__init__()
        # Adding all logic methods
        self._add_component_logic(
            "c1",self._preprocessor,self._processor_c1,self._post_processor)
        self._add_component_logic(
            "c2",self._preprocessor,self._processor_c2,self._post_processor)
    
    def _preprocessor(self, streams : Dict[str,Stream]) -> Dict:
        return streams

    def _processor_c1(self, instantiated_obj : object, preprocessed_data : Dict) \
            -> Dict:
        print("Processing c1", preprocessed_data)
        preprocessed_data["base"] = instantiated_obj.is_file("Tests/Test_files/gettysburg.wav")
        return preprocessed_data

    def _processor_c2(self, instantiated_obj : object, preprocessed_data : Dict) \
            -> Dict:
        print("Processing c2", preprocessed_data)
        if preprocessed_data["c1"] == True:
            engine.configure("Tests/Test_files/gettysburg.wav", 22050, 1)
            utterances = engine.transcribe()
            print("engine output:", utterances)
        return preprocessed_data

    def _post_processor(self, processed_data : Dict) -> Stream:
        return processed_data["base"]

### Pipeline tests

def pipeline_set_logic() -> bool:
    """
    Tests:
        1. Verifies logic properly set in pipeline
    """
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    return p.set_logic(logic)

def pipeline_set_base_input() -> bool:
    """
    Tests:
        1. Verifies base input properly set in pipeline
    """
    p = Pipeline("Test_pipeline")
    return p.set_base_input(list(range(1,100)))

def pipeline_add_component() -> bool:
    """
    Tests:
        1. Verifies simple components can be added to pipeline
        2. Verifies unknown component cannot be added to pipeline
        3. Verifies unknown component cannot be made as a dependency
    """
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

def pipeline_add_component_without_logic() -> bool:
    """
    Tests:
        1. Verifies that exception thrown when adding a component without a 
           logic set
    """
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    try:
        p.add_component("c1",None)
        return False
    except:
        return True

def pipeline_add_component_unsupported_name() -> bool:
    """
    Tests:
        1. Verifies that component cannot be added if it is not a supported
           component in the logic
    """
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    try:
        p.add_component("not_component", None)
        return False
    except:
        return True

def pipeline_add_component_bad_source() -> bool:
    """
    Tests:
        1. Verifies that a component with an unknown source cannot be added
           to the pipeline
    """
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    try:
        p.add_component("c1",None)
        p.add_component("c2",None, ['not_component'])
        return False
    except:
        return True

# TODO: Bug, c2 can be set twice, overwrites dependency of c1 to c3
def pipeline_add_duplicate_component() -> bool:
    """
    Tests:
        1. Verifies that a component cannot be set twice
    """
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1",None)
    p.add_component("c3",None)
    p.add_component("c2",None, ['c1'])
    p.add_component("c2",None, ['c3'])
    print("check:", p.get_component_dependencies("c2"))
    return p.get_component_names() == ['c1', 'c3', 'c2'] and p.get_component_dependencies("c2") == ["c1"]

# TODO: Bug, can add c1 twice, and c1 can be dependent on itself
def pipeline_add_invalid_component() -> bool:
    """
    Tests:
        1. Verifies that a component cannot be dependent on itself
    """
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1",None)
    succ = p.add_component("c1",None, ['c1'])
    print("invalid:", p.get_component_dependencies("c1"))
    return not succ

def pipeline_add_multiple_component() -> bool:
    """
    Tests:
        1. Verifies that two components with no dependencies can be added to
           the pipeline successfully
    """
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    try:
        res1 = p.add_component("c1", None)
        res2 = p.add_component("c2", None)
        return res1 and res2
    except:
         return True

def pipeline_get_name() -> bool:
    """
    Tests:
        1. Getter for pipeline name
    """
    name = "Test_pipeline"
    p = Pipeline(name)
    return p.get_name() == name

def pipeline_get_component_names() -> bool:
    """
    Tests:
        1. Getter for component names
    """
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
    """
    Tests:
        1. Getter for component dependencies
    """
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
    """
    Tests:
        1. Getter for execution summary
    """
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1",None,[])
    p.add_component("c2",None,["c1"])
    return type(p.get_execution_summary()) == dict

def pipeline_get_successful_components() -> bool:
    """
    Tests:
        1. Getter for successful components
    """
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1",None)
    p.add_component("c2",None,["c1"])
    p.execute()
    return p.get_successful_components() == ["c1","c2"]

def pipeline_get_failed_components() -> bool:
    """
    Tests:
        1. Getter for failed components
    """
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1",None)
    p.add_component("c2",None,["c1"])
    p.add_component("c3",None)
    p.execute()
    return p.get_failed_components() == ["c3"]

def pipeline_get_executed_components() -> bool:
    """
    Tests:
        1. Getter for executed components
    """
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1",None)
    p.add_component("c2",None,["c1"])
    p.add_component("c3",None)
    p.execute()
    return p.get_executed_components() == ["c1","c2","c3"]

def pipeline_get_unexecuted_components() -> bool:
    """
    Tests:
        1. Getter for unexcuted components
    """
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1",None)
    p.add_component("c2",None,["c1"])
    p.add_component("c3",None)
    p.add_component("c4",None,["c3"])
    p.execute()
    return p.get_unexecuted_components() == ["c4"]

def pipeline_simple_passing() -> bool:
    """
    Tests:
        1. Execution of pipeline that passes strings of data between each
    """
    logic = TestPipelineLogic2()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1",None)
    p.add_component("c2",None,["c1"])
    p.execute()
    return True

def pipeline_two_dependencies() -> bool:
    """
    Tests:
        1. Execution of pipeline that passes strings of data between each with
           more complicated dependencies
    """
    logic = TestPipelineLogic2()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1",None)
    p.add_component("c3",None)
    p.add_component("c4",None, ["c1", "c3"])
    p.execute()
    return True

def pipeline_pass_data_despite_nondependent_failure() -> bool:
    """
    Tests:
        1. Execution of pipeline with partial failures in pipeline, ensures
           the successful parts of pipeline run despite failure
    """
    logic = TestPipelineLogic2()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1",None)
    p.add_component("c3",None)
    p.add_component("c4",None, ["c1", "c3"])
    p.add_component("c5", None)
    p.execute()
    return p.get_failed_components() == ["c5"] and p.get_successful_components() == ["c1", "c3", "c4"]

def pipeline_execute_two_dependencies_one_failure() -> bool:
    """
    Tests:
        1. Execution of pipeline with a failure that affects other components,
           ensures affected parts of pipeline do not run 
    """
    logic = TestPipelineLogic2()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1",None)
    p.add_component("c5", None)
    p.add_component("c4",None, ["c1", "c5"])
    p.execute()
    return p.get_failed_components() == ["c5"] and p.get_unexecuted_components() == ["c4"] and \
        p.get_successful_components() == ["c1"]

def pipeline_execute_simple_failure_dependency() -> bool:
    """
    Tests:
        1. Execution of pipeline with a failure that affects other components,
           ensures affected parts of pipeline do not run 
    """
    logic = TestPipelineLogic2()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c5", None)
    p.add_component("c1", None, ["c5"])
    p.execute()
    return p.get_successful_components() == [] and p.get_unexecuted_components() == ["c1"] and \
        p.get_failed_components() == ["c5"]

def pipeline_execute_failure_in_chain() -> bool:
    """
    Tests:
        1. Execution of pipeline with a failure that affects other components,
           ensures affected parts of pipeline do not run 
    """
    logic = TestPipelineLogic2()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c5", None)
    p.add_component("c1", None, ["c5"])
    p.add_component("c2", None, ["c1"])
    p.execute()
    return p.get_successful_components() == [] and p.get_unexecuted_components() == ["c1", "c2"] and \
        p.get_failed_components() == ["c5"]

def pipeline_execute() -> bool:
    """
    Tests:
        1. Pipeline execution of simple pipeline
    """
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

def pipeline_two_executions() -> bool:
    """
    Tests:
        1. Executing pipeline twice and confirming their executions are the same
    """
    logic = TestPipelineLogic2()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1",None)
    p.add_component("c2",None,["c1"])
    p.execute()
    execution1_succ = p.get_successful_components()
    print("execution1: ", p.get_execution_summary())
    p.execute()
    execution2_succ = p.get_successful_components()
    print("execution2: ", p.get_execution_summary())
    return execution1_succ == execution2_succ

def pipeline_execute_with_objects() -> bool:
    """
    Tests:
        1. Executing pipeline with instantiated objects
    """
    logic = TestPipelineLogic3()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1", IO())
    p.add_component("c2",GoogleEngine(IO()),["c1"])
    p.execute()
    return p.get_successful_components() == ["c1", "c2"] and p.get_failed_components() == [] and\
        p.get_unexecuted_components() == []

def pipeline_reset() -> bool:
    """
    Tests:
        1. Verifies that reset of pipeline is successful
    """
    logic = TestPipelineLogic2()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1",None)
    p.add_component("c2",None,["c1"])
    p.execute()
    p.reset_pipeline()
    return p.get_component_names() == [] and p.get_unexecuted_components() == []


### component tests ###

def component_get_set_state() -> bool:
    """
    Tests:
        1. Getter and setter of component state
    """
    component = Component("c1", None)
    state1 = component.get_state()
    res = component.set_state(ComponentState.failed)
    state2 = component.get_state()
    return res and state1 == ComponentState.ready and state2 == ComponentState.failed

def component_get_name() -> bool:
    """
    Tests:
        1. Getter of component name
    """
    component = Component("c1", None)
    return component.get_name() == "c1"

def component_get_inst_obj() -> bool:
    """
    Tests:
        1. Getter of instantiated object
    """
    component = Component("c1", None)
    return component.get_instantiated_object() == None

def component_get_res() -> bool:
    """
    Tests:
        1. Getter and setter of result
    """
    component = Component("c1", None)
    result_start = component.get_result()
    return result_start == None 

def component_get_set_runtime() -> bool:
    """
    Tests:
        1. Getter and setter of component runtime
    """
    component = Component("c1", None)
    runtime1 = component.get_runtime()
    res = component.set_runtime(10)
    runtime2 = component.get_runtime()
    return res and runtime1 == 0 and runtime2 == 10

def component_set_invalid_runtime() -> bool:
    """
    Tests:
        1. Verifies setter fails when runtime is negative
    """
    component = Component("c1", None)
    success = component.set_runtime(-100)
    return not success and component.get_runtime() == 0

## logic tests

def logic_is_component_supported_true() -> bool:
    """
    Tests:
        1. Verifies is_component_supported returns true with a known component
    """
    logic = TestPipelineLogic()
    return logic.is_component_supported("c1")

def logic_is_component_supported_false() -> bool:
    """
    Tests:
        1. Verifies is_component_supported returns false with a unknown component
    """
    logic = TestPipelineLogic()
    return not logic.is_component_supported("not_component")

def logic_get_supported_c_names() -> bool:
    """
    Tests:
        1. Verifies getter of component names
    """
    logic = TestPipelineLogic()
    names = logic.get_supported_component_names()
    return names == ['c1', 'c2', 'c3', 'c4']

####################### TEST SUITE DEFINITION ################################

def define_pipeline_test_suite() -> TestSuite:
    suite = TestSuite()

    ## Component Tests ##
    suite.add_test("component_get_set_state",(), True, True, component_get_set_state)
    suite.add_test("component_get_name",(), True, True, component_get_name)
    suite.add_test("component_get_inst_obj",(), True, True, component_get_inst_obj)
    suite.add_test("component_get_res",(), True, True, component_get_res)
    suite.add_test("component_get_set_runtime",(), True, True, component_get_set_runtime)
    suite.add_test("component_set_invalid_runtime",(), True, True, component_set_invalid_runtime)

    suite.add_test("pipeline_set_logic", (), True, True, pipeline_set_logic)
    suite.add_test(
        "pipeline_set_base_input", (), True, True, pipeline_set_base_input)
    suite.add_test(
        "pipeline_add_component", (), True, True, pipeline_add_component)
    suite.add_test(
        "pipeline_add_component_without_logic", (), True, True, pipeline_add_component_without_logic)
    suite.add_test(
        "pipeline_add_component_unsupported_name", (), True, True, pipeline_add_component_unsupported_name)
    suite.add_test(
        "pipeline_add_component_bad_source", (), True, True, pipeline_add_component_bad_source)
    suite.add_test(
        "pipeline_add_multiple_component", (), True, True, pipeline_add_multiple_component)
    suite.add_test(
        "pipeline_add_duplicate_component", (), True, True, pipeline_add_duplicate_component)
    suite.add_test(
        "pipeline_add_invalid_component", (), True, True, pipeline_add_invalid_component)
    suite.add_test("pipeline_get_name", (), True, True, pipeline_get_name)
    suite.add_test("pipeline_get_component_names", (), True, True,
        pipeline_get_component_names)
    suite.add_test("pipeline_get_component_dependencies", (), True, True,
        pipeline_get_component_dependencies)
    suite.add_test("pipeline_get_execution_summary", (), True, True,
        pipeline_get_execution_summary)
    suite.add_test("pipeline_get_successful_components", (), True, True,
        pipeline_get_successful_components)
    suite.add_test("pipeline_get_failed_components", (), True, True,
        pipeline_get_failed_components)
    suite.add_test("pipeline_get_executed_components", (), True, True,
        pipeline_get_executed_components)
    suite.add_test("pipeline_get_unexecuted_components", (), True, True,
        pipeline_get_unexecuted_components)
    suite.add_test("pipeline_execute",(), True, True, pipeline_execute)
    suite.add_test("pipeline_simple_passing",(), True, True, pipeline_simple_passing)
    suite.add_test("pipeline_two_dependencies",(), True, True, pipeline_two_dependencies)
    suite.add_test("pipeline_pass_data_despite_nondependent_failure",(), True, True, pipeline_pass_data_despite_nondependent_failure)
    suite.add_test("pipeline_execute_two_dependencies_one_failure",(), True, True, pipeline_execute_two_dependencies_one_failure)
    suite.add_test("pipeline_execute_simple_failure_dependency",(), True, True, pipeline_execute_simple_failure_dependency)
    suite.add_test("pipeline_execute_failure_in_chain",(), True, True, pipeline_execute_failure_in_chain)
    suite.add_test("pipeline_two_executions",(), True, True, pipeline_two_executions)
    #suite.add_test("pipeline_execute_with_objects",(), True, True, pipeline_execute_with_objects)
    suite.add_test("pipeline_reset",(), True, True, pipeline_reset)
    return suite




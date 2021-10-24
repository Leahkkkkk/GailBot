# Local imports
from Src.components.pipeline import Component, ComponentState
from Tests.pipeline.vardefs import *


############################### GLOBALS #####################################

############################### SETUP #####################################

########################## TEST DEFINITIONS #################################

def test_component_get_set_state() -> None:
    """
    Tests:
        1. Getter and setter of component state
    """
    component = Component("c1", None)
    state1 = component.get_state()
    res = component.set_state(ComponentState.failed)
    state2 = component.get_state()
    assert res and state1 == ComponentState.ready and state2 == ComponentState.failed


def test_component_get_name() -> None:
    """
    Tests:
        1. Getter of component name
    """
    component = Component("c1", None)
    assert component.get_name() == "c1"


def test_component_get_inst_obj() -> None:
    """
    Tests:
        1. Getter of instantiated object
    """
    component = Component("c1", None)
    assert component.get_instantiated_object() == None


def test_component_get_res() -> None:
    """
    Tests:
        1. Getter and setter of result
    """
    component = Component("c1", None)
    result_start = component.get_result()
    assert result_start == None


def test_component_get_set_runtime() -> None:
    """
    Tests:
        1. Getter and setter of component runtime
    """
    component = Component("c1", None)
    runtime1 = component.get_runtime()
    res = component.set_runtime(10)
    runtime2 = component.get_runtime()
    assert res and runtime1 == 0 and runtime2 == 10


def test_component_set_invalid_runtime() -> None:
    """
    Tests:
        1. Verifies setter fails when runtime is negative
    """
    component = Component("c1", None)
    success = component.set_runtime(-100)
    assert not success and component.get_runtime() == 0

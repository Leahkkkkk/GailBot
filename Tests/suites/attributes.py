# Standard library imports 
from enum import IntEnum

class TestAttributes(IntEnum):
    """
    Defines the attributes of a test.

    Inherits:
        IntEnum
    """
    name = 0
    args = 1
    status = 2
    expected_result = 3
    function_ptr = 4
    result = 5
    time_taken = 6

class TestSuiteAttributes(IntEnum):
    """
    Defines the attributes of a suite of tests.

    Inherits:
        IntEnum
    """
    tests = 0


# Standard library imports 
import time
from typing import Tuple, Any, List
# Local imports 
from .models import TestSuiteModel,TestModel
from .attributes import TestAttributes


class TestSuite:
    """
    Provides an API to run a series of tests.
    """

    def __init__(self) -> None:
        """
        Params:
            tests (Dict): Mappings of names to TestModel
        """
        self.tests = dict()
        
    def add_test(self,name : str, args : Tuple, status : bool,
            expected_result : Any ,function_ptr : Any) -> None:
        """
        Add a test to the suite of tests.
        
        Args:
            name (str): Name of the test
            status (bool): True if test is to be run. False otherwise.
            args (Tuple): Arguments to the test function.
            expected_result (Any): Expected result of the test.
            function_ptr (Any): Pointer to the test function
        """
        test = TestModel(name=name,args=args,status=status,
                         expected_result=expected_result,
                         function_ptr= function_ptr)
        self.tests[name] = test
    
    def remove_test(self,name : str) -> None:
        """
        Removes a test from the test suite if it exists

        Args:
            name (str): Name of test to be removed.
        """
        try:
            del self.tests[name]
        except KeyError:
            pass

    def run_single_test(self,name : str) -> None:
        """
        Runs the given test if it exists in the test suite.

        Args:
            name (str): Name of the test to be run.
        """
        try:
            args = self.tests[name].data(TestAttributes.args)
            function_ptr = self.tests[name].data(TestAttributes.function_ptr)
            start = time.time()
            result = function_ptr(*args)
            total_time = time.time() - start
            
            self.tests[name].set_data(TestAttributes.time_taken,total_time)
            self.tests[name].set_data(TestAttributes.result,result)
        except KeyError:
            pass
    
    def run_all_tests(self) -> None:
        """
        Runs all tests in the test suites.
        """
        for name, test in self.tests.items():
            if test.data(TestAttributes.status):
                self.run_single_test(name)
        
    ##### GETTERS ######
        
    def get_test_args(self, name : str) -> None:
        """
        Returns the arguments that will be passed to the given test when 
        it is run.

        Args:
            name (str): Name of the test
        """
        try:
            return self.tests[name].data(TestAttributes.args)
        except KeyError:
            return None

    def get_test_status(self,name : str) -> None:
        """
        Returns the status of the given test i.e. True if the test will be 
        executed and False otherwise.

        Args:
            name (str): Name of the test to be run.
        """
        try:
            return self.tests[name].data(TestAttributes.status) 
        except KeyError:
            return None
    
    def get_test_expected_result(self,name : str) -> None:
        """
        Returns the expected result of running the given test.

        Args:
            name (str): Name of the test.
        """
        try:
            return self.tests[name].data(TestAttributes.expected_result)
        except KeyError:
            return None
    
    def get_test_result(self,name : str) -> None:
        """
        Returns the result of the given test.

        Args:
            name (str): Name of the test.
        """
        try:
            return self.tests[name].data(TestAttributes.result)
        except KeyError:
            return None
    
    def get_test_time(self,name : str) -> None:
        """
        Get the time taken to run the given test.

        Args:
            name (str): Name of the test.
        """
        try:
            return self.tests[name].data(TestAttributes.time_taken)
        except KeyError:
            return None
        
    def get_tests(self) -> TestSuiteModel:
        """
        Returns all tests that are present in the suite.

        Returns:
            (TestSuiteModel): Suite of all tests
        """
        return TestSuiteModel(self.tests.values())
    
    def get_test_names(self) -> List[str]:
        """
        Returns the names of all the tests in the suite.

        Returns:
            (List[str]): Names of all tests in the suite.
        """
        return self.tests.keys()

    ##### SETTERS ######
        
    def set_test_status(self,name : str,status : bool) -> None:
        """
        Sets the status of the given test i.e. whether it will be run or not.

        Args:
            name (str): Name of the test
            status (bool): True if the test should be executed. False otherwise.
        """
        try:
            self.tests[name].set_data(TestAttributes.status,status)
        except KeyError:
            pass
"""
Script responsible for running all tests 
"""
# Standard library imports 
from typing import List, Dict
# Local imports 
from Tests import TestSuite
from Tests import define_network_test_suite, \
    define_util_thread_test_suite, define_io_test_suite, \
    define_organizer_test_suite, define_engines_test_suite

#### Helper functions for using test suite.

def print_summary(test_suite : TestSuite, name : str) -> None:
    """
    Print a summary of a single test from a given test suite.

    Args:
        test_suite (TestSuite)
        name (str): Name of the test in suite whose summary to print.
    """
    is_expected = test_suite.get_test_expected_result(
        name) == test_suite.get_test_result(name)
    print("*" * 10, end = " ") 
    print("{}".format(name), end=" ")
    print("*" * 10, end="\n\n")
    print("Function arguments: {}".format(test_suite.get_test_args(name)))
    print("Expected result: {}".format(
        test_suite.get_test_expected_result(name)))
    print("Actual result: {}".format(test_suite.get_test_result(name)))
    print("Result as expected: {}".format(is_expected))
    print("Time taken: {}".format(test_suite.get_test_time(name)))
    print("\n")

def print_all_summary(test_suite: TestSuite) -> None:
    """
    Print summary of all tests in the test suite.

    Args:
        test_suite (TestSuite)
    """
    test_names = test_suite.get_test_names()
    for name in test_names:
        # Only print summary if the test was run 
        if test_suite.get_test_status(name):
            print_summary(test_suite, name)

def run_single_test_suite(suites : Dict[str,TestSuite], name : str) -> None:
    """
    Run a single test suite from a dictionary of test suites 

    Args:
        suites (Dict[str,TestSuite]): Mapping of suite name to TestSuite object 
        name (str): Name of the test suite.
    """
    suites[name].run_all_tests()
    print_all_summary(suites[name])
    # try:
    #     suites[name].run_all_tests()
    #     print_all_summary(suites[name])
    # except (Exception ) as e:
    #     print("Exception thrown in '{}' test suite:\n {}".format(name,e))
        
def run_all_test_suites(suites : Dict[str,TestSuite]) -> None:
    """
    Run all test suites and print their summary 

    Args:
        suites (Dict[str,TestSuite]): Mapping of suite name to TestSuite object 
    """
    for suite in suites.values():
        suite.run_all_tests()
        print_all_summary(suite)

if __name__ == "__main__":
    # Defining all test suites 
    suites = {
        #"config_test_suite" : define_config_test_suite(),
        "network_test_suite" : define_network_test_suite(),
        "util_thread_test_suite" : define_util_thread_test_suite(),
        "io_test_suite" : define_io_test_suite(),
        "organizer_test_suite" : define_organizer_test_suite(),
        "engines_test_suite" : define_engines_test_suite()
    }
    run_single_test_suite(suites,"engines_test_suite")
    # Executing all test suites 
    # run_all_test_suites(suites)
    

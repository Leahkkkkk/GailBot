
# Standard library imports 
from typing import Any, List, Tuple
from abc import ABC,abstractmethod

class IModels(ABC):
    """
    Defines an interface for models that can be used to store data.

    Inherits:
        ABC
    """

    def __init__(self,**kwargs):
        pass

    @abstractmethod
    def data(self,index : Any) -> Any:
        """
        Obtain the data stored at the specified index

        Args:
            index (Any): Index identifying the data
        """
        pass 

    @abstractmethod
    def set_data(self,index : Any,item : Any) -> None:
        """
        Store the data item at the specified index in the model.

        Args:
            index (Any): Index identifying the data
            item (Any): data to be stored at the index.
        """
        pass 

    @abstractmethod
    def row_count(self) -> int:
        """
        Returns the number of data items present in the model.

        Returns:
            (int): No. of data items stored in the model.
        """
        pass 


class TestModel(IModels):
    """
    Defines a model to store test information

    Inherits:
        IModels
    """
    def __init__(self,name : str ,status : bool, args : Tuple,
                expected_result : Any, function_ptr : Any) -> None:
        """
        Args:
            name (str): Name of the test
            status (bool): True if test is to be run. False otherwise.
            args (Tuple): Arguments to the test function.
            expected_result (Any): Expected result of the test.
            function_ptr (Any): Pointer to the test function

        Params:
            name (str): Name of the test
            status (bool): True if test is to be run. False otherwise.
            args (Tuple): Arguments to the test function.
            expected_result (Any): Expected result of the test.
            function_ptr (Any): Pointer to the test function
            result (Any): Result of the test function.
            time_taken (int): Time taken to run the test
            items (List): Stores the items associated with this test.
        """
        super().__init__()
        self.name = name
        self.args = args
        self.status = status
        self.expected_result = expected_result
        self.function_ptr = function_ptr
        self.result = None
        self.time_taken = None
        self.items = [self.name,self.args,self.status,self.expected_result,
                      self.function_ptr,self.result,self.time_taken]

    def data(self,index : Any) -> Any:
        """
        Obtain the data stored at the specified index

        Args:
            index (Any): Index identifying the data
        """
        return self.items[index]

    def set_data(self,index : Any,item : Any) -> None:
        """
        Store the data item at the specified index in the model.

        Args:
            index (Any): Index identifying the data
            item (Any): data to be stored at the index.
        """
        self.items[index] = item

    def row_count(self) -> None:
        """
        Returns the number of data items present in the model.

        Returns:
            (int): No. of data items stored in the model.
        """
        return len(self.items)
    
class TestSuiteModel(IModels):
    """
    Defines a model to store a suite of tests

    Inherits:
        IModels
    """

    def __init__(self,tests : List[TestModel] = list()) -> None:
        """
        Args:
            tests (List[Any]): List of tests to be stored in the model

        Params:
            tests (List[TestModel])
            items (List[List[TestModel]]): Stores all tests in the suite
        
        """
        super().__init__() 
        self.tests = tests
        self.items = [self.tests]

    def data(self,index : Any) -> Any:
        """
        Obtain the data stored at the specified index

        Args:
            index (Any): Index identifying the data
        """
        return self.items[index]

    def set_data(self,index : Any,item : Any) -> None:
        """
        Store the data item at the specified index in the model.

        Args:
            index (Any): Index identifying the data
            item (Any): data to be stored at the index.
        """
        self.items[index] = item

    def row_count(self) -> None:
        """
        Returns the number of data items present in the model.

        Returns:
            (int): No. of data items stored in the model.
        """
        return len(self.items)





# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 15:53:06
# @Last Modified by:   Vivian Li and Siara Small
# @Last Modified time: 2023-01-26 16:07:48


from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, Future, wait
from typing import Tuple, Callable, List, Dict, Any, Union
from gailbot.core.utils.logger import makelogger

logger = makelogger("thread")

#### Custom Exceptions for Threads ####
class TaskNotFoundException(Exception):
    def __init__(self, task_key  = None ) -> None:
        self.task_key = task_key 
    def __str__(self) -> str:
        return "task" + str(self.task_key) + " is not found"
        
class TaskNotFinishedException(Exception):
    def __init__(self, task_key  = None ) -> None:
        self.task_key = task_key 
    def __str__(self) -> str:
        return "task" + str(self.task_key) + " is not finished"

class TaskCancelException(Exception):
    def __init__(self, task_key  = None ) -> None:
        self.task_key = task_key 
    def __str__(self) -> str:
        return "task" + str(self.task_key) + " cannot be canceled"

class TaskCreateError(Exception):
    def __init__(self, msg  = None ) -> None:
        self.msg = msg
    def __str__(self) -> str:
        return "task cannot be created due to the error " + self.msg
 
class ThreadError(Exception):
    def __init__(self, task_key  = None, msg: str = None ) -> None:
        self.task_key = task_key 
        self.msg = msg
        
    def __str__(self) -> str:
        return "task" + str(self.task_key) + " has an error " + self.msg

### Defines different possible statuses for a task ###
@dataclass
class Status:
    running = "RUNNING"
    pending = "PENDING"
    finished = "FINISHED"
    cancelled = "CANCELLED"
    error = "ERROR"

class ThreadPool(ThreadPoolExecutor):
    """
    Implement a threadpool that is able to run tasks parallel on different 
    threads, support functions to query tasks status, return task result and 
    add callback task to previous task   
    
    Inheritance:
    ThreadPoolExecutor 
    
    """
    def __init__(self, max_workers: int, *args, **kwargs) -> None:
        """ 
        Constructs a threadpool with the given size that is able to run tasks on different 
            threads.

        Args:
            max_workers (int):  the maximum number of tasks that will be run 
                                at the same time parallel
        """
        super().__init__(max_workers, *args, **kwargs)
        self.num_thread = max_workers              
        self.task_pool: Dict[Any, Future] = dict() # used to keeps track of the task status
        self.next_key = 0                          # next available key


    def get_num_threads(self) -> int:
        """
        Returns the number of threads available in the thread pool.

        Return:
            int: Integer value representing the number of 
                 threads in the given thread pool.
        """
        return self.num_thread

    def add_task(
        self, 
        task: Callable, 
        args: List = [], 
        kwargs: Dict = {},
        error_fun: Callable = None,
        key: Union[str, int] = None) -> Union[str, int]:
        """
        Adds the given task to the task pool.

        Args:
            fun: Callable: function that will be run in the threadpool
            args: List (Optional): a list argument to the function
            kwargs: Dict (Optional): a list of key word arguments to the function
            error_fun: Callable (Optional): a function to handle the error 
            key: Union[str, int](Optional): a user provided key that can be used to query 
                                the task progress and result after submitting it 
                                to the threadpool, caller is responsible for
                                providing unique key  
        Return:
            Union[str, int]: key that will be used to keep track of the task in the thread.
        """
        logger.info(f"the task {task} is being added to the thread")
        try:
            if not callable(task) or type(args) != list or type(kwargs) != dict:
                logger.error(f"type error in adding thread task ")
                raise TypeError("Type error in adding thread task.")
            worker = self.submit(task, *args, **kwargs)
            if key:
                self.task_pool[key] = worker
                return key
            else:
                self.task_pool[self.next_key] = worker
                self.next_key += 1
                return self.next_key - 1
        except Exception as e:
            logger.error(e, exc_info=e)
            if error_fun: 
                error_fun()
            else: 
                raise TaskCreateError(e)


    def check_task_status(self, key: Union[str, int]):
        """ 
        Return a string representing the status of the current task.

        Args:
            key: key to find the given task in the thread. 
        
        Returns: 
            String representing the status of the current task.
        """
        self._task_in_pool(key)
        future: Future = self.task_pool[key]
        return future._state

    def get_tasks_with_status(self, status: Status) -> List[Tuple[int, str]]:
        """ 
        Returns a list of tasks that match the status passed in by caller

        Args:
            status (Status): Status ot the task 
            
        Returns:
            A List[Tuple[int, str]] of tasks in the thread pool that
                match the requested status. 
        """
        return [task_key for task_key in self.task_pool.keys() if self.check_task_status(task_key) == status ]

    def get_task_result(self, key: Union[str, int], error_fun: Callable = None ):
        """ 
        Gets the result from the given task.

        Args:
            key (int): Key to find the given task in the thread pool.

        Return:
            If result is successfully obtained, return the result of the given task.
            else return false as default or call the error handling function passed 
            in from user
        """
        self._task_in_pool(key)
        try:
            future = self.task_pool[key]
            return future.result()
        except Exception as e:
            logger.error(f"task with task key {key} with future object {future} received an exception {e} , the function exception is {future.exception()}", exc_info=e)
            if error_fun and callable(error_fun): 
                logger.error(e)
                error_fun()
                return future.result()
            else: 
                raise ThreadError(key, f"received exception {e}") ##

    def completed(self, key: Union[str, int], error_fun: Callable = None )-> bool:
        """ 
        Checks if a given task has been completed.

        Args:
            key (int): Key to find the given task in the thread pool.
            error_fun: Callable function used if there is an error when 
                       executing the task. 

        Raise:
            Raise ThreadError if the result of the given task is not 
            successfully obtained.
        
        Return:
            bool: True if the given task has been completed, false if not.
        """
        self._task_in_pool(key)
        try:
            return self.task_pool[key].done()
        except: 
            if error_fun and callable(error_fun): 
                error_fun()
            else: 
                raise ThreadError(key, "ERROR: failed to get thread status")

    def wait_for_all_completion(self, error_fun: Callable = None ):
        """ 
        Wait for all tasks in the thread pool to be completed.

        Args:
            error_fun: Callable function used if there is an error when 
                       executing the task. 
        
        Raises:
            Raises a ThreadError if the function cannot be properly executed.

        Return: 
            Calls wait_for_task() for all tasks in the thread pool. 
        """
        futures = self.task_pool.values()
        wait(futures) 
        

    def wait_for_task(self, key: Union[str, int], error_fun: Callable = None ):
        """ 
        Waits for a certain task in the thread pool to be completed.

        Args:
            key (int): Key to find the given task in the thread pool.
            error_fun: Callable function used if there is an error when 
                       executing the task. 
        
        Raises:
            Raises a ThreadError if the task cannot be properly executed.

        Return:
            None
        """
        logger.info(f"wait for the task {key}")
        self._task_in_pool(key)
        future = self.task_pool[key]
        try:
            wait([future])
            assert not future.exception()
        except Exception as e:
            logger.error(e, exc_info=e)
            if error_fun: 
                error_fun()
            else: 
                raise ThreadError(key, f"received exception {e}")
    
    def cancel(self, key: Union[str, int]) -> bool:
        """
        Cancels the task at the given key.
 
        Args:
            key (int): Key to find the given task in the thread pool.

        Raises:
            TaskCancelException if the task at the given key cannot be 
            properly cancelled.
        
        Return:
            true if the thread is canceled 
        """
        self._task_in_pool(key)
        try:
            self.task_pool[key].cancel()
            if not self.task_pool[key].cancelled():
                raise TaskCancelException(key)
            return True
        except:
            return False

    def cancel_all(self) -> None:
        """ 
        Cancels all the running tasks in the thread pool.

        Raises:
            TaskCancelException if the current task cannot be properly cancelled.
        
        Return: 
            None
        """
        try:
            for task in self.task_pool.values():
                if not task.done():
                    task.cancel()
            return True
        except:
            return False

    def add_callback_with_arg(
        self, key: Union[str, int], fun: Callable, error_fun: Callable = None):
        """ 
        Adds a function to the thread as a callback of a previous function

        Args:
            key (int): key to find the given task.
            fun (Callable): function to be called as the callback. 
            error_fun: Callable function used if there is an error 
                       when executing the task.
                       
        Raises:
            ThreadError if the callback function cannot be added
            
        Return: 
            Returns the key that identify the newly added task 
        """
        self._task_in_pool(key)
        future = self.task_pool[key]
        res = [future.result()]
        if res and future.done():
            return self.add_task(fun, res)
        elif error_fun and callable(error_fun):
            error_fun()
        else: 
            raise ThreadError(key, "ERROR: Failed to add callback")
    
    def add_callback(self, key: Union[str, int], fun: Callable):
        """ add call back function fun that will run after the task identified
            by key is finished running 

        Args:
            key (Union[str, int]): the key that identifies the existing an task  
            fun (Callable): the call back function that will be added 
        """
        if not callable(fun):
            raise ThreadError(key, "ERROR: Non-function added as callback")
        future = self.task_pool[key]
        future.add_done_callback(fun)
    
    def add_callback_on_result(
        self, 
        key: Union[str, int], 
        fun: Callable, 
        args: List = [], 
        kwargs: Dict = {},  
        error_fun: Callable = None) -> int:
        """ 
        Adds a task to the thread after one task has finished running.

        Args:
            key (int): Key to find the current task.
            fun (Callable): function to be called after the current task has 
                            been completed. 
            error_fun: Callable function used if there is an error when
                      executing the task.

        Raises: 
            Raises ThreadError if the task identified by key is throws an 
            exception 
            
            Raises TypeError if the arguments is not passed in correctly 
        
        Returns:
            Returns the key that identify the newly added task 
        """
        self._task_in_pool(key)
        future = self.task_pool[key]
        wait([future])
        if not callable(fun) and type(args) == list and type(kwargs) == dict:
            logger.error(f"type error in adding thread task ")
            raise TypeError(f"Type error in adding callback on result to thread task {key}")
        try:
            future.result()
            return self.add_task(fun, args, kwargs)
        except Exception as e:
            logger.error(e, exc_info=e)
            if error_fun: 
                error_fun()
            else: 
                raise ThreadError(key, f"ERROR: Failed to add callback task, get error {e}")
    
    def is_busy(self) -> bool:
        """
        Determines if the thread queue has tasks in it.

        Returns:
            bool: True if the queue has non-zero tasks, false if otherwise.
        """
        return self._work_queue.qsize() != 0 
    
    def count_waiting_tasks(self) -> int:
        """
        Calculates the total number of tasks waiting in the queue.

        Returns:
            Integer representing the total waiting tasks
        """
        return self._work_queue.qsize()

    def count_completed_tasks(self) -> int: 
        """get the number of completed task 

        Returns:
            int: the number of completed task 
        """
        num = 0 
        for future in self.task_pool.values():
            if future.done():
                num += 1
        return num
    
    def count_total_tasks(self) -> int:
        """get the number of all the tasks that has been added to the threadpool,
           which includes failure task, completed task, running task and pending task 


        Returns:
            int:  the total number of task 
        """
        return len(self.task_pool)
        
    ############ private function  ##########
    def _task_in_pool(self, key:int) -> None :
        """ 
        Private function to determine if the given task is currently in the task pool.

        Args:
            key (int): key with which to find the given task in the thread.

        Raises:
            Raises TaskNotFoundException if the given task is not currently 
            in the thread.
        
        Return:
            None
        """
        if not key in self.task_pool:
            raise TaskNotFoundException(key)
    

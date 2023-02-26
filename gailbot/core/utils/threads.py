# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 15:53:06
# @Last Modified by:   Vivian Li and Siara Small
# @Last Modified time: 2023-01-26 16:07:48


from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, Future, wait
from queue import Queue
from enum import Enum
from typing import Tuple, Callable, List, Dict
from gailbot.core.utils.logger import makelogger

logger = makelogger("thread")

#### Custom Exceptions for Threads ####
class TaskNotFoundException(Exception):
    def __str__(self) -> str:
        return super().__str__()

class TaskNotFinishedException(Exception):
    pass

class TaskCancelException(Exception):
    pass

class TaskCreateError(Exception):
    pass 

class ThreadError(Exception):
    pass 

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
        self.task_pool: Dict[int, Future] = dict() # used to keeps track of the task status
        self.next_key = 0


    def get_num_threads(self) -> int:
        """
        Returns the number of threads available in the thread pool.

        Return:
            int: Integer value representing the number of 
                 threads in the given thread pool.
        """
        return self.num_thread

    def add_task(
        self, fun, args: List = None, kwargs: Dict = None,
             error_fun: Callable = None) -> int:
        """
        Adds the given task to the task pool.

        Args:
            fun: Callable: function that will be run in the threadpool
            args: List (Optional): a list argument to the function
            kwargs: Dict (Optional): a list of key word arguments to the function
            error_fun: Callable (Optional): a function to handle the error 
       
        Return:
            int: An integer id key that will be used to keep track of the task in the thread.
        """
        logger.info(f"args: {args}, kwargs {kwargs}")
        try:
            if args and kwargs:
                worker: Future = self.submit(fun, *args, **kwargs)
            elif args:
                logger.info(*args)
                worker: Future = self.submit(fun, *args)
            elif kwargs:
                worker: Future = self.submit(fun, **kwargs)
            else:
                worker: Future = self.submit(fun)
            # worker.add_done_callback(self._handle_error)
            self.task_pool[self.next_key] = worker
            self.next_key += 1
        except:
            if error_fun: error_fun()
            else: raise TaskCreateError
        else:
            return self.next_key - 1

    def check_task_status(self, key: int):
        """ 
        Return a string representing the status of the current task.

        Args:
            key: key to find the given task in the thread. 
        
        Returns: 
            String representing the status of the current task.
        """
        self._task_in_pool(key)
        exception = self.task_pool[key].exception()
        if exception:
            return Status.error
        return self.task_pool[key]._state

    def get_tasks_with_status(self, status: Status) -> List[Tuple[int, str]]:
        """ 
        Returns a list of tasks that match the status passed in by caller

        Args:
            status (Status): Status from set list of possible statuses
        
        Returns:
            A List[Tuple[int, str]] of tasks in the thread pool that
                match the requested status. 
        """
        return [id for id in self.task_pool.keys() if self.check_task_status(id) == status ]

    def get_task_result(self, key: int, error_fun: Callable = None ):
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
            assert not future.exception()
            return future.result()
        except:
            logger.error(future.exception())
            if error_fun: 
                error_fun()
            else: return False

    def completed(self, key, error_fun: Callable = None )-> bool:
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
            if error_fun: error_fun()
            else: raise ThreadError("ERROR: failed to get thread status")

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
        for task in self.task_pool.keys():
            self.wait_for_task(task, error_fun)

    def wait_for_task(self, key: int, error_fun: Callable = None ):
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
        self._task_in_pool(key)
        future = self.task_pool[key]
        try:
            wait([future])
            future.result()
            assert not future.exception()
        except Exception as e:
            if error_fun: error_fun()
            else: raise ThreadError(e)

    def cancel(self, key: int) -> bool:
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
                raise TaskCancelException("Failed to cancel thread")
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

    def add_callback_with_arg(self, key, fun: Callable, error_fun: Callable = None):
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
        elif error_fun:
            error_fun()
        else: 
            raise ThreadError("ERROR: Failed to add callback")
    
    def add_callback(self, key, fun: Callable):
        future = self.task_pool[key]
        future.add_done_callback(fun)
    
    def add_task_after(
        self, key, fun: Callable, args: List = None, 
        kwargs: Dict = None,  error_fun: Callable = None) -> int:
        """ 
        Adds a task to the thread after one task has finished running.

        Args:
            key (int): Key to find the current task.
            fun (Callable): function to be called after the current task has been completed. 
            error_fun: Callable function used if there is an error when executing the task.

        Raises: 
            Raises ThreadError if the error function is not successfully completed.
        
        Returns:
            Returns the key that identify the newly added task 
        """
        self._task_in_pool(key)
        future = self.task_pool[key]
        wait([future])
        try:
            future.result()
            return self.add_task(fun, args, kwargs)
        except:
            if error_fun: error_fun()
            else: raise ThreadError("ERROR: Failed to add task after")
    
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
            raise TaskNotFoundException("ERROR: task is not found")
    
    def _handle_error(self, future: Future) -> None :
        """
        Handles errors raised by finding the future of a task. 

        Args:
            future: Future to determine if there is an exception raised. 

        Raises:
            Raises ThreadError if the given future raises an exception.
            
        Return:
            None
        """
        if future.exception():
            pass 
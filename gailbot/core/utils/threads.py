# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 15:53:06
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-26 16:07:48


# TODO: Add a threading mechanism with a ThreadPool that is Event based i.e,
# each thread can send signals or status updates.
# Use case: We are running a process inside a thread and want to get its status
# periodically and want to run other functions at different stages
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, Future, wait
from queue import Queue
from enum import Enum
from typing import Tuple, Callable, List, Dict

# TODO: 
# 1. add documentation 
#    class doc -> Vivian 
#    function doc -> Siara
# 2. testing and fix bugs 
# 3. implement is_busy function



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
      
    Public Function:
    - get_num_thread() -> int 
    - add_task(fun, args, kwargs, error_fun) -> int 
    - check_task_status(key) -> Status 
    - get_task_with_status(status) -> List [Tuple[int, str]]
    - get_task_result(key, error_fun) 
    - completed(key, error_fun) -> bool 
    - wait_for_all_completion(error_fun) -> None 
    - wait_for_task(key, error_fun) 
    - cancel(key)
    - cancel_all(key)
    - add_callback(key, fun, error_fun)
    - add_task_after(key, fun, args, kwargs, error_fun)
    
    Exception: 
    
    """
    def __init__(self, max_workers: int, *args, **kwargs) -> None:
        """ constructing a threadpool that i sable to run tasks on different 
            thread 

        Args:
            max_workers (int):  the maximum number of tasks that will be run 
                                at the same time parallel
        """
        super().__init__(max_workers, *args, **kwargs)
        self.num_thread = max_workers
        self.task_pool: Dict[int, Future] = dict() # used to keeps track of the task status
        self.task_name: Dict[int, str] = dict()
        self.next_key = 0


    def get_num_threads(self) -> int:
        """
        Return the number of thread available in the thread pool

        Returns:
            int: _description_
        """
        return self.num_thread

    """ TODO: check if this can be cleaner """
    def add_task(
        self, fun, args: List = None, kwargs: Dict = None, error_fun: Callable = None) -> int:
        """
        Add the task to the task pool

        Args:
            task (Tuple[callable, List, Dict]): _description_
            key (int):  a key that identifies the name of the running task

        Returns:
            bool: return an id that will be used to keep track of the task
        """
        try:
            if args and kwargs:
                worker: Future = self.submit(fun, *args, **kwargs)
            elif args:
                worker: Future = self.submit(fun, *args)
            elif kwargs:
                worker: Future = self.submit(fun, **kwargs)
            else:
                worker: Future = self.submit(fun)
            worker.add_done_callback(self._handle_error)
            self.task_pool[self.next_key] = worker
            self.task_name[self.next_key] = fun.__name__
            self.next_key += 1
        except:
            if error_fun: error_fun()
            else: raise TaskCreateError
        else:
            return self.next_key - 1

    def check_task_status(self, key: int):
        """ return a string representing the status of the current task

        Args:
            a string that identify the task
        """
        self._task_in_pool(key)
        exception = self.task_pool[key].exception()
        if exception:
            return Status.error
        return self.task_pool[key]._state

    # TODO: Rename to something meaningful - maybe get_tasks_with_status...
    def get_tasks_with_status(self, status: Status) -> List[Tuple[int, str]]:
        """ returns a list of task that matched the status passed in by caller

        Args:
            status (Status): _description_
        """
        return [(id, self.task_name[id])
                for id in self.task_pool.keys()
                if self.check_task_status(id) == status ]

    # TODO: Explain description + annotate return value.
    def get_task_result(self, key: int, error_fun: Callable = None ):
        """ ret

        Args:
            id (int): _description_

        Returns:
            int: _description_
        """
        self._task_in_pool(key)
        try:
            return self.task_pool[key].result()
        except:
            if error_fun: error_fun()
            else: raise ThreadError

    def completed(self, key, error_fun: Callable = None )-> bool:
        """ check if a given task is completed

        Args:
            key (_type_): _description_

        Returns:
            bool: _description_
        """
        self._task_in_pool(key)
        try:
            return self.task_pool[key].done()
        except: 
            if error_fun: error_fun()
            else: raise ThreadError

    def wait_for_all_completion(self, error_fun: Callable = None ):
        """ wait for all tasks to be completed

        """
        for task in self.task_pool.keys():
            self.wait_for_task(task, error_fun)

    def wait_for_task(self, key: int, error_fun: Callable = None ):
        """ wait for a certain task to be completed

        Args:
            key (int): _description_
        """
        self._task_in_pool()
        future = self.task_pool[key]
        try:
            future.result()
            assert not future.exception()
        except:
            if error_fun: error_fun()
            else: raise ThreadError


    def cancel(self, key: int):
        """_summary_

        Args:
            key (int): _description_

        Raises:
            TaskCancelException: _description_
        """
        self._task_in_pool(key)
        try:
            self.task_pool[key].cancel()
            if not self.task_pool[key].cancelled():
                raise TaskCancelException()
        except:
            print("running task cannot be cancelled")

    def cancel_all(self):
        """ cancel all the running task

        Raises:
            TaskCancelException: _description_
        """
        try:
            for task in self.task_pool.values():
                if not task.done():
                    task.cancel()
        except:
            raise TaskCancelException()

    """ TODO: Test error  """
    def add_callback(self, key, fun: Callable, error_fun: Callable = None):
        """ add a function to the thread as a callback of a previous function
        Args:
            fun (Callable): _description_
        """
        self._task_in_pool(key)
        future = self.task_pool[key]
        res = [future.result()]
        if res and future.done():
            return self.add_task(fun, res)
        elif error_fun:
            error_fun()
        else: 
            raise ThreadError
    
    
    """ TODO: Test error 
              Test adding task with / without args and kwargs 
              Change name
            """
    def add_task_after(
        self, key, fun: Callable, args: List = None, 
        kwargs: Dict = None,  error_fun: Callable = None):
        """ add a task to the thread after one task finished running

        Args:
            key (_type_): _description_
            fun (Callable): _description_

        Returns:
            _type_: _description_
        """
        self._task_in_pool(key)
        future = self.task_pool[key]
        wait([future])
        try:
            future.result()
            return self.add_task(fun, args, kwargs)
        except:
            if error_fun: error_fun()
            else: raise ThreadError
    
    def is_busy(self) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        return self._work_queue.qsize() != 0 
    
    def count_task_in_queue(self) -> int:
        """_summary_

        Returns:
            int: _description_
        """
        return self._work_queue.qsize()
        


    ############ private function  ##########

    def _task_in_pool(self, key:int):
        """ private function to check if the given task is in the task pool

        Args:
            key (int): _description_

        Raises:
            TaskNotFoundException: _description_
        """
        if not key in self.task_pool:
            raise TaskNotFoundException()
    
    def _handle_error(self, future: Future):
        if future.exception():
            raise ThreadError

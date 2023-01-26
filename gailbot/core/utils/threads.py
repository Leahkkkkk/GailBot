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



#### Custom Exceptions for Threads ####

class TaskNotFoundException(Exception):
    pass

class TaskNotFinishedException(Exception):
    pass

class TaskCancelException(Exception):
    pass

#####


# TODO: Shouldn't this simply be an enum???
#####
# Proposed alternative

class Status(Enum):
    RUNNING = 0
    PENDING = 1
    FINISHED = 2
    CANCELLED = 3
#####


@dataclass
class Status:
    running = "RUNNING"
    pending = "PENDING"
    finished = "FINISHED"
    cancelled = "CANCELLED"


class ThreadPool(ThreadPoolExecutor):
    # TODO: Add class desc.

    def __init__(self, max_workers, *args, **kwargs) -> None:
        # TODO: Add docstring.
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


    def add_task(
        self, fun, args: List = None, kwargs: Dict = None) -> int:
        """
        Add the task to the task pool

        Args:
            task (Tuple[callable, List, Dict]): _description_
            key (int):  a key that identifies the name of the running task

        Returns:
            bool: return an id that will be used to keep track of the task
        """
        try:
            self.submit(fun, *args, **kwargs)

            if args and kwargs:
                worker: Future = self.submit(fun, *args, **kwargs)
            elif args:
                worker: Future = self.submit(fun, *args)
            elif kwargs:
                worker: Future = self.submit(fun, **kwargs)
            else:
                worker: Future = self.submit(fun)

            self.task_pool[self.next_key] = worker
            self.task_name[self.next_key] = fun.__name__
            self.next_key += 1
        except:
            raise Exception("task cannot be submitted")
        else:
            return self.next_key - 1

    def check_task_status(self, key: int):
        """ return a string representing the status of the current task

        Args:
            a string that identify the task
        """
        self._task_in_pool(key)
        return self.task_pool[key]._state

    # TODO: Rename to something meaningful - maybe get_tasks_with_status...
    def get_current(self, status: Status) -> List[int]:
        """ returns a list of task that matched the status passed in by caller

        Args:
            status (Status): _description_
        """
        return [(id, self.task_name[id])
                for id in self.task_pool.keys()
                if self.check_task_status(id) == status ]


    # TODO: Explain description + annotate return value.
    def get_task_result(self, key: int):
        """ ret

        Args:
            id (int): _description_

        Returns:
            int: _description_
        """
        self._task_in_pool(key)
        return self.task_pool[key].result()

    def completed(self, key)-> bool:
        """ check if a given task is completed

        Args:
            key (_type_): _description_

        Returns:
            bool: _description_
        """
        self._task_in_pool(key)
        return self.task_pool[key].done()

    def wait_for_completion(self):
        """ wait for all tasks to be completed

        """
        wait([task for task in self.task_pool.values()])

    def wait_for_task(self, key: int):
        """ wait for a certain task to be completed

        Args:
            key (int): _description_
        """
        self._task_in_pool()
        wait([self.task_pool[key]])


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

    def _task_in_pool(self, key:int):
        """ check if the given task is in the task pool

        Args:
            key (int): _description_

        Raises:
            TaskNotFoundException: _description_
        """
        if not key in self.task_pool:
            raise TaskNotFoundException()

    def add_callback(self, key, fun: Callable):
        """ add a function to the thread as a callback of a previous function

        Args:
            fun (Callable): _description_
        """
        self._task_in_pool(key)
        return self.add_task(fun, [self.task_pool[key].result()])

    # TODO: Raise exception or remove.
    def is_busy(self):
        pass


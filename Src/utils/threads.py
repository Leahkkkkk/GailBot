# Standard library imports
from threading import Thread
from queue import Queue
from typing import Callable, List, Dict, Any, Tuple


class ThreadWorker(Thread):
    """
    Responsible for creating and managing a single Thread that processes
    tasks from the given data queue.

    Inheritance:
        Thread:
    """

    def __init__(self, task_queue : "Queue[Tuple[Callable,List,Dict]]",
            except_callback : Callable[[None],None], is_daemon : bool = True) \
                -> None:
        """
        Args:
            task_queue (Queue[Tuple[Callable,List,Dict]]) :
                    Queue containing callbacks, args, and kwargs for all tasks.
            except_callback (Callable): Function to be executed in case of
                                    an exception
            is_daemon (bool): True to run as separate process. False otherwise.
                                default = True.
        """
        super().__init__()
        self.task_queue = task_queue
        self.daemon = is_daemon
        self.on_except = except_callback if except_callback != None else lambda: None
        # Start, which causes the run method to be invoked.
        self.start()

    def run(self) -> None:
        """
        Start threads and process while there are still tasks remaining.
        """
        while True:
            try:
                callback,args,kwargs = self.task_queue.get()
                try:
                    callback(*args, **kwargs)
                except:
                    try:
                        self.on_except(*args,**kwargs)
                    except:
                        pass
                finally:
                    self.task_queue.task_done()
            except:
                pass

class ThreadPool:
    """
    Responsible for creating and managing a pool of ThreadWorkers that
    collectively process the assigned tasks
    """

    def __init__(self, num_threads : int ) -> None:
        """
        Params:
            num_threads (int): No. of separate threads in this pool.
                            Must be greater than 0.
        """
        if num_threads <= 0:
            self.num_threads = 1
        else:
            self.num_threads = num_threads
        # Callbacks
        self.on_pool_end = lambda : None
        self.on_thread_except = lambda : None
        # Task queue
        self.task_queue = Queue()

    def set_on_pool_end(self, on_end_callback : Callable) -> bool:
        """
        Callable that is executed when all tasks in the thread pool have
        finished execution

        Args:
            on_end_callback (Callable): Callable executed on pool end

        Returns:
            (bool): True if successful. False otherwise.
        """
        if callable(on_end_callback):
            self.on_pool_end = on_end_callback
            return True
        return False

    def set_on_thread_except(self, on_thread_except_callback : Callable) -> bool:
        """
        Callable executed if any task fails and throws an exception

        Args:
            on_thread_except_callback (Callable): Callable to be executed on
                                                    exception.

        Returns:
            (bool): True if successful. False otherwise.
        """
        if callable(on_thread_except_callback):
            self.on_thread_except = on_thread_except_callback
            return True
        return False

    def get_num_threads(self) -> int:
        """
        Returns the no. of threads that are being used by the pool.

        Returns:
            (int): No. of threads being used.
        """
        return self.num_threads

    def add_task(self, callback : Callable, args : List = [],
            kwargs : Dict = {}) -> bool:
        """
        Add a callable task that will be processed by the thread pool.

        Args:
            callback (Callable): Callable that will be executed via a thread.
            args (List): Arguments to be passed to the Callable on execution.
                        Defaults to empty list.
            kwargs (Dict): Keywork arguments to be passed to the Callable on
                            execution.
                            Defaults to empty dictionary.

        Returns:
            (bool): True if successfully added. False otherwise.
        """
        if not callable(callback) or type(args) != list or type(kwargs) != dict:
            return False
        self.task_queue.put((callback,args,kwargs))
        return True

    def spawn_threads(self) -> bool:
        """
        Spawn threads to start processing assigned tasks.

        Returns:
            (bool): True if successful. False otherwise.
        """
        # Spawning threads
        if not self._is_pool_ready():
            return False
        for _ in range(self.num_threads):
            try:
                ThreadWorker(self.task_queue,self.on_thread_except)
            except:
                pass
        return True

    def wait_completion(self) -> bool:
        """
        Blocks execution until all tasks in the thread pool have been completed.
        Finally executes the on pool end function.

        Returns:
            (bool): True if successful. False otherwise.
        """
        self.task_queue.join()
        try:
            self.on_pool_end() if self.on_pool_end != None else None
            return True
        except:
            return False

    def _is_pool_ready(self) -> bool:
        """
        Determined whether the thread pool is ready to start.

        Returns:
            (bool): True if the pool is ready. False otherwise.
        """
        return True

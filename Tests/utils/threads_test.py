# Standard library imports
from typing import List
from queue import Queue
# Local imports
from Src.utils.threads import ThreadPool, ThreadWorker

############################### GLOBALS #####################################

############################### SETUP #####################################

def valid_on_except(status : List[bool], test_no: int) -> None:
    status[test_no] = False

def invalid_on_except():
    raise Exception

def valid_callback(status : List[bool], test_no : int) -> None:
    status[test_no] = True

def invalid_callback():
    print("Invalid callback")
    raise Exception

def on_pool_end():
    print("Ending")

########################## TEST DEFINITIONS #################################

def test_thread_worker_run() -> None:
    """
    Tests the run method of the ThreadWorker class

    Tests:
        1. Run ThreadWorker with valid parameters.
        2. Run a Thread with callback that throws an exception with
            valid on except
        3. Run a Thread with a valid invalid on except and invalid callback.
        4. Start a thread with the task_queue containing invalid data i.e. not
            callables.
        5. Start a thread that does not continaing a tuple of three elements in
            the queue.

    Returns:
        (bool): True if successful. False otherwise.
    """
    # Dictionary to keep track of status of different tests
    status = {}
    # Test 1
    task_queue = Queue()
    task_queue.put((valid_callback,[],{"status" : status, "test_no" : 1}))
    ThreadWorker(task_queue,valid_on_except,is_daemon=True)
    # Test 2
    task_queue = Queue()
    task_queue.put((invalid_callback,[],{"status" : status, "test_no" : 2}))
    ThreadWorker(task_queue,valid_on_except,is_daemon=True)
    # Test 3
    task_queue = Queue()
    task_queue.put((invalid_callback,[],{"status" : status, "test_no" : 3}))
    ThreadWorker(task_queue,invalid_on_except,is_daemon=True)
    # Test 4
    task_queue = Queue()
    task_queue.put(("What?",[],{"status" : status, "test_no" : 4}))
    ThreadWorker(task_queue,invalid_on_except,is_daemon=True)
    # Test 5
    task_queue = Queue()
    task_queue.put((valid_callback,None))
    ThreadWorker(task_queue,invalid_on_except,is_daemon=True)

    assert status[1] and not status[2] and \
        3 not in status and 4 not in status

def thread_pool_setters() -> None:
    """
    Tests all the setter methods for ThreadPool.

    Tests:
        1. Set valid args for all methods.
        2. Set invalid args for all methods.
        3. Set valid no. of threads.
        4. Set invalid no. of threads.

    Returns:
        (bool): True if successful. False otherwise.
    """
    num_threads = 1
    pool = ThreadPool(num_threads)
    assert pool.set_on_pool_end(on_pool_end) and \
        pool.set_on_thread_except(valid_on_except) and \
        not pool.set_on_pool_end(num_threads) and \
        not pool.set_on_thread_except(num_threads)

def thread_pool_getters() -> None:
    """
    Tests all the getter methods for ThreadPool.

    Tests:
        1. Test valid return type and value.

    Returns:
        (bool): True if successful. False otherwise.
    """
    pool = ThreadPool(100)
    num_threads = pool.get_num_threads()
    assert type(num_threads) == int and num_threads == 100

def thread_pool_add_task() -> None:
    """
    Tests all the add_task method for ThreadPool.

    Tests:
        1. Add a task with a valid callable
        2. Add task with invalid callable.
        3. Add args and kwargs with invalid type.

    Returns:
        (bool): True if successful. False otherwise.
    """
    pool = ThreadPool(1)
    assert pool.add_task(valid_callback,[],{"status" : {}, "test_no" : 1}) and\
            not pool.add_task(100,[],{}) and\
            not pool.add_task(100,{},[]) and \
            pool.add_task(valid_callback)

def thread_pool_spawn() -> None:
    """
    Spawns and wait for completion of all threads.

    Tests:
        1. Run ThreadWorker with valid parameters.
        2. Run a Thread with callback that throws an exception with
            valid on except
        3. Run a Thread with a valid invalid on except and invalid callback.
        4. Start a thread with the task_queue containing invalid data i.e. not
            callables.
        5. Start a thread that does not continaing a tuple of three elements in
            the queue.

    Returns:
        (bool): True if successful. False otherwise.
    """
    status = dict()
    pool = ThreadPool(5)
    pool.set_on_pool_end(on_pool_end)
    pool.set_on_thread_except(valid_on_except)
    tasks = [
        (valid_callback,[],{"status" : status, "test_no" : 1}),
        (invalid_callback,[],{"status" : status, "test_no" : 2}),
        ("What?",[],{"status" : status, "test_no" : 4}),
        (valid_callback,None)
    ]
    for task in tasks:
        pool.add_task(*task)
    pool.spawn_threads()
    success_1 = pool.wait_completion()
    pool.set_on_thread_except(invalid_callback)
    pool.add_task((invalid_callback,[],{"status" : status, "test_no" : 3}))
    success_2 = pool.wait_completion()
    assert status[1] and not status[2] and \
        3 not in status and 4 not in status and \
        success_1 and success_2
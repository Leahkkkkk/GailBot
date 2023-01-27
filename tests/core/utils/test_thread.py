""" TODO: test for callback / add_task_after
1. with more than 1 thread  (5 - 10) - Siara
2. make sure the callback function actually runs after the previous function finishes - Vivian
3. make sure if we have a lot of callback, the threadpool still runs (stress test) - Vivian 
4. test error handling function - Vivian 
5. test passing different number of arguments to add_task_after - Siara
"""

import pytest 
import time 
from gailbot.core.utils.threads import ThreadPool, Status

def worker_no_param():
    """
    Instantiate a thread worker with no parameters.
    """
    time.sleep(2)
    print("worker no param")

def worker_one_param(n: int):
    """
    Instantiate a thread worker with one parameter.
    """
    time.sleep(n)
    print(f"worker: {n}")

def worker_key_param(n: int, s = "Default"):
    """
    Instantiate a thread worker with default parameters.
    """
    time.sleep(n)
    print(str(n) + str(s))

def worker_with_return(n: int, result):
    """
    Instantiate a thread worker with no return value other than itself.
    """
    time.sleep(n)
    return result

def worker_test_callback(n):
    """
    Instantiate a thread worker that just returns its value.
    """
    return n 

def previous_worker(n, name):
    """
    Instantiate a thread worker that prints the name of the previous worker.
    """
    print(f"previous worker:{name}")
    time.sleep(n)
    return name 

def callback_worker(name):
    """
    Instantiate a thread worker that prints the name of the callback worker.
    """
    print(f"callback worker:{name}")



@pytest.mark.parametrize("size", [1,2,3])
def test_construction(size):
    """
    Test the construction of a thread pool with various sizes and ensure it can properly add tasks.
    """
    pool = ThreadPool(size)
    assert size == pool.get_num_threads()
    pool.add_task(worker_no_param)


@pytest.mark.parametrize("args, kwargs", [([1], {"s": "test"}), ([2], {"s": 123})] )
def test_with_arg(args, kwargs):
    """
    Test the addition of tasks with various parameters as arguments. 
    """
    pool = ThreadPool(2)
    pool.add_task(worker_one_param, args)
    pool.add_task(worker_key_param, args, kwargs)


@pytest.mark.parametrize("arg", ["string", 1 , [1, 2, 3, 4], (1, 2), {1: 2}])
def test_get_test_result(arg):
    """
    Test the correct result is returned from various tasks in the thread pool.
    """
    pool = ThreadPool(2)
    id = pool.add_task(worker_with_return, [1, arg])
    assert pool.get_task_result(id) == arg

@pytest.mark.parametrize("t",[2,3])
def test_thread_status(t):
    """
    Test the correct status is returned from various tasks in one thread.
    """
    pool = ThreadPool(5)
    threadIds = []
    for i in range(5):
        threadIds.append(pool.add_task(worker_one_param, [t]))
        print(pool.check_task_status(i))
        assert not pool.completed(i)
    time.sleep(t + 1)
    for id in threadIds:
        print(pool.check_task_status(id))
        assert  pool.completed(i)

@pytest.mark.parametrize("t, num_threads", [(2, 2), (5, 5), (3, 10)])
def test_get_current_status(t, num_threads):
    """
    Test the correct status is returned from various tasks in the thread pool.
    """
    pool = ThreadPool(num_threads)
    for i in range(10):
        pool.add_task(worker_one_param, [t])
    
    print(Status.pending)
    print(pool.get_tasks_with_status(Status.pending))
    time.sleep(t - 1)
    print(Status.running)
    print(pool.get_tasks_with_status(Status.running))
    time.sleep((10//num_threads + 1) * t)
    print(Status.finished)
    print(pool.get_tasks_with_status(Status.finished))

@pytest.mark.parametrize("t", [5])
def test_cancel(t):
    """
    Test that the status cancelled tasks are correctly updated.
    """
    pool = ThreadPool(1)
    for i in range(5):
        pool.add_task(worker_key_param, [t])
        pool.cancel(i) 
    for i in range(1, 5):
        assert pool.check_task_status(i) == Status.cancelled


@pytest.mark.parametrize("args",[[1,4], [1, "string"], [2, [1,2,3,4]]])
def test_thread_callback(args):
    """
    Tests the callback function is correctly called for a pool of 1 thread.
    """
    pool = ThreadPool(1)
    id_0 = pool.add_task(worker_with_return, args)
    id_1 = pool.add_callback(id_0, worker_test_callback)
    assert id_1 == id_0 + 1
    assert args[1] == pool.get_task_result(id_1)

@pytest.mark.parametrize("args",[[1,4], [1, "string"], [2, [1,2,3,4]]])
def test_mult_thread_callback(args):
    """
    Tests the callback function is correctly called for a pool of 10 threads.
    """
    pool = ThreadPool(10)
    id_0 = pool.add_task(worker_with_return, args)
    id_1 = pool.add_callback(id_0, worker_test_callback)
    assert id_1 == id_0 + 1
    assert args[1] == pool.get_task_result(id_1)
    assert pool.get_num_threads() == 10

@pytest.mark.parametrize("",[])
def test_multiple_thread_callback():
    pass

@pytest.mark.parametrize("",[])
def test_completed():
    pass

@pytest.mark.parametrize("",[])
def test_query_thread():
    pass


""" make sure the callback function actually runs after the previous function finishes"""
@pytest.mark.parametrize("",[])
def test_(args):
    pass 


def test_add_task_after():
    """
    Tests that add_task_after correctly adds a new task to the correct place in the thread pool."""
    pool = ThreadPool(10)
    for i in range(5):
        pool.add_task(previous_worker, [i, f"worker {i}"])
    
    for i in range(5):
        pool.add_task_after(i, lambda: callback_worker(f"worker {i}"))
        pool.add_callback(i, callback_worker)
        





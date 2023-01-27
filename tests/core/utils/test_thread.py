""" TODO: test for callback / add_task_after
1. with more than 1 thread  (5 - 10) - Siara
2. make sure the callback function actually runs after the previous function finishes - Vivian
3. make sure if we have a lot of callback, the threadpool still runs (stress test) - Vivian 
4. test error handling function - Vivian 
5. test passing different number of arguments to add_task_after - Siara
"""

import pytest 
import time 
from gailbot.core.utils.threads import ThreadPool, Status, ThreadError
import logging
from queue import Queue 


# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create a file handler
file_handler = logging.FileHandler('tests/core/utils/thread.log')
file_handler.setLevel(logging.DEBUG)

# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)


def sleep_two_sec():
    time.sleep(2)
    logger.info("worker no param")

def sleep_n_sec(n: int):
    time.sleep(n)
    logger.info(f"worker: {n}")

def sleep_n_sec_print(n: int, s = "Default"):
    time.sleep(n)
    logger.info(str(n) + str(s))

def sleep_n_sec_return(n: int, result):
    time.sleep(n)
    return result

def worker_test_callback(n):
    return n 

def previous_worker(n, name):
    logger.info(f"\u25B6 previous worker start:{name}\n")
    time.sleep(n)
    logger.info(f"\u23F9 previous worker finished:{name}\n")
    return name 

def callback_worker(name):
    logger.info(f"\u23F1 callback worker:{name}\n")


@pytest.mark.parametrize("size", [1,2,3])
def test_construction(size):
    pool = ThreadPool(size)
    assert size == pool.get_num_threads()
    pool.add_task(sleep_two_sec)

@pytest.mark.parametrize("args, kwargs", [([1], {"s": "test"}), ([2], {"s": 123})] )
def test_with_arg(args, kwargs):
    pool = ThreadPool(2)
    pool.add_task(sleep_n_sec, args)
    pool.add_task(sleep_n_sec_print, args, kwargs)


@pytest.mark.parametrize("arg", ["string", 1 , [1, 2, 3, 4], (1, 2), {1: 2}])
def test_get_test_result(arg):
    pool = ThreadPool(2)
    id = pool.add_task(sleep_n_sec_return, [1, arg])
    assert pool.get_task_result(id) == arg

@pytest.mark.parametrize("t",[2,3])
def test_thread_status(t):
    pool = ThreadPool(5)
    threadIds = []
    for i in range(5):
        threadIds.append(pool.add_task(sleep_n_sec, [t]))
        print(pool.check_task_status(i))
        assert not pool.completed(i)
    time.sleep(t + 1)
    for id in threadIds:
        print(pool.check_task_status(id))
        assert  pool.completed(i)

@pytest.mark.parametrize("t, num_threads", [(2, 2), (5, 5), (3, 10)])
def test_get_current_status(t, num_threads):
    pool = ThreadPool(num_threads)
    for i in range(10):
        pool.add_task(sleep_n_sec, [t])
    
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
    pool = ThreadPool(1)
    for i in range(5):
        pool.add_task(sleep_n_sec_print, [t])
        pool.cancel(i) 
    for i in range(1, 5):
        assert pool.check_task_status(i) == Status.cancelled


@pytest.mark.parametrize("args",[[1,4], [1, "string"], [2, [1,2,3,4]]])
def test_thread_callback(args):
    pool = ThreadPool(1)
    id_0 = pool.add_task(sleep_n_sec_return, args)
    id_1 = pool.add_callback(id_0, worker_test_callback)
    assert id_1 == id_0 + 1
    assert args[1] == pool.get_task_result(id_1)

@pytest.mark.parametrize("nthreads, nsec", [(5, 3), (3, 4)] )
def test_count_tasks(nthreads, nsec):
    pool = ThreadPool(nthreads)
    for i in range( nthreads * 2):
        pool.add_task(sleep_n_sec, [nsec])
    assert pool.count_task_in_queue() == nthreads * 2 - pool.get_num_threads()
    assert pool.is_busy()
    time.sleep(nsec + 0.5)
    assert pool.count_task_in_queue() == 0
    assert not pool.is_busy()
    time.sleep(nsec + 1)
    assert pool.count_task_in_queue() == 0 
    assert not pool.is_busy()

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
    """ test add task after function runs the task in correct dependent order"""
    pool = ThreadPool(10)
    previous_id = []
    for i in range(4):
       previous_id.append(pool.add_task(previous_worker, [ (i + 1) * 5, f"worker {i}"]))
    logger.info(previous_id)
    
    for id in previous_id:
        logger.info(id)
        pool.add_task_after(id, callback_worker, [f"callback task {id}"])
        

def test_add_multi_task_after():
    """ test the thread's ability to add multiple sequential task 
    """
    pool = ThreadPool(5)
    ids = []
    for i in range(10):
        ids.append(pool.add_task(previous_worker, [(i + 1) * 2, f"woker {i}"]))
    for id in ids:
        for i in range(5):
            pool.add_task_after(id, callback_worker, [f"callback task id: {id} - {i}"])


TestQueue = Queue()
def callback_check_queue(id):
    """ Helper function for testing thread with a queue 
    Args:
        id: thread task id that will be logged 
    """
    logger.info(f"\u23F1 callback worker:{id}\n")
    assert id == TestQueue.get()

def test_callback_with_queue():
    """ Test the sequence of the execution with a queue without manually looking
        over the log message 
    """
    pool = ThreadPool(5)
    ids = []
    for i in range(5):
        newid = pool.add_task(previous_worker, [(i + 1) * 2, f"worker {i}"])
        ids.append(newid)
        TestQueue.put(newid)
    
    for id in ids:
        pool.add_task_after(id, callback_check_queue, [id])
        
    ids = []
    for i in range(5):
        newid = pool.add_task(previous_worker, [(i + 1) * 2, i])
        ids.append(newid)
        TestQueue.put(newid)
    
    for id in ids:
        pool.add_callback(id, callback_check_queue)


def test_multiple_callback_with_queue():
    """ Test the sequential execution of multiple callback with a queue 
        without manually looking over the log message 
    """
    pool = ThreadPool(5)
    ids = []
    for i in range(5):
        newid = pool.add_task(previous_worker, [(i + 1) * 2, i])
        ids.append(newid)
        TestQueue.put(newid)
    assert ids == [j for j in range(5)]
    logger.info(ids)
    for i in range(5):
       newid =pool.add_task_after(i, callback_check_queue, [i])
       ids.append(newid)
       TestQueue.put(newid)
    assert ids == [j for j in range(10)]
    
    for i in range(5, 10):
       newid =pool.add_task_after(i, callback_check_queue, [i])
       ids.append(newid)
       TestQueue.put(newid)
    assert ids == [j for j in range(15)]

def error_worker():
    time.sleep(4)
    logger.info("error worker")
    raise ThreadError

def error_handler():
    logger.info("error handler")
    logger.warn("an error detected")
    raise ThreadError

def test_error():
    """ test the thread's ability to handle error  """
    pool = ThreadPool(2)
    with pytest.raises(ThreadError):
        id = pool.add_task(error_worker, error_fun = error_handler)
        res = pool.get_task_result(id, error_fun = error_handler)
        id = pool.add_task_after(id, error_worker, error_fun = error_handler)
        pool.add_task_after(id, error_worker)
    assert pool.check_task_status(id) == Status.error
    

    
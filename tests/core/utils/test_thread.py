import pytest 
import time 
from gailbot.core.utils.threads import ThreadPool, Status, ThreadError
import logging
from queue import Queue 

class ThreadErrorHandleException(Exception):
    pass

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


######### worker function defined that will be run on thread for testing #####
def sleep_two_sec():
    """
    Instantiate a thread worker with no parameters.
    """
    time.sleep(2)
    logger.info("worker no param")

def sleep_n_sec(n: int):
    """
    Instantiate a thread worker with one parameter.
    """
    time.sleep(n)
    logger.info(f"worker: {n}")

def sleep_n_sec_print(n: int, s = "Default"):
    """
    Instantiate a thread worker with default parameters.
    """
    time.sleep(n)
    logger.info(str(n) + str(s))

def sleep_n_sec_return(n: int, result):
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
    logger.info(f"\u25B6 previous worker start:{name}\n")
    time.sleep(n)
    logger.info(f"\u23F9 previous worker finished:{name}\n")
    return name 

def callback_worker(name):
    """
    Instantiate a thread worker that prints the name of the callback worker.
    """
    print(f"callback worker:{name}")
    logger.info(f"\u23F1 callback worker:{name}\n")


TestQueue = Queue()   # helper data structure to test the thread callback function
def callback_check_queue(id):
    """ Helper function for testing thread with a queue 
    Args:
        id: thread task id that will be logged 
    """
    logger.info(f"\u23F1 callback worker:{id}\n")
    assert id == TestQueue.get()

def error_worker():
    """ 
    a thread worker that will throw an error  
    used for testing error handling 
    """
    time.sleep(4)
    logger.info("error worker")
    raise ThreadError

def error_handler():
    """ 
    a thread error handling function that log error message and raise 
    a ThreadErrorHandleException
    used for testing error handling 
    """
    logger.info("error handler")
    logger.warn("an error detected")
    raise ThreadErrorHandleException


@pytest.mark.parametrize("size", [1,2,3])
def test_construction(size):
    """
    Test the construction of a thread pool with various sizes and ensure 
    it can properly add tasks.
    """
    pool = ThreadPool(size)
    assert size == pool.get_num_threads()
    pool.add_task(sleep_two_sec)

@pytest.mark.parametrize("args, kwargs", [([1], {"s": "test"}), ([2], {"s": 123})] )
def test_with_arg(args, kwargs):
    """
    Test the addition of tasks with various parameters as arguments. 
    """
    pool = ThreadPool(2)
    pool.add_task(sleep_n_sec, args)
    pool.add_task(sleep_n_sec_print, args, kwargs)


@pytest.mark.parametrize("arg", ["string", 1 , [1, 2, 3, 4], (1, 2), {1: 2}])
def test_get_test_result(arg):
    """
    Test the correct result is returned from various tasks in the thread pool.
    """
    pool = ThreadPool(2)
    id = pool.add_task(sleep_n_sec_return, [1, arg])
    assert pool.get_task_result(id) == arg

@pytest.mark.parametrize("t",[2,3])
def test_thread_status(t):
    """
    Test the correct status is returned from various tasks in one thread.
    """
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
    """
    Test the correct status is returned from various tasks in the thread pool.
    """
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
    """
    Test that the status cancelled tasks are correctly updated.
    """
    pool = ThreadPool(1)
    for i in range(5):
        pool.add_task(sleep_n_sec_print, [t])
        pool.cancel(i) 
    for i in range(1, 5):
        assert pool.check_task_status(i) == Status.cancelled


@pytest.mark.parametrize("args",[[1,4], [1, "string"], [2, [1,2,3,4]]])
def test_thread_callback(args):
    """
    Tests the callback function is correctly called for a pool of 1 thread.
    """
    pool = ThreadPool(1)
    id_0 = pool.add_task(sleep_n_sec_return, args)
    id_1 = pool.add_callback_with_arg(id_0, worker_test_callback)
    assert id_1 == id_0 + 1
    assert args[1] == pool.get_task_result(id_1)

@pytest.mark.parametrize("nthreads, nsec", [(5, 3), (3, 4)] )
def test_count_tasks(nthreads, nsec):
    """ 
    Test the count waiting task function in threadpool 
    """
    pool = ThreadPool(nthreads)
    for i in range( nthreads * 2):
        pool.add_task(sleep_n_sec, [nsec])
    assert pool.count_waiting_tasks() == nthreads * 2 - pool.get_num_threads()
    assert pool.is_busy()
    time.sleep(nsec + 0.5)
    assert pool.count_waiting_tasks() == 0
    assert not pool.is_busy()
    time.sleep(nsec + 1)
    assert pool.count_waiting_tasks() == 0 
    assert not pool.is_busy()

@pytest.mark.parametrize("args",[[1,4], [1, "string"], [2, [1,2,3,4]]])
def test_mult_thread_callback(args):
    """
    Tests the callback function is correctly called for a pool of 10 threads.
    """
    pool = ThreadPool(10)
    id_0 = pool.add_task(sleep_n_sec_return, args)
    id_1 = pool.add_callback_with_arg(id_0, worker_test_callback)
    assert id_1 == id_0 + 1
    assert args[1] == pool.get_task_result(id_1)
    assert pool.get_num_threads() == 10


def test_add_task_after():
    """ 
    Test add_task_after function runs the task in correct dependent order
    """
    pool = ThreadPool(10)
    previous_id = []
    for i in range(4):
       previous_id.append(pool.add_task(previous_worker, [ (i + 1) * 5, f"worker {i}"]))
    logger.info(previous_id)
    
    for id in previous_id:
        logger.info(id)
        pool.add_task_after(id, callback_worker, [f"callback task {id}"])
        

def test_add_multi_task_after():
    """ 
    Test the thread's ability to add multiple sequential task 
    """
    pool = ThreadPool(5)
    ids = []
    for i in range(10):
        ids.append(pool.add_task(previous_worker, [(i + 1) * 2, f"woker {i}"]))
    for id in ids:
        for i in range(5):
            pool.add_task_after(id, callback_worker, [f"callback task id: {id} - {i}"])


def test_callback_with_queue():
    """ 
    Test the sequence of the execution with a queue
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
        pool.add_callback_with_arg(id, callback_check_queue)


def test_multiple_callback_with_queue():
    """ 
    Test the sequential execution of multiple callback with a queue 
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


def test_error():
    """ 
    Test the thread's ability to handle errors
    """
    pool = ThreadPool(2)
    with pytest.raises(ThreadErrorHandleException):
        id = pool.add_task(error_worker, error_fun = error_handler)
        res = pool.get_task_result(id, error_fun = error_handler)
        id = pool.add_task_after(id, error_worker, error_fun = error_handler)
    with pytest.raises(ThreadError):
        pool.add_task_after(id, error_worker)
    assert pool.check_task_status(id) == Status.error
    

    
import pytest 
import time 
from gailbot.core.utils.threads import ThreadPool

def worker_no_param():
    time.sleep(1)
    print("worker no param")

def worker_one_param(n: int):
    time.sleep(n)
    print(f"worker with one param: {n}")

def worker_key_param(n: int, arg = "Default"):
    time.sleep(n)
    print(str(n) + arg)

def worker_with_return(n: int, result):
    time.sleep(n)
    return result

@pytest.mark.parametrize("size", [1,2,3])
def _test_construction(size):
    pool = ThreadPool(size)
    assert size == pool.get_num_threads()
    pool.add_task(worker_no_param)
    pool.add_task(worker_one_param, [2])
    pool.add_task(worker_key_param, [2], {"string": "hello"})


@pytest.mark.parametrize("arg", ["string", 1 , [1, 2, 3, 4], (1, 2), {1: 2}])
def test_fun_with_return(arg):
    pool = ThreadPool(2)
    id = pool.add_task(worker_with_return, [1, arg])
    assert pool.get_task_result(id) == arg



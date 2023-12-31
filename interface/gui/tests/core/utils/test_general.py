'''
File: test_general.py
Project: GailBot GUI
File Created: Saturday, 21st January 2023 11:01:59 am
Author: Siara Small  & Vivian Li
-----
Last Modified: Wednesday, 25th January 2023 6:47:38 am
Modified By:  Siara Small  & Vivian Li
-----
'''
from concurrent.futures import ThreadPoolExecutor
from gailbot.core.utils.threads import ThreadPool
from concurrent.futures import Future
import pytest
import os 
import shutil
from gailbot.core.utils import general 
import time
import logging

def create_test_dictionary() -> dict:
    test_dict = dict()
    for i in range(10):
        test_dict[str(i)] = str(i)
    return test_dict

def test_is_directory():
    dir = os.getcwd()
    assert general.is_directory(dir)
    assert not general.is_directory(f"{dir}/not_a_directory")


def test_isFile():
    file = __file__
    assert general.is_file(file)
    assert not general.is_file(f"{file}/not")

@pytest.fixture
def file_dir_path():
    file_dir_path = f"{os.getcwd()}/test_num_file"
    os.mkdir(file_dir_path)
    for i in range(5):
        open(f"{file_dir_path}/file{i}.txt", "w+")
    yield file_dir_path
    shutil.rmtree(f"{file_dir_path}")
    
@pytest.fixture 
def root_dir_path():
    root_dir_path = f"{os.getcwd()}/test_num_dir"
    os.mkdir(root_dir_path)
    for i in range(10):
        os.mkdir(f"{root_dir_path}/dir{i}")
    yield root_dir_path
    shutil.rmtree(root_dir_path)
    
def test_num_items_in_dir(file_dir_path):
    assert general.is_directory(file_dir_path)
    assert general.num_items_in_dir(f'{file_dir_path}', ["*"]) == 5
    
def test_paths_in_dir(file_dir_path):
    file_list = general.paths_in_dir(file_dir_path, ["*"])
    test_res = []
    for i in range(5):
        test_res.append(f"{file_dir_path}/file{i}.txt")
    test_res = set(test_res)
        
    for file in file_list:
        assert file in test_res

def test_num_subdirs(root_dir_path):
    assert general.num_subdirs(root_dir_path, ["*"]) == 10


""" NOTE: the returned file name does not contain the extension """
def test_get_name():
    assert general.get_name(os.getcwd()) == "GailBot"
    assert general.get_name(__file__) == "test_general"

def test_get_extension():
    assert general.get_extension(__file__) == "py"

def test_get_parent_path():
    assert general.get_parent_path(__file__) == f"{os.getcwd()}/tests/core/utils"
    
def test_get_size():
    basedir = f"{os.getcwd()}/test_file_size"
    os.mkdir(basedir)
    size_sum = 0 
    for i in range(5):
        new_file = f"{basedir}/test{i}.txt"
        with open(new_file, "w+") as f:
            f.write("test" * i)
        f.close()
        assert general.get_size(new_file) == os.path.getsize(new_file)
        size_sum += os.path.getsize(new_file)
    assert general.get_size(basedir) == size_sum
    shutil.rmtree(basedir)

def test_move():
    src_dir  = os.getcwd()
    src_file = f"{src_dir}/test.txt"
    open(src_file, "w+")
    des_dir = f"{src_dir}/des"
    os.mkdir(des_dir)
    general.move(src_file, des_dir)
    assert general.is_file(f"{des_dir}/test.txt")
    assert not general.is_file(src_file) 
    shutil.rmtree(des_dir)

def test_copy():
    basedir = os.getcwd()
    src_dir = f"{basedir}/src"
    des_dir = f"{basedir}/des_dir"
    os.mkdir(src_dir)
    os.mkdir(des_dir)
    for i in range(5):
        open(f"{src_dir}/test{i}.txt", "w+")

    general.copy(src_dir, des_dir)
    
    for i in range(5):
        assert general.is_file(f"{src_dir}/test{i}.txt")
        assert general.is_file(f"{des_dir}/test{i}.txt") 
    shutil.rmtree(des_dir)
    shutil.rmtree(src_dir)
    
    
def test_rename():
    new_file = f"{os.getcwd()}/test.txt"
    open(new_file, "w+")
    general.rename(new_file, "new_file.txt")
    assert not general.is_file(new_file)
    assert general.is_file(f"{os.getcwd()}/new_file.txt")
    general.delete(f"{os.getcwd()}/new_file.txt")

def test_make_delete_file():
    new_file = f"{os.getcwd()}/test_file.txt"
    open(new_file, "w+")
    assert general.is_file(new_file)
    general.delete(new_file)
    assert not general.is_file(new_file)
    new_dir = f"{os.getcwd()}/test_dir"
    general.make_dir(new_dir)
    assert general.is_directory(new_dir)
    general.delete(new_dir)
    assert not general.is_directory(new_dir)

def test_read_write_json():
    test_dictionary = create_test_dictionary()
    filename = f"{os.getcwd()}/test.json"
    general.write_json(filename, test_dictionary)
    json_dictionary = general.read_json(filename)
    for key, value in json_dictionary.items():
        assert value == test_dictionary[key]
    assert len(json_dictionary) == len (test_dictionary)
    general.delete(filename)
    assert not general.is_file(filename)
    
def test_read_write_toml():
    test_dictionary = create_test_dictionary()
    filename = f"{os.getcwd()}/test.toml"
    general.write_toml(filename, test_dictionary)
    assert general.is_file(filename)
    toml_dictionary = general.read_toml(filename)
    for key, value in toml_dictionary.items():
        assert value == test_dictionary[key]
    assert len(toml_dictionary) == len(test_dictionary)
    general.delete(filename)
    assert not general.is_file(filename)
    

def test_read_write_yaml():
    test_dictionary = create_test_dictionary()
    filename = f"{os.getcwd()}/test.yaml"
    general.write_yaml(filename, test_dictionary)
    yaml_dictionary = general.read_yaml(filename)
    for key, value in yaml_dictionary.items():
        assert value == test_dictionary[key]
    assert len(yaml_dictionary) == len(test_dictionary)
    general.delete(filename)
    assert not general.is_file(filename)

def test_read_write_txt():
    test_str_list = []
    for i in range (10):
        test_str_list.append(str(i))
    filename = f"{os.getcwd()}/test.txt"
    general.write_txt(filename, test_str_list)
    text_str_list = general.read_txt(filename)
    assert len(text_str_list) == len(test_str_list)
    print(test_str_list)
    print(text_str_list)
    for s1, s2 in zip(test_str_list, text_str_list):
        assert s1 == s2
    general.delete(filename)
    assert not general.is_file(filename)


def test_run_cmd():
    pid = general.run_cmd(["ls"]) 
    status = general.get_cmd_status(pid)
    assert status == general.CMD_STATUS.RUNNING
    time.sleep(1)
    status = general.get_cmd_status(pid)
    assert status == general.CMD_STATUS.FINISHED
    

def test_csv():
    file_path = os.path.join(os.getcwd(), "data/text_file/test.csv")
    data = [{'name': 'John', 'age': 28, 'city': 'New York'},
        {'name': 'Jane', 'age': 35, 'city': 'San Francisco'},
        {'name': 'Bob', 'age': 42, 'city': 'Chicago'}]
    general.write_csv(file_path, data)
    result = general.read_csv(file_path)
    logging.info(result)


def test_yaml_threads():
    with ThreadPoolExecutor(max_workers=8) as executer:
        futures = []
        for _ in range (10):
            futures.append(executer.submit(test_yaml_thread))
        for f in futures:
            assert not f.exception()

        

def test_single_yaml():
    path = "/Users/yike/GailBot/Backend/gailbot_workspace/engine_source/whisper_workspace/cache/models/pyannote/models--pyannote--speaker-diarization/snapshots/2c6a571d14c3794623b098a065ff95fa22da7f25/config.yaml"
    logging.info(general.read_yaml(path))

def test_yaml_thread():
    path = "/Users/yike/GailBot/Backend/gailbot_workspace/engine_source/whisper_workspace/cache/models/pyannote/models--pyannote--speaker-diarization/snapshots/2c6a571d14c3794623b098a065ff95fa22da7f25/config.yaml"
    keys: list[int] = []
    with ThreadPool(max_workers=8) as executer:
        for _ in range(10):
            keys.append(executer.submit(general.read_yaml, [path]))
    for key in keys:
        logging.info(executer.get_task_result(key))
    return True

def test_yaml_gb_threads(): 
    keys: list[int] = []
    with ThreadPool(max_workers=8) as executer:
        for _ in range(10):
           keys.append(executer.add_task(test_yaml_thread))
    for key in keys:
        logging.info(executer.get_task_result(key))

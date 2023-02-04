
from gailbot.core.pipeline import (
    Pipeline, Component, ComponentResult, ComponentState 
)
import time 
from typing import Dict 
from gailbot.core.utils.logger import makelogger
from gailbot.core.utils.general import write_txt
import pytest 
import os 
from transformers import pipeline, set_seed


logger = makelogger("test_pipeline_vivian")

def hugging_face_test(length: int, outpath: str):
    print("test hugging face")
    generator = pipeline('text-generation', model='gpt2')
    set_seed(50)
    text = generator("this is a test for hugging face",
                     max_length=length, num_return_sequences=5)
    logger.info(outpath)
    logger.info(text)     

class TestHuggingFace(Component):
    def __init__(self, name:str, num_word: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name 
        self.num_word = num_word
    
    def __call__(
        self, 
        dependency_outputs: Dict[str, ComponentResult], 
        base_filename: str = "", 
        *args, **kwargs) -> ComponentState:
        logger.info(self.name)
        s = time.perf_counter()
        filename = base_filename + self.name
        print("file name -------------")
        print(filename)

        try:
          hugging_face_test(self.num_word, filename)
          e = time.perf_counter()
          return ComponentResult(
              state=ComponentState.SUCCESS,
              result=self.name,
              runtime= e - s, 
          )
        except Exception as e:
          logger.error(e)
          print(e)
          return ComponentResult(
              state=ComponentState.FAILED,
              result=self.name, 
              runtime= 0
          )
          
class TestComponent(Component):
    def __init__(self, name: str, sleeptime: int ):
        self.name = name 
        self.sleeptime = sleeptime
        
    def __call__(self, 
                 dependency_outputs: Dict[str, ComponentResult], 
                 *args, **kwargs) -> ComponentState:
        logger.info(self.name)
        time.sleep(self.sleeptime)
        return ComponentResult(
            state=ComponentState.SUCCESS, 
            result=self.name, 
            runtime=self.sleeptime
        )
    
    def __repr__(self):
        return f"Component {self.name}"

    @property
    def __name__(self):
        return self.name

class ErrorComponent(Component):
    """ error component that will raise an error  """
    def __init__(self, name: str, *args, **kwargs):
        self.name = name 
    
    def __call__(self, dependency_outputs: Dict[str, ComponentResult], *args, **kwargs) -> ComponentState:
        time.sleep(3)
        raise Exception("Component Execution Failed")
        
    @property
    def __name__(self):
        return self.name

def test_pipeline_has_cycle():
    """ test exception handling or circle in graph  """
    components = {
        str(i): TestComponent(i, 3 * i) for i in range(1,6)
    } 
    
    with pytest.raises(Exception) as e :
        pipe = Pipeline(
            dependency_map={
            "1" : ["2"],
            "2" : ["1"],
            "3" : ["1"],
            "4" : ["1"],
            "5" : ["1"]
            }, 
            components=components,
            num_threads=1,
        )
    
        pipe._generate_dependency_graph(pipe.dependency_map)
        graph = pipe.get_dependency_graph()
        logger.info(e)

def test_pipeline_sequence():
    """ test the sequential execution in dependency graph """
    components = {
        str(i): TestComponent(i, i) for i in range(1,11)
    } 
     
    pipe = Pipeline(
        dependency_map={
            "1": [],
            "2": ["1"],
            "3": ["2"],
            "4": ["3"],
            "5": ["4"],
            "6": ["5"],
            "7": ["6"],
            "8": ["7"],
            "9": ["8"],
            "10":["9"],
        },
        components=components,
        num_threads=10
    )   
    
    res = pipe({})
    logger.info(res)
    
def test_thread_performance():
    """  test up to 100 thread """
    components = {
        str(i): TestComponent(i, 5) for i in range( 1, 101)
    }
    pipe = Pipeline(
        dependency_map={ str(i) : [] for i in range(1,101)},
        components=components,
        num_threads=100
    )
    
    res = pipe({})
    for i in range(1, 101):
        assert res[str(i)] == ComponentState.SUCCESS
    
def test_pipeline_fail():
    """ test when one node fail in the pipeline 
    """
    components = {
        str(i): TestComponent(i, 1) 
                if i != 4
                else ErrorComponent(i) 
                for i in range(1,17)
    }
    
    pipe = Pipeline(
        dependency_map={
            "1": [], 
            "2": ["1"],
            "3": ["1"],
            "4": ["1"],
            "5": ["2", "1"],
            "6": [],
            "7": ["2", "5", "6"],
            "8": ["7", "6"],
            "9": ["2", "7", "8"],
            "10":["1", "4"],
            "11":["4", "1"],
            "12":["10","2"],
            "13":["10"],
            "14":["13"],
            "15":["14"],
            "16":["15"]
        },
        components=components,
        num_threads=3
    )
    
    res = pipe({})
    
    for i in range(1, 10):
        if i != 4:
            assert(res[str(i)] == ComponentState.SUCCESS) 
        else:
            assert(res[str(i)]) == ComponentState.FAILED
    
    for i in range(10, 16):
        assert(res[str(i)] == ComponentState.FAILED)
    logger.info(res)  
    
def test_complex_dependency():
    components = {
        str(i): TestComponent(str(i), 1) for i in range(1,17)
    }
    
    pipe = Pipeline(
        dependency_map={
            "2" : [],
            "4" : [],
            "6" : [],
            "3" : ["2", "4"],
            "15": ["3"],
            "1" : ["2","3", "4"],
            "5" : ["1", "2"],
            "7" : ["2", "5", "6"],
            "8" : ["7", "6"],
            "9" : ["2", "7", "8"],
            "10": ["1", "4"],
            "11": ["4", "1", "8"],
            "12": ["10","2", "7", "3"],
            "13": ["10", "12", "11", "9", "8", "7", "6"],
            "14": ["13"],
            "16": ["15"]
        }, 
        components=components,
        num_threads=3
    )
    
    res = pipe({})
    logger.info(res)
    for i in range(1, 17):
        assert(res[str(i)] == ComponentState.SUCCESS) 
    
def test_hugging_face():
    basedir = os.path.join(os.getcwd(), "data/h_face_output")
    os.makedirs(basedir, exist_ok=True)
    TEXT_LENTH = 200 
    components = {
        str(i) : TestHuggingFace(str(i), TEXT_LENTH) for i in range (1, 11)
    }
    pipe = Pipeline(
                dependency_map={
                    "1" : ["2"],
                    "2" : [],
                    "3" : ["2"],
                    "4" : ["2"],
                    "5" : ["1"],
                    "6" : [],
                    "7" : ["2"],
                    "8" : ["2"],
                    "9" : ["2"],
                    "10": ["1"]},
                components=components,
                num_threads=10
    )
    
    base = os.path.join(basedir, f"gpt2_outout")
    res = pipe(additional_component_kwargs={"base_filename": "hugging_face"})

def test_one_hugging_face():
    s = time.perf_counter()
    hugging_face_test(200, "one_hugging_face") 
    e = time.perf_counter()
    logger.info(f"time for one hugging face tes {e - s}")
    
def test_ten_hugging_face():
    s = time.perf_counter()
    
    components = {
        str(i): TestHuggingFace(str(i), 200) for i in range( 1, 11)
    }
    
    pipe = Pipeline(
        dependency_map={ str(i) : [] for i in range(1,11)},
        components=components,
        num_threads=10
    )
    
    res = pipe(additional_component_kwargs={"base_filename": "hugging_face"})
    e = time.perf_counter()
    logger.info(f"time for ten hugging face tes {e - s}")
    logger.info(res)
from gailbot.plugins.suite import PluginComponent, PluginSuite, ComponentResult, ComponentState
from gailbot.plugins.plugin import Plugin
from gailbot.services.pipeline.pluginMethods import GBPluginMethods, Methods
import pytest 
from typing import Dict, Any, List



test_plugin_method = GBPluginMethods()
SUCCESS_RESULT = ComponentResult(ComponentState.SUCCESS)
FAILURE_RESULT = ComponentResult(ComponentState.FAILED)


test_config = {
    "name": "test_suite",
    "path": "../../data/plugin/test",
    "plugins": [
       {
           "class_name": "test1",
           "dependencies": [],
           "module_name": "test_module"
       },  {
           "class_name": "test2",
           "dependencies": ["test1"],
           "module_name": "test_module"
       },  {
           "class_name": "test3",
           "dependencies": ["test2"],
           "module_name": "test_module"
       }, {
           "class_name": "test4",
           "dependencies": ["test3"],
           "module_name": "test_module"
       }, 
    ]
}

class TestPlugin(Plugin):
    def __init__(self) -> None:
        super().__init__()
        self.is_success = False 
        self.is_loaded = False 
        
    def apply(self, 
              dependency_outputs: Dict[str, Any], 
              methods: Methods, *args, **kwargs) -> Any:
        
        print("test plugin called ")  
        self.is_success = True

class TestFailurePlugin(Plugin):
    def __init__(self) -> None:
        super().__init__()
        self.is_success = False 
        self.is_loaded = False 
        
    def apply(self, 
              dependency_outputs: Dict[str, Any], 
              methods: Methods, *args, **kwargs) -> Any:
        try: 
            raise Exception 
        except Exception as e:
            self.is_success = False

    
def test_plugin_component():
    plugin = TestPlugin()
    plugin_com = PluginComponent(plugin)
    success_dep = {"success": SUCCESS_RESULT}
    plugin_com(success_dep)


def test_plugin_suit_construct():
    dict_conf = {
        "1": ["2", "3"],
        "2":[],
        "3": ["2"]
    }
    
    test_plugin_suite = PluginSuite(dict_conf)
    
    
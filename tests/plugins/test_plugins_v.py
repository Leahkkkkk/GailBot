from gailbot.plugins.suite import PluginComponent, PluginSuite, ComponentResult, ComponentState
from gailbot.plugins.plugin import Plugin
from gailbot.services.pipeline.pluginMethods import GBPluginMethods, Methods
import pytest 
from typing import Dict, Any, List
from gailbot.core.utils.logger import makelogger
from .plugin_data import hilab_plugin, test_config, TEST_PLUGIN_URL, HIL_LAB_PLUGIN_URL, TEST_TWO_DIR_SRC, Invalid
from gailbot.plugins.manager import PluginManager
from gailbot.configs import top_level_config_loader 
import pytest 
import os
import time

TOP_CONFIG = top_level_config_loader()
logger = makelogger("test_plugins")

TEST_CONFIG_SRC = "/Users/yike/Documents/GitHub/GailBot/data/test_suite/conf.toml"
TEST_DIR_SRC = "/Users/yike/Documents/GitHub/GailBot/data/test_suite"
HIL_CONFIG_SRC =  "/Users/yike/Documents/GitHub/GailBot/gb_hilab_suite/config.toml"
HIL_DIR_SRC = "/Users/yike/Documents/GitHub/GailBot/gb_hilab_suite"
PLUGIN_WORKSPACE = os.path.join( TOP_CONFIG.root, TOP_CONFIG.workspace.plugin_workspace)
test_plugin_method = GBPluginMethods()
SUCCESS_RESULT = ComponentResult(ComponentState.SUCCESS)
FAILURE_RESULT = ComponentResult(ComponentState.FAILED)

TEST_SUITE_NAME = "test_suite"
HIL_LAB_SUITE_NAME = "gb_hilab_suite"
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
            raise Exception("Plugin Error") 
        except Exception as e:
            self.is_success = False
            

class TestMethod(Methods):
    def __call__(self, msg: str, *args: Any, **kwds: Any) -> Any:
        # time.sleep(5)
        return True


class TestMethodError(Methods):
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        time.sleep(2)
        raise Exception("Plugin Method Error")
                
def test_plugin_component():
    plugin = TestPlugin()
    plugin_com = PluginComponent(plugin)
    success_dep = {"success": SUCCESS_RESULT}
    plugin_com(success_dep, test_plugin_method)

@pytest.mark.parametrize(
    "source", [[TEST_DIR_SRC, HIL_DIR_SRC, TEST_TWO_DIR_SRC]])
def test_load_dir(source):
    """ test to load plugin from the directory  """
    test_manager = PluginManager(
        plugin_sources =source,
        load_existing=False)
    logger.info(test_manager.suite_names)

    
@pytest.mark.parametrize("url", [[HIL_LAB_PLUGIN_URL, TEST_PLUGIN_URL]])
def test_load_url(url):
    """ load plugin from github url """
    test_manager = PluginManager(
        plugin_sources=url,
        load_existing=False)
    logger.info(test_manager.suite_names)


@pytest.mark.parametrize("source", [[TEST_DIR_SRC]])
def test_run_plugin(source):
    """  test running the plugin , which should return the result as 
         successful 
    """
    test = PluginManager(
        plugin_sources=source,
        load_existing=True
    )
    
    for suite_name in test.suite_names:
        test_method = TestMethod()
        suite = test.get_suite(suite_name)
        assert suite.is_ready
        result = suite([], test_method)
        logger.info(result)
        from gailbot.core.pipeline.component import ComponentState
        for res in result.values():
            assert res == ComponentState.SUCCESS


@pytest.mark.parametrize("source", [[TEST_DIR_SRC, HIL_DIR_SRC]])
def test_delete_suite(source):
    """ test function to delete the suite """
    test = PluginManager(
    plugin_sources=source,
    load_existing=False
    )
    logger.info(test.get_suite_path(TEST_SUITE_NAME))
    assert test.delete_suite(TEST_SUITE_NAME)
    assert(not test.is_suite(TEST_SUITE_NAME))
    logger.info(test.get_suite_path(HIL_LAB_SUITE_NAME)) 
    assert test.delete_suite(HIL_LAB_SUITE_NAME)
    assert(not test.is_suite(HIL_LAB_SUITE_NAME))


@pytest.mark.parametrize("source", [[Invalid.InvalidConf, Invalid.InvalidConf2, Invalid.InvalidConf3]])
def test_invalid_configuration(source):
    test = PluginManager(
        plugin_sources=source,
        load_existing=False,
        overwrite=True
    )
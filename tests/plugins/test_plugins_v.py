from gailbot.plugins.suite import PluginComponent, PluginSuite, ComponentResult, ComponentState
from gailbot.plugins.plugin import Plugin
from gailbot.services.pipeline.pluginMethods import GBPluginMethods, Methods
import pytest 
from typing import Dict, Any, List
from gailbot.core.utils.logger import makelogger
from .plugin_confs import hilab_plugin, test_config
from gailbot.plugins.manager import PluginManager
from gailbot.configs import top_level_config_loader 
import pytest 
import os

TOP_CONFIG = top_level_config_loader()
logger = makelogger("test_plugins")


test_plugin_method = GBPluginMethods()
SUCCESS_RESULT = ComponentResult(ComponentState.SUCCESS)
FAILURE_RESULT = ComponentResult(ComponentState.FAILED)


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
    plugin_com(success_dep, test_plugin_method)


@pytest.mark.parametrize("config", [hilab_plugin, test_config])    
def test_load_plugin(config):
    plugin_config = PluginSuite(config)    
    logger.info(plugin_config.dependency_map)
    logger.info(plugin_config.plugins)
    assert plugin_config._is_ready
    logger.info(plugin_config.name)
    logger.info(plugin_config.dependency_graph())
    for plugin in config["plugins"]:
        assert plugin_config.is_plugin(plugin["plugin_name"])
    logger.info(plugin_config.plugin_names())                 

TEST_CONFIG_SRC = "/Users/yike/Documents/GitHub/GailBot/data/test_suite/conf.toml"
TEST_DIR_SRC = "/Users/yike/Documents/GitHub/GailBot/data/test_suite"
HIL_CONFIG_SRC =  "/Users/yike/Documents/GitHub/GailBot/gb_hilab_suite/config.toml"
HIL_DIR_SRC = "/Users/yike/Documents/GitHub/GailBot/gb_hilab_suite"

@pytest.mark.parametrize("source", [[TEST_DIR_SRC, HIL_DIR_SRC]])
def test_load_config(source):
    test_manager = PluginManager(
        workspace_dir=os.path.join(TOP_CONFIG.root, TOP_CONFIG.workspace.plugin_workspace),
        plugin_sources =source,
        load_existing=True)
   
    with pytest.raises(Exception) as e :
        failed_manager = PluginManager(
        workspace_dir=os.path.join(TOP_CONFIG.root, TOP_CONFIG.workspace.plugin_workspace),
        plugin_sources=[TEST_CONFIG_SRC],
        load_existing=False
        )
        logger.info(e)
    

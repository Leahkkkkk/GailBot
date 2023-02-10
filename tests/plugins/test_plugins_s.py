from gailbot.plugins.manager import (
    PluginManager,
    PluginDictLoader,
    PluginDirectoryLoader,
    PluginURLLoader,
    PluginTOMLLoader,
)
from .plugin_confs import hilab_plugin 
from .plugin_confs import test_config
from .test_plugins_v import TestPlugin
from gailbot.configs import top_level_config_loader 
import pytest 

TOP_CONFIG = top_level_config_loader()
import os 
# test_manager = PluginManager(workspace_dir="/Users/yike/Documents/GitHub/GailBot",
#                             plugin_sources=hilab_plugin,
#                             load_existing=False) #TODO: fix error in manager.py that occurs when load existing = true




# class TestManager(PluginManager):
def __init__():
    test_sources = { }
    # test_suite = PluginSuite(dict_conf = dependency_map)
    # test_manager = PluginManager(plugin_sources=[])
    # test_manager.suites = test_suite

def test_suite_names(self):
    # plugin1 = TestPlugin()
    # plugin2 = TestPlugin()
    # plugin3 = TestPlugin()
    # test_manager.suites = {plugin1, plugin2, plugin3}
    # assert(test_manager.suite_names == [plugin1.self.name, plugin2.self.name, plugin3.self.name])
    pass

def test_reset_workspace(self):
    pass

def test_register_suite():
    ## relies on load conf
    #TODO test loaders first
    # manager = TestManager()
    pass
    
def test_dict_loader():
    # implicitly tests get_suite and is_suite
    loader = PluginDictLoader()
    suite = loader.load(hilab_plugin)
    manager = PluginManager(plugin_sources=[suite], workspace_dir= os.path.join(TOP_CONFIG.root, "plugin"))
    assert(manager.is_suite(manager, "hil_lab"))
    test_suite = manager.get_suite("hil_lab")
    assert(test_suite.name == "hil_lab")
    # assert("hil_lab" in manager.suite_names())

def test_url_loader():
    ##TODO complete this test later when we have a URL for the hilab suite
    pass

def dont_test_toml_loader():
    loader = PluginTOMLLoader()
    suite = loader.load()

def dont_test_directory_loader():
    # TODO need test plugins within directory
    loader = PluginDirectoryLoader()



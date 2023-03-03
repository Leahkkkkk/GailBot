from gailbot.plugins.manager import (
    PluginManager,
    PluginDirectoryLoader,
    PluginURLLoader,
)
from .plugin_data import hilab_plugin 
from .plugin_data import test_config
from .test_plugins_v import TestPlugin

import os 

def test_suite_names(self):
    pass

def test_reset_workspace(self):
    pass

def test_register_suite():
    pass
    
    # implicitly tests get_suite and is_suite
    manager = PluginManager(plugin_sources=[suite], workspace_dir= os.path.join(TOP_CONFIG.root, "plugin"))
    assert(manager.is_suite(manager, "hil_lab"))
    test_suite = manager.get_suite("hil_lab")
    assert(test_suite.name == "hil_lab")
    # assert("hil_lab" in manager.suite_names()




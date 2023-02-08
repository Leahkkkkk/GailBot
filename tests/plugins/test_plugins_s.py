from gailbot.plugins import (
    PluginManager,
    PluginSuite,
    Plugin,
    Methods
)

test_manager = PluginManager()

class TestManager(PluginManager):
    def __init__():
        test_sources = { }
        # test_suite = PluginSuite(dict_conf = dependency_map)
        # test_manager = PluginManager(plugin_sources=[])
        # test_manager.suites = test_suite

    def test_loaders(self):
        pass

    def test_suite_names(self):
        test_manager.suites = {"test1": 1, "test2":2, "test3":3, "test4":4, "test5": 5}
        assert(test_manager.suite_names == ["test1", "test2", "test3", "test4", "test5"])

    def test_is_suite():
        test_manager.suites = dict()
        assert(not test_manager.is_suite(test_manager, "test"))
        test_manager.suites = {"test":1}
        assert(test_manager.is_suite(test_manager, "test"))


    def test_reset_workspace(self):
        pass

    def test_register_suite():
        ## relies on load conf
        pass

    def test_get_suite():
        pass


        

    
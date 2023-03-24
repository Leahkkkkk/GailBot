from gb_hilab_suite.src.core.word_tree import WordTreePlugin
from gailbot.plugins import GBPluginMethods

GBPlugin = GBPluginMethods()

def test_word_tree():
    plg = WordTreePlugin()
    res = plg.apply_plugin({}, GBPlugin)
    print(res)

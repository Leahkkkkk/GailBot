from gb_hilab_suite.src.core.word_tree import WordTreePlugin
from gailbot.plugins import GBPluginMethods

GBPlugin = GBPluginMethods()

def test_word_tree():
    plg = WordTreePlugin()
    res = plg.apply({}, GBPlugin)
    print(res)
    assert plg._getIntLabel("1") == 1
    assert plg._getIntLabel("SPEAKER_01") == 1

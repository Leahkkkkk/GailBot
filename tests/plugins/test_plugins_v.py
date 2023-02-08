from gailbot.plugins.suite import PluginComponent, PluginSuite, ComponentResult, ComponentState
from gailbot.plugins.plugin import Plugin
from gailbot.services.pipeline.pluginMethods import GBPluginMethods, Methods
import pytest 
from typing import Dict, Any, List
from gailbot.core.utils.logger import makelogger

logger = makelogger("test plugins")


test_plugin_method = GBPluginMethods()
SUCCESS_RESULT = ComponentResult(ComponentState.SUCCESS)
FAILURE_RESULT = ComponentResult(ComponentState.FAILED)


test_config = {
    "suite_name": "test_suite",
    "suite_abs_path": "/Users/yike/Documents/GitHub/GailBot/data",
    "plugins": [ {
           "plugin_name": "test1",
           "dependencies": [],
           "module_name": "test_module",
           "rel_path":"test_suite/test_module.py"
            },  {
           "plugin_name": "test2",
           "dependencies": ["test1"],
           "module_name": "test_module",
           "rel_path":"test_suite/test_module.py"

       },  {
           "plugin_name": "test3",
           "dependencies": ["test2"],
            "rel_path":"test_suite/test_module.py",
            "module_name": "test_module"
       }, {
           "plugin_name": "test4",
           "dependencies": ["test3"],
           "rel_path":"test_suite/test_module.py",
           "module_name": "test_module"
       }, 
    ]
}

hilab_plugin = {
    "suite_name": "hil_lab",
    "suite_abs_path": "/Users/yike/Documents/GitHub/GailBot/gb_hilab_suite",
    "plugins" : [
    {
      "plugin_name": "WordTreePlugin",
      "dependencies": [],
      "rel_path": "src/core/word_tree.py",
      "module_name": "word_tree",
    },
    {
      "dependencies": [
        "WordTreePlugin"
      ],
      "rel_path": "src/core/utterance_map.py",
      "module_name": "utterance_map",
      "plugin_name": "UtteranceMapPlugin"
    },
    {
      "dependencies": [
        "UtteranceMapPlugin"
      ],
      "rel_path": "src/core/speaker_map.py",
      "module_name": "speaker_map",
      "plugin_name": "SpeakerMapPlugin"
    },
    {
      "dependencies": [
        "SpeakerMapPlugin"
      ],
      "rel_path": "src/core/conversation_map.py",
      "module_name": "conversation_map",
      "plugin_name": "ConversationMapPlugin"
    },
    {
      "dependencies": [
        "WordTreePlugin",
        "UtteranceMapPlugin",
        "SpeakerMapPlugin",
        "ConversationMapPlugin"
      ],
      "rel_path": "src/core/conversation_model.py",
      "module_name": "conv_model",
      "plugin_name": "ConversationModelPlugin"
    },
    {
      "dependencies": [
        "ConversationModelPlugin"
      ],
      "rel_path": "src/analysis/overlaps.py",
      "module_name": "overlaps",
      "plugin_name": "OverlapPlugin"
    },
    {
      "dependencies": [
        "ConversationModelPlugin"
      ],
      "rel_path": "src/analysis/pauses.py",
      "module_name": "pauses",
      "plugin_name": "PausePlugin"
    },
    {
      "dependencies": [
        "ConversationModelPlugin"
      ],
      "rel_path": "src/analysis/gaps.py",
      "module_name": "gaps",
      "plugin_name": "GapPlugin"
    },
    {
      "dependencies": [
        "ConversationModelPlugin"
      ],
      "rel_path": "src/analysis/syllable_rate.py",
      "module_name": "syllable_rate",
      "plugin_name": "SyllableRatePlugin"
    },
    {
      "dependencies": [
        "ConversationModelPlugin",
        "GapPlugin",
        "PausePlugin",
        "OverlapPlugin"
      ],
      "rel_path": "src/format/chat.py",
      "module_name": "chat",
      "plugin_name": "ChatPlugin"
    },
    {
      "dependencies": [
        "ConversationModelPlugin",
        "GapPlugin",
        "PausePlugin",
        "OverlapPlugin"
      ],
      "rel_path": "src/format/text.py",
      "module_name": "text",
      "plugin_name": "TextPlugin"
    },
    {
      "dependencies": [
        "ConversationModelPlugin",
        "GapPlugin",
        "PausePlugin",
        "OverlapPlugin"
      ],
      "rel_path": "src/format/csv.py",
      "module_name": "csv",
      "plugin_name": "CSVPlugin"
    },
    {
      "dependencies": [
        "ConversationModelPlugin",
        "GapPlugin",
        "PausePlugin",
        "OverlapPlugin"
      ],
      "rel_path": "src/format/xml.py",
      "module_name": "xml",
      "plugin_name": "XMLPlugin"
    }
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
    plugin_com(success_dep, test_plugin_method)


def test_plugin_suite_construct():
    test_plugin_suite = PluginSuite(test_config)
    
def test_loading_hillab():
    hilab_plugin_suite = PluginSuite(hilab_plugin)    
    logger.info(hilab_plugin_suite.dependency_map)
    logger.info(hilab_plugin_suite.plugins)
    assert hilab_plugin_suite._is_ready
    logger.info(hilab_plugin_suite.name)
    logger.info(hilab_plugin_suite.dependency_graph())
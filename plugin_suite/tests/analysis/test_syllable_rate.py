import logging 
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


from gailbot.plugins import GBPluginMethods
from gb_hilab_suite.src.core.word_tree import WordTreePlugin
from gb_hilab_suite.src.core.utterance_map import UtteranceMapPlugin
from gb_hilab_suite.src.core.speaker_map import SpeakerMapPlugin
from gb_hilab_suite.src.core.conversation_map import ConversationMapPlugin
from gb_hilab_suite.src.core.nodes import Node
from gb_hilab_suite.src.core.conversation_model import ConversationModelPlugin, ConversationModel

from gb_hilab_suite.src.analysis.syllable_rate import SyllableRatePlugin
from gb_hilab_suite.src.format.chat import ChatPlugin
from gb_hilab_suite.src.format.text import TextPlugin
from gb_hilab_suite.src.format.csv import CSVPlugin
from gb_hilab_suite.src.format.xml import XMLPlugin
from .test_fun import analysis_test
from typing import Dict, Union, Any, List, TypedDict
from pydantic import BaseModel 
SYLLABLE_RATE_OUT_PATH = "/Users/yike/Desktop/plugin_output/syllable_rate"

def test_syllable_rate():
    fast_utt             = [{"start": i, "end": i + 0.99, "speaker": 1, "text": f"word{i}"} for i in range(0,20,1)]
    slow_utt             = [{"start": i, "end": i + 0.20, "speaker": 1, "text": f"word{i}"} for i in range(20, 40, 1)]
    normal_utt           = [{"start": i, "end": i + 0.50, "speaker": 1, "text": f"word{i}"} for i in range(40, 60, 1)]
    syllable_rate_data   = {"test": fast_utt + slow_utt + normal_utt}
    plugin = SyllableRatePlugin()
    analysis_test(syllable_rate_data, plugin, SYLLABLE_RATE_OUT_PATH)
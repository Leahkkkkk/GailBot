import logging 
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

from .test_fun import analysis_test
from gailbot.plugins import GBPluginMethods
from gb_hilab_suite.src.core.word_tree import WordTreePlugin
from gb_hilab_suite.src.core.utterance_map import UtteranceMapPlugin
from gb_hilab_suite.src.core.speaker_map import SpeakerMapPlugin
from gb_hilab_suite.src.core.conversation_map import ConversationMapPlugin
from gb_hilab_suite.src.core.nodes import Node
from gb_hilab_suite.src.core.conversation_model import ConversationModelPlugin, ConversationModel

from gb_hilab_suite.src.analysis.pauses import PausePlugin
from gb_hilab_suite.src.analysis.syllable_rate import SyllableRatePlugin
from gb_hilab_suite.src.format.chat import ChatPlugin
from gb_hilab_suite.src.format.text import TextPlugin
from gb_hilab_suite.src.format.csv import CSVPlugin
from gb_hilab_suite.src.format.xml import XMLPlugin
from typing import Dict, Union, Any, List, TypedDict
from pydantic import BaseModel 
PAUSE_OUT_PATH = "/Users/yike/Desktop/plugin_output/pauses"


def test_pauses():
    lartch       = [{"start": i, "end": i + 0.99, "speaker": 1, "text": f"word{i}"} for i in range(0,20,1)]
    micro_pause  = [{"start": i, "end": i + 0.40, "speaker": 1, "text": f"word{i}"} for i in range(20, 40, 1)]
    long_pause   = [{"start": i, "end": i + 0.10, "speaker": 1, "text": f"word{i}"} for i in range(40, 60, 2)]
    medium_pause = [{"start": i, "end": i + 1.4, "speaker": 1, "text": f"word{i}"} for i in range(60, 80, 2)]
    pause_data   = {"test": lartch + micro_pause + long_pause + medium_pause}
    pause_plugin = PausePlugin()
    analysis_test(pause_data, pause_plugin, PAUSE_OUT_PATH)
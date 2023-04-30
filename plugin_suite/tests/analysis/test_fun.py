import logging 
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


from gailbot.plugins import GBPluginMethods, Plugin
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
from typing import Dict, Union, Any, List, TypedDict
from pydantic import BaseModel 
SYLLABLE_RATE_OUT_PATH = "/Users/yike/Desktop/plugin_output/syllable_rate"

def analysis_test(data, plugin: Plugin, output):
    GBPlugin =  GBPluginMethods(data, output_path=output)
    word_tree = WordTreePlugin()
    word_res = word_tree.apply({}, GBPlugin)
    assert type(word_res) == Node
    
    utt_map = UtteranceMapPlugin()
    utt_res = utt_map.apply({"WordTreePlugin": word_res}, GBPlugin)
    assert type(utt_res) == dict
    
    speaker_map = SpeakerMapPlugin()
    speaker_res = speaker_map.apply({"UtteranceMapPlugin": utt_res}, GBPlugin)
    assert type(speaker_res) == dict
    for key, d in speaker_res.items():
        assert type(d) == dict
        for k, l in d.items():
            assert type(l) == list
            for i in l:
                assert type(l) == list
    
    conv_map = ConversationMapPlugin()
    conv_map_res = conv_map.apply({}, GBPlugin)
    assert type(conv_map_res) == dict
    
    conv_model = ConversationModelPlugin()
    conv_model_res = conv_model.apply(dependency_outputs=
                                             {"UtteranceMapPlugin": utt_res,
                                              "SpeakerMapPlugin": speaker_res,
                                              "ConversationMapPlugin": conv_map_res,
                                              "WordTreePlugin": word_res},
                                            methods = GBPlugin)
    
    assert type(conv_model_res) == ConversationModel
    res = plugin.apply({"ConversationModelPlugin":conv_model_res},GBPlugin)
    logger.info(res)

    chat = ChatPlugin()
    chat.apply({"ConversationModelPlugin": conv_model_res}, GBPlugin)
    
    text = TextPlugin()
    text.apply({"ConversationModelPlugin": conv_model_res}, GBPlugin)
    
    csv = CSVPlugin()
    csv.apply({"ConversationModelPlugin": conv_model_res}, GBPlugin)
    
    
    xml = XMLPlugin()
    xml.apply({"ConversationModelPlugin": conv_model_res},GBPlugin) 



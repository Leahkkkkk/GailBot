from gailbot.plugins import GBPluginMethods
from gb_hilab_suite.src.core.word_tree import WordTreePlugin
from gb_hilab_suite.src.core.utterance_map import UtteranceMapPlugin
from gb_hilab_suite.src.core.speaker_map import SpeakerMapPlugin
from gb_hilab_suite.src.core.conversation_map import ConversationMapPlugin
from gb_hilab_suite.src.core.nodes import Node
from gb_hilab_suite.src.core.conversation_model import ConversationModelPlugin, ConversationModel

from gb_hilab_suite.src.analysis.overlaps import OverlapPlugin
from gb_hilab_suite.src.analysis.pauses import PausePlugin
from gb_hilab_suite.src.analysis.gaps import GapPlugin
from gb_hilab_suite.src.analysis.syllable_rate import SyllableRatePlugin

from gb_hilab_suite.src.format.chat import ChatPlugin
from gb_hilab_suite.src.format.text import TextPlugin
from gb_hilab_suite.src.format.csv import CSVPlugin
from gb_hilab_suite.src.format.xml import XMLPlugin
GBPlugin = GBPluginMethods()

def test_analysis():

    word_tree = WordTreePlugin()
    word_res = word_tree.apply_plugin({}, GBPlugin)
    assert type(word_res) == Node
    
    utt_map = UtteranceMapPlugin()
    utt_res = utt_map.apply_plugin({"WordTreePlugin": word_res}, GBPlugin)
    assert type(utt_res) == dict
    
    speaker_map = SpeakerMapPlugin()
    speaker_res = speaker_map.apply_plugin({"UtteranceMapPlugin": utt_res}, GBPlugin)
    assert type(speaker_res) == dict
    for key, d in speaker_res.items():
        assert type(d) == dict
        for k, l in d.items():
            assert type(l) == list
            for i in l:
                assert type(l) == list
    
    conv_map = ConversationMapPlugin()
    conv_map_res = conv_map.apply_plugin({}, GBPlugin)
    assert type(conv_map_res) == dict
    
    conv_model = ConversationModelPlugin()
    conv_model_res = conv_model.apply_plugin(dependency_outputs=
                                             {"UtteranceMapPlugin": utt_res,
                                              "SpeakerMapPlugin": speaker_res,
                                              "ConversationMapPlugin": conv_map_res,
                                              "WordTreePlugin": word_res},
                                            plugin_input = GBPlugin)
    
    assert type(conv_model_res) == ConversationModel
                
    
    overlap = OverlapPlugin()
    overlap_res = overlap.apply_plugin({"ConversationModelPlugin": conv_model_res},
                                       GBPlugin)
    assert type(overlap_res) == ConversationModel
    
    pause = PausePlugin()
    pause_res = pause.apply_plugin({"ConversationModelPlugin": overlap_res},
                                   GBPlugin)
    assert type(pause_res) == ConversationModel
    
    gap = GapPlugin()
    gap_res = gap.apply_plugin({"ConversationModelPlugin":pause_res},
                               GBPlugin)
    assert type(gap_res) == ConversationModel
    
    syllable = SyllableRatePlugin()
    syllable_res = syllable.apply_plugin({"ConversationModelPlugin":gap_res},
                               GBPlugin)
    assert type(syllable_res) == ConversationModel

    chat = ChatPlugin()
    chat.apply_plugin({"ConversationModelPlugin": syllable_res},
                      GBPlugin)
    
    text = TextPlugin()
    text.apply_plugin({"ConversationModelPlugin": syllable_res},
                      GBPlugin)
    
    csv = CSVPlugin()
    csv.apply_plugin({"ConversationModelPlugin": syllable_res},
                      GBPlugin)
    
    
    xml = XMLPlugin()
    xml.apply_plugin({"ConversationModelPlugin": syllable_res},
                      GBPlugin)
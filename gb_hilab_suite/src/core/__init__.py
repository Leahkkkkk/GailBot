# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-08-24 08:31:04
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-24 11:49:47


from typing import List, Dict

from gb_hilab_suite.src.core.nodes import Word, Node

def get_dependencies() -> List[Dict]:
    return [
        {
        "plugin_name": "word_tree",
        "plugin_dependencies": [],
        "plugin_file_path": "core/word_tree.py",
        "plugin_source_name": "word_tree",
        "plugin_class_name": "WordTreePlugin"
        },
        {
        "plugin_name": "utterance_map",
        "plugin_dependencies": ["word_tree"],
        "plugin_file_path": "core/utterance_map.py",
        "plugin_source_name": "utterance_map",
        "plugin_class_name": "UtteranceMapPlugin"
        },
        {
        "plugin_name": "speaker_map",
        "plugin_dependencies": ["utterance_map"],
        "plugin_file_path": "core/speaker_map.py",
        "plugin_source_name": "speaker_map",
        "plugin_class_name": "SpeakerMapPlugin"
        },
        {
        "plugin_name": "conversation_map",
        "plugin_dependencies": ["speaker_map"],
        "plugin_file_path": "core/conversation_map.py",
        "plugin_source_name": "conversation_map",
        "plugin_class_name": "ConversationMapPlugin"
        },
        {
        "plugin_name": "conv_model",
        "plugin_dependencies": [
            "word_tree",
            "utterance_map",
            "speaker_map",
            "conversation_map"
        ],
        "plugin_file_path": "core/conversation_model.py",
        "plugin_source_name": "conv_model",
        "plugin_class_name": "ConversationModelPlugin"
        },
    ]
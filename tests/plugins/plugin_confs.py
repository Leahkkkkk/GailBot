test_config = {
    "suite_name": "test_suite",
    "suite_abs_path": "/Users/yike/Documents/GitHub/GailBot/data/test_suite",
    "plugins": [ 
           {
            "plugin_name": "test", 
            "dependencies": [],
            "module_name":  "test_module",
            "rel_path": "src/test_module.py" 
           }
            , {
                "plugin_name": "TestDependOne",
                "dependencies": ["TestOne", "test"],
                "module_name": "test_d_one",
                "rel_path":"src/test_d_one.py"
            }
           , {
           "plugin_name": "TestDependTwo",
           "dependencies": ["TestTwo", "TestOne", "test"],
           "module_name": "test_d_two",
           "rel_path":"src/test_d_two.py"
            }  
           , {
           "plugin_name": "TestDependThree",
           "dependencies": ["TestTwo", "TestDependTwo", "test"],
            "rel_path":"src/test_dd_three.py",
            "module_name": "test_dd_three"
            }
            ,{
            "plugin_name": "TestOne",
            "dependencies": ["test"],
            "rel_path":"src/test_one.py",
            "module_name": "test_one"
             }
            ,{
            "plugin_name": "TestTwo", 
            "dependencies": ["test"],
            "rel_path":"src/test_two.py",
            "module_name": "test_two"
             }
            ,{
            "plugin_name": "TestThree",
            "dependencies": ["test"],
            "rel_path":"src/test_three.py",
            "module_name": "test_three"
            }
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


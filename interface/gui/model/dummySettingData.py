dummySettingValues={
    "Default": {
        'engine': {
            "CMU": {
                '1.language model setting': {
                    '1. language model': 'English',
                    '2. costum language model': 'Air Force Study'
                },
                '2.Acoustic Model Setting': {
                    '1. acoustic model setting': 'acoustic2',
                    '2. acoustic model setting(optional)': '3',
                    '3. plugin': 'plugin 1'
                },
                '3.CMU specialised setting': {
                    'CMU dummy setting': 'dummy setting1'
                }
            }
        },
        'Post Transcribe': {
            'Gap Length': 'dummy',
            'Turn End Threshold': 'dummy',
            'Large Pause - Lower Bound': 'dummy',
            'Laughter Detection Module bool': 'OFF',
            'Laughter Probability - Lower Bound': 'dummy',
            'Laughter Length - Lower Bound': 'dummy',
            'Upper Bound': 'dummy',
            'Lower Bound': 'dummy',
            'Beat Transcription Mode bool': 'OFF',
            'FTO (Floor Transfer offset)Transcription Mode bool': 'OFF',
            'Syllable Rate mode bool': 'OFF'
        },
    },
    "Coffee Study": {
        "engine": {
            "IBM": {
                '1.language model setting': {
                    '1. language model': 'Spanish',
                    '2. costum language model': 'Air Force Study'
                },
                '2.Acoustic Model Setting': {
                    '1. acoustic model setting': 'acoustic2',
                    '2. acoustic model setting(optional)': '3'
                },
                '3.advanced setting': {
                    '1. Advanced Setting Option 1': 'advanced 1',
                    '2. plugin': 'plugin 1'
                },
                '4.IBM specialised setting': {
                    'IBM dummy setting': 'dummy setting1'
                }
            }
        },
        'Post Transcribe': {
            'Gap Length': '0s',
            'Turn End Threshold': '0s',
            'Large Pause - Lower Bound': '0s',
            'Laughter Detection Module bool': 'ON',
            'Laughter Probability - Lower Bound': '0s',
            'Laughter Length - Lower Bound': '0s',
            'Upper Bound': '0s',
            'Lower Bound': '0s',
            'Beat Transcription Mode bool': 'ON',
            'FTO (Floor Transfer offset)Transcription Mode bool': 'ON',
            'Syllable Rate mode bool': 'ON'
        },
    },
    "HRI lab study": {
        'engine': {
            "IBM": {
                '1.language model setting': {
                    '1. language model': 'IBM language',
                    '2. costum language model': 'Air Force Study'
                },
                '2.Acoustic Model Setting': {
                    '1. acoustic model setting': 'acoustic2',
                    '2. acoustic model setting(optional)': '3'
                },
                '3.advanced setting': {
                    '1. Advanced Setting Option 1': 'advanced 1',
                    '2. plugin': 'plugin 1'
                },
                '4.IBM specialised setting': {
                    'IBM dummy setting': 'dummy setting1'
                }
            }
        },
        'Post Transcribe': {
            'Gap Length': '0s',
            'Turn End Threshold': '0s',
            'Large Pause - Lower Bound': '0s',
            'Laughter Detection Module bool': 'OFF',
            'Laughter Probability - Lower Bound': '0s',
            'Laughter Length - Lower Bound': '0s',
            'Upper Bound': '0s',
            'Lower Bound': '0s',
            'Beat Transcription Mode bool': 'OFF',
            'FTO (Floor Transfer offset)Transcription Mode bool': 'OFF',
            'Syllable Rate mode bool': 'OFF'
        }
    }
}

dummySettingForms={
    "Required Setting": {
        "Engine":{"IBM": {
            "1.language model setting": {
                "1. language model": [
                    "IBM language",
                    "English",
                    "Spanish"
                ],
                "2. costum language model": [
                    "HRI lab",
                    "None",
                    "Air Force Study"
                ]
            },
            "2.Acoustic Model Setting": {
                "1. acoustic model setting": [
                    "acoustic1",
                    "acoustic2",
                    "acoustic3"
                ],
                "2. acoustic model setting(optional)": [
                    "1",
                    "2",
                    "3"
                ]
            },
            "3.advanced setting": {
                "1. Advanced Setting Option 1": [
                    "advanced 1",
                    "advanced 2",
                    "advanced 3"
                ],
                "2. plugin": [
                    "plugin 1",
                    "plugin 2"
                ]
            },
            "4.IBM specialised setting": {
                "IBM dummy setting": [
                    "dummy setting1",
                    "dummy setting2",
                    "dummy setting3"
                ]
            }
        },
        "CMU": {
            "1.language model setting": {
                "1. language model": [
                    "CMU language",
                    "English",
                    "Spanish"
                ],
                "2. costum language model": [
                    "CMU costum",
                    "None",
                    "Air Force Study"
                ]
            },
            "2.Acoustic Model Setting": {
                "1. acoustic model setting": [
                    "acoustic1",
                    "acoustic2",
                    "acoustic3"
                ],
                "2. acoustic model setting(optional)": [
                    "1",
                    "2",
                    "3"
                ],
                "3. plugin": [
                    "plugin 1",
                    "plugin 2"
                ]
            },
            "3.CMU specialised setting": {
                "CMU dummy setting": [
                    "dummy setting1",
                    "dummy setting2",
                    "dummy setting3"
                ]
            }
        }},
        
        "OutPut Format": {
            "Corpus Settings":{
                "Corpus aame": "enter corpus name",
                "Corpus location": "enter corpus location",
                "Corpus room layout": "enter corous room layout",
                "Corpus situation":"enter situation"
            }
        }
    },
    "Post Transcribe": {
        "General": {
            "Gap Length": "0s",
            "Turn End Threshold": "0s",
            "Large Pause - Lower Bound": "0s"
        },
        "Laghter Settings": {
            "Laughter Detection Module bool": "ON",
            "Laughter Probability - Lower Bound": "0s",
            "Laughter Length - Lower Bound": "0s",
        },
        "MicroPause Bound": {
            "Upper Bound": "0s",
            "Lower Bound": "0s"
        },
        "Transcription Model": {
            "Beat Transcription Mode bool": "ON",
            "FTO (Floor Transfer offset)Transcription Mode bool": "ON",
            "Syllable Rate mode bool": "ON"
        },
    }
}

testSet = {
    'a': {
        'engine': {
            "IBM": {
                '1.language model setting': {
                    '1. language model': 'English',
                    '2. costum language model': 'None'
                },
                '2.Acoustic Model Setting': {
                    '1. acoustic model setting': 'acoustic1',
                    '2. acoustic model setting(optional)': '2'
                },
                '3.advanced setting': {
                    '1. Advanced Setting Option 1': 'advanced 1',
                    '2. plugin': 'plugin 1'
                },
                '4.IBM specialised setting': {
                    'IBM dummy setting': 'dummy setting1'
                }
            }
        },
        'Post Transcribe': {
            'Gap Length': '0s',
            'Turn End Threshold': '0s',
            'Large Pause - Lower Bound': '0s',
            'Laughter Detection Module bool': 'ON',
            'Laughter Probability - Lower Bound': '0s',
            'Laughter Length - Lower Bound': '0s',
            'Upper Bound': '0s',
            'Lower Bound': '0s',
            'Beat Transcription Mode bool': 'ON',
            'FTO (Floor Transfer offset)Transcription Mode bool': 'ON',
            'Syllable Rate mode bool': 'ON'
        },
        'Output Form Data': {
            'language': 'English',
            'Number of speaker': '1',
            'gender0': 'Female',
            'gender1': 'Female',
            'gender2': 'Female',
            'Output File Format': '.TXT'
        },
        'User Info': {
            'username': 'ad',
            'password': 'ad'
        }
    }
}
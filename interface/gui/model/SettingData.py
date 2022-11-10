'''
File: SettingData.py
Project: GailBot GUI
File Created: Friday, 4th November 2022 1:01:27 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Wednesday, 9th November 2022 12:32:55 pm
Modified By:  Siara Small  & Vivian Li
-----
'''



""" placeholder data profile values for development """
SettingValues={
    "Default": {
        "RequiredSetting": {
            'Engine': {
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
                        'CMU setting option': 'setting option 1'
                    }
                }
            },
            'Output Form Data': {
                'language': 'Spanish',
                'Number of speaker': '1',
                'gender0': 'Female',
                'gender1': 'Female',
                'gender2': 'Female',
                'Corpus Settings': {
                    'Corpus name': 'enter corpus name',
                    'Corpus location': 'enter corpus location',
                    'Corpus room layout': 'enter corous room layout',
                    'Corpus situation': 'enter situation'
                },
                'Output File Format': 'CHART'
            }
        },
        'PostTranscribe': {
            'Gap Length': '0',
            'Turn End Threshold': '0',
            'Large Pause - Lower Bound': '0',
            'Laughter Detection Module bool': 'OFF',
            'Laughter Probability - Lower Bound': '0',
            'Laughter Length - Lower Bound': '0',
            'Upper Bound': '0',
            'Lower Bound': '0',
            'Beat Transcription Mode bool': 'OFF',
            'FTO (Floor Transfer offset)Transcription Mode bool': 'OFF',
            'Syllable Rate mode bool': 'OFF'
        },
        "Plugins": {
            "constructTree"
        }
    },
    "Coffee Study": {
        "RequiredSetting": {
            "Engine": {
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
                        'IBM setting option': 'setting option 2'
                    }
                }
            },
            'Output Form Data': {
                'language': 'Spanish',
                'Number of speaker': '1',
                'gender0': 'Female',
                'gender1': 'Female',
                'gender2': 'Female',
                'Corpus Settings': {
                    'Corpus name': 'enter corpus name',
                    'Corpus location': 'enter corpus location',
                    'Corpus room layout': 'enter corous room layout',
                    'Corpus situation': 'enter situation'
                },
                'Output File Format': 'CHART'
            }
        },
        'PostTranscribe': {
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
        "Plugins": {
            "constructTree",
            "utteranceDict",
            "conversationDict"
        }
    },
    "HRI lab study": {
        "RequiredSetting": {
            'Engine': {
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
                        'IBM setting option': 'setting option 3'
                    }
                }
            },
            'Output Form Data': {
                'language': 'Spanish',
                'Number of speaker': '1',
                'gender0': 'Female',
                'gender1': 'Female',
                'gender2': 'Female',
                'Corpus Settings': {
                    'Corpus name': 'enter corpus name',
                    'Corpus location': 'enter corpus location',
                    'Corpus room layout': 'enter corous room layout',
                    'Corpus situation': 'enter situation'
                },
                'Output File Format': 'CHART'
            }
        },
        'PostTranscribe': {
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
        },
        "Plugins": {
            "constructTree",
            "XMLtoCSV",
            "overlaps"
        }
    },
}
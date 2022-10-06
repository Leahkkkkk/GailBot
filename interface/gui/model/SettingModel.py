'''
File: SettingModel.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 9:49:48 am
Modified By:  Siara Small  & Vivian Li
-----
'''


""" to storing setting data
TODO: Create D.S to store user created setting profile
"""

class SettingModel:
    """ dummy setting data for testing setting page functionality """
    def __init__(self):
      self.data = {
        "engine": {"IBM": 
                    {"1. language model":["English", "Spanish"],
                      "2. costum language model": ["HRI lab", "None", "Air Force Study"],
                      "3. acoustic model setting": ["acoustic1", "acoustic2", "acoustic3"],
                      "4. advanced setting": ["advanced 1", "advanced 2", "advanced 3"],
                      "5. IBM specialised setting": ["dummy setting1", "dummy setting2", "dummy setting3"]
                    },
                  "CMU": 
                    {"1. language model":["English", "Spanish", "French", "Madarin"],
                     "2. acoustic model setting": ["acoustic4", "acoustic5", "acoustic6"],
                     "3. advanced setting": ["advanced 7", "advanced 11", "advanced 9"]
                    }}  ,
          "Post Transcribe": { "General":["Gap Length", "Turn End Threshold", "Large Pause - Lower Bound"],
                               "Transcription Model": ["Beat Transcription Mode", "FTO Transcription Mode", "Syllable Rate mode"],
                               "MicroPause Bound": ["Upper Bound", "Lower Bound"]}
        }
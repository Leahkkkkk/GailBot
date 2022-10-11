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
                      {"1.language model setting":
                          {"1. language model":["IBM language", "English", "Spanish"],
                           "2. costum language model": ["HRI lab", "None", "Air Force Study"]},
                          
                        "2.Acuoustic Model Setting": 
                            {"1. acoustic model setting": ["acoustic1", "acoustic2", "acoustic3"],
                             "2. acoustic model setting(optional)": ["1", "2", "3"]},
                        
                        "3.advanced setting": 
                            {"1. Advanced Setting Option 1":["advanced 1", "advanced 2", "advanced 3"],
                             "2. plugins":["puglins 1", "plugins 2"]},
                        
                        "4.IBM specialised setting": {
                            "IBM dummy setting": ["dummy setting1", "dummy setting2", "dummy setting3"]}
                      },
                    "CMU": 
                        {"1.language model setting":
                            {"1. language model":["CMU language", "English", "Spanish"],
                             "2. costum language model": ["CMU costum", "None", "Air Force Study"]},
                            
                            "2.Acuoustic Model Setting": 
                                {"1. acoustic model setting": ["acoustic1", "acoustic2", "acoustic3"],
                                "2. acoustic model setting(optional)": ["1", "2", "3"],
                                "3. plugins":["puglins 1", "plugins 2"]},
                            
                            "3.CMU specialised setting": {
                                "CMU dummy setting": ["dummy setting1", "dummy setting2", "dummy setting3"]}
                        }},
        
        
        
        
          "Post Transcribe": { "General":["Gap Length", "Turn End Threshold", "Large Pause - Lower Bound"],
                               "Transcription Model": ["Beat Transcription Mode", "FTO Transcription Mode", "Syllable Rate mode"],
                               "MicroPause Bound": ["Upper Bound", "Lower Bound"]}
        }
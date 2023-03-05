'''
File: Model.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 9:48:10 am
Modified By:  Siara Small  & Vivian Li
-----
'''
from typing import List, Tuple, Dict
from .organizer import FileOrganizer, ProfileOrganizer, PluginOrganizer
from gailbot.api import GailBot

class Model():
    """ a database that stores three tables: 
        1.FileData: a file data base with all the file uploaded by user
        2.ProfileData: profile database with all the profile created by user
        3.PluginData: plugin database with all the plugin and 
                    plugin source loaded by user
    """
    def __init__(self, gbController: GailBot):
        self.fileOrganizer = FileOrganizer(gbController)
        self.profileOrganizer = ProfileOrganizer(gbController)
        self.pluginOrganizer = PluginOrganizer(gbController)
    
    def profileKeys(self) -> List[str]:
        return self.profileOrganizer.profilekeys
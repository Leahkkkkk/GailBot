'''
File: MVController.py
Project: GailBot GUI
File Created: Tuesday, 1st November 2022 6:13:52 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Tuesday, 1st November 2022 7:39:49 pm
Modified By:  Siara Small  & Vivian Li
-----
Description:
Model view controller than connect ths database to a front end view object 
'''
from gbLogger import makeLogger 
from view import ViewController
from .organizer import FileOrganizer, PluginOrganizer, ProfileOrganizer
from gailbot.api import GailBot

class MVController:
    """ 
    Model View controller to send requested data on view and 
    handle request from view to modify data in the database

    Constructor Args:
        view (MainWindow): main view 
        fileOrganizer (FileModel): file database 
        profileOrganizer (ProfileModel): profile database
        pluginOrganizer (PluginModel): plugin database
    
    Field:
        view: view object 
        fileOrganizer: file database 
        profileOrganizer: profile database
        pluginOrganizer: plugin database
    
    Public Function:
        exec(): driver function that starts to run the model view controller
    """
    def __init__(self, view: ViewController, gb: GailBot) -> None:
        self.fileOrganizer = FileOrganizer(gb, view.getFileSignal())
        self.profileOrganizer = ProfileOrganizer(gb, view.getProfileSignal())
        self.pluginOrganizer = PluginOrganizer(gb, view.getPluginSignal())
        self.logger = makeLogger("F")
        self.view  = view 
        self.gb = gb 
        
    def exec(self):
        """ public function to execute the model view controller """
        # add available plugin suite to the frontend interface
        pluginSuites = self.gb.get_all_plugin_suites()
        self.logger.info(f"get plugin suites {pluginSuites}")
        pluginInfo =[(suite, self.gb.get_plugin_suite_metadata(suite)) for suite in pluginSuites]
        self.logger.info(f"get plugin suite info {pluginInfo}")
        self.view.addAvailablePluginSuites(pluginInfo)

        # add available setting to the frontend interface
        settingNames = self.gb.get_all_settings_name()
        self.logger.info(f"get profile {settingNames}")
        self.view.addAvailableSettings(settingNames)
        

     
     
    
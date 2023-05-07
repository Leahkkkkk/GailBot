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
from .organizer import FileOrganizer, PluginOrganizer, ProfileOrganizer, EngineOrganizer
from gailbot.api import GailBot

class MVController:
    """ 
    Model View controller to handle data-related view request 
    
    wrapper object that contain fileOrganizer, profileOrganizer, 
    pluginOrganizer, engineOrganizer that handle request for 
    different data 
    """
    def __init__(self, view: ViewController, gb: GailBot) -> None:
        self.fileOrganizer = FileOrganizer(gb, view.getFileSignal())
        self.profileOrganizer = ProfileOrganizer(gb, view.getProfileSignal())
        self.pluginOrganizer = PluginOrganizer(gb, view.getPluginSignal())
        self.engineOrganizer = EngineOrganizer(gb, view.getEngineSignal())
        self.logger = makeLogger()
        self.view  = view 
        self.gb = gb 
        
    def exec(self):
        """ public function to execute the model view controller """
        # add available plugin suite to the frontend interface
        pluginSuites = self.gb.get_all_plugin_suites()
        self.logger.info(f"get plugin suites {pluginSuites}")
        pluginInfo =[(suite, 
                      self.gb.get_plugin_suite_metadata(suite),
                      self.gb.is_official_suite(suite))
                     for suite in pluginSuites]
        self.logger.info(f"get plugin suite info {pluginInfo}")
        self.view.addAvailablePluginSuites(pluginInfo)

        # add available setting to the frontend interface
        settingNames = self.gb.get_all_settings_name()
        settingInfo = [(name, self.gb.get_setting_dict(name)) for name in settingNames]
        self.logger.info(f"get profile {settingInfo}")
        self.view.addAvailableSettings(settingInfo)
        
        # add available engines 
        engines = self.gb.get_engine_setting_names()
        engineInfo = [(name, self.gb.get_engine_setting_data(name)) for name in engines]
        self.logger.info(f"get engines{engineInfo}")
        self.view.addAvailableEngineSetting(engineInfo)
     
     
    
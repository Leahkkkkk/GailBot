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
        
        # add available setting to the frontend interface
        settingNames = self.gb.get_all_settings_name()
        self.logger.info(f"get profile {settingNames}")
        self.view.addAvailableSettings(settingNames)
        
        # add available plugin suite to the frontend interface
        pluginSuites = self.gb.get_all_plugin_suites()
        self.logger.info(f"get plugin suites {pluginSuites}")
        pluginInfo =[(suite, self.gb.get_plugin_suite_metadata(suite)) for suite in pluginSuites]
        self.logger.info(f"get plugin suite info {pluginInfo}")
        self.view.addAvailablePluginSuites(pluginInfo)

    
    def exec(self):
        """ public function to execute the model view controller """
        self._connectFileDBToView()
        self._connectViewToFileDB()
        self._connectProfileDBToView()
        
    def _connectFileDBToView(self):
        """ connect the signal from the file database to view
            change the presentation of data on the view
        """
        self.logger.info("")
        dbSignal = self.fileOrganizer.signals
        view = self.view
        # connect database response to view to display change
        dbSignal.fileAdded.connect(view.addFile)
        dbSignal.fileUpdated.connect(view.updateFile)
        
        # handle file database's request to load the profile of one file
        dbSignal.profileRequest.connect(self.view.loadProfile)
        dbSignal.error.connect(self.view.showErr)
     
    def _connectViewToFileDB(self):
        """ connect the signal from the view to file database  
            store, delete or edit the database based on the view's request
        """
        self.logger.info("initialize model&view connection")
        viewSignal = self.view.getFileSignal()
        db = self.fileOrganizer
        # handle view's request to pfost new file
        viewSignal.postFile.connect(db.post)
        # handle view's request to edit file data
        viewSignal.editFile.connect(db.edit)
        # handle view's request to change file profile 
        viewSignal.changeProfile.connect(db.editFileProfile)
        # handle view's reuqesgt to see file profile
        viewSignal.requestprofile.connect(db.requestProfile)
        # handle remove file 
        viewSignal.delete.connect(db.delete)
    
    #     """ connect the signal from the view to plugin database  
    #         store, delete or edit the database based on the view's request
    #     """
    #     self.logger.info("initialize model&view connection")
    #     viewSignal = self.view.getPluginSignal()
    #     # handle view's request to load new plugin
    #     viewSignal.addPlugin.connect(self.pluginOrganizer.addPlugin)
    #     viewSignal.detailRequest.connect(self.pluginOrganizer.gerPluginSuiteDetail)
    
    
    # def _connectPluginDBToView(self):
    #     """ connect the signal from the plugin database to view
    #         change the presentation of data on the view
    #     """
    #     self.logger.info("initialize model&view connection")
    #     signal = self.pluginOrganizer.signals
    #     # reflect the plugin database's changes on view
    #     signal.pluginAdded.connect(self.view.addPlugin)
    #     signal.pluginDetail.connect(self.view.displayPluginSuiteDetail)
    
        
    def _connectProfileDBToView(self):
        """ connect the signal from the profile database to view
            change the presentation of data on the view
        """
        self.logger.info("initialize model&view connection")
        dbSignal = self.profileOrganizer.signals
        # connect db's response to load profile data 
        dbSignal.send.connect(self.view.loadProfile)
        # connect db's response to add new profile selection on view
        # dbSignal.profileAdded.connect(self.view.addProfile) 
        dbSignal.deleteProfile.connect(self.view.deleteProfile)
        dbSignal.deleteProfile.connect(self.fileOrganizer.profileDeleted)
        dbSignal.error.connect(self.view.showErr)
        
    
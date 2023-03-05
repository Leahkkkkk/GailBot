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

from util.Logger import makeLogger
from view.MainWindow import MainWindow
from model.organizer import FileOrganizer, PluginOrganizer, ProfileOrganizer


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
    def __init__(
        self, 
        view: MainWindow, 
        fileOrganizer: FileOrganizer, 
        profileOrganizer: ProfileOrganizer, 
        pluginOrganizer: PluginOrganizer) -> None:  
        self.logger = makeLogger("Backend")
        self.view = view 
        self.fileOrganizer = fileOrganizer
        self.profileOrganizer = profileOrganizer
        self.pluginOrganizer = pluginOrganizer
    
    def exec(self):
        """ public function to execute the model view controller """
        self._connectFileDBToView()
        self._connectViewToFileDB()
        self._connectPluginDBToView()
        self._connectViewToPluginDB()
        self._connectProfileDBToView()
        self._connectViewToProfileDB()
        
    def _connectFileDBToView(self):
        """ connect the signal from the file database to view
            change the presentation of data on the view
        """
        self.logger.info("")
        dbSignal = self.fileOrganizer.signals
        view = self.view
        # connect database response to view to display change
        dbSignal.fileAdded.connect(view.addFileToTables)
        dbSignal.fileUpdated.connect(view.updateFile)
        
        # handle file database's request to load the profile of one file
        dbSignal.profileRequest.connect(self.profileOrganizer.get)
     
    def _connectViewToFileDB(self):
        """ connect the signal from the view to file database  
            store, delete or edit the database based on the view's request
        """
        self.logger.info("initialize model&view connection")
        viewSignal = self.view.fileTableSignals
        db = self.fileOrganizer
        # handle view's request to pfost new file
        viewSignal.postFile.connect(db.post)
        # handle view's request to edit file data
        viewSignal.editFile.connect(db.edit)
        # handle view's request to change file profile 
        viewSignal.changeProfile.connect(db.editFileProfile)
        # handle view's reuqesgt to see file profile
        viewSignal.requestprofile.connect(db.requestProfile)
    
    def _connectViewToPluginDB(self):
        """ connect the signal from the view to plugin database  
            store, delete or edit the database based on the view's request
        """
        self.logger.info("initialize model&view connection")
        viewSignal = self.view.profileSignals
        # handle view's request to load new plugin
        viewSignal.addPlugin.connect(self.pluginOrganizer.post)
    
    def _connectPluginDBToView(self):
        """ connect the signal from the plugin database to view
            change the presentation of data on the view
        """
        self.logger.info("initialize model&view connection")
        dbSignal = self.pluginOrganizer.signals
        view = self.view.MainStack.ProfileSettingPage
        # reflect the plugin database's changes on view
        dbSignal.pluginAdded.connect(view.addPluginHandler)
        
    def _connectViewToProfileDB(self):
        """ connect the signal from the view to profile database  
            store, delete or edit the database based on the view's request
        """
        self.logger.info("initialize model&view connection")
        viewSignal = self.view.profileSignals
        db = self.profileOrganizer
        # handle view's request to post new profile
        viewSignal.post.connect(db.post)
        # handle view's request to get profile data 
        viewSignal.get.connect(db.get)
        # handle view's request to cedit profile data 
        viewSignal.edit.connect(db.edit)
    
    def _connectProfileDBToView(self):
        """ connect the signal from the profile database to view
            change the presentation of data on the view
        """
        self.logger.info("initialize model&view connection")
        dbSignal = self.profileOrganizer.signals
        profileView = self.view.MainStack.ProfileSettingPage
        fileView = self.view.MainStack.FileUploadPage.fileTable
        # connect db's response to load profile data 
        dbSignal.send.connect(profileView.loadProfile)
        # connect db's response to add new profile selection on view
        dbSignal.profileAdded.connect(profileView.addProfile)
        dbSignal.profileAdded.connect(fileView.addProfile)
        
        dbSignal.delete.connect(self.fileOrganizer.profileDeleted)
        
    
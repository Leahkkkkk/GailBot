'''
File: MVController.py
Project: GailBot GUI
File Created: Tuesday, 1st November 2022 6:13:52 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Tuesday, 1st November 2022 7:39:49 pm
Modified By:  Siara Small  & Vivian Li
-----
'''

from util.Logger import makeLogger
from view.MainWindow import MainWindow
from model.dataBase.fileDB import FileModel
from model.dataBase.profileDB import ProfileModel
from model.dataBase.pluginDB import PluginModel

logger = makeLogger("Backend")

class MVController:
    def __init__(
        self, 
        view: MainWindow, 
        fileDB: FileModel, 
        profileDB: ProfileModel, 
        pluginDB: PluginModel) -> None:
        """ Model View controller to send requested data on view and 
            handle request from view to modify data in the database

        Args:
            view (MainWindow): main view 
            fileDB (FileModel): file database 
            profileDB (ProfileModel): profile database
            pluginDB (PluginModel): plugin database
        """
        self.view = view 
        self.fileDB = fileDB
        self.profileDB = profileDB
        self.pluginDB = pluginDB
    
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
        logger.info("")
        dbSignal = self.fileDB.signals
        view = self.view
        # connect database response to view to display change
        dbSignal.fileAdded.connect(view.addFileToTables)
        dbSignal.fileUpdated.connect(view.updateFile)
        
        # handle file database's request to load the profile of one file
        dbSignal.profileRequest.connect(self.profileDB.get)
     
    def _connectViewToFileDB(self):
        """ connect the signal from the view to file database  
            store, delete or edit the database based on the view's request
        """
        logger.info("initailize model&view connection")
        viewSignal = self.view.fileTableSignals
        db = self.fileDB
        # handle view's request to post new file
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
        logger.info("initailize model&view connection")
        viewSignal = self.view.profileSignals
        # handle view's request to load new plugin
        viewSignal.addPlugin.connect(self.pluginDB.post)
    
    def _connectPluginDBToView(self):
        """ connect the signal from the plugin database to view
            change the presentation of data on the view
        """
        logger.info("initailize model&view connection")
        dbSignal = self.pluginDB.signals
        view = self.view.MainStack.ProfileSettingPage
        # reflect the plugin database's changes on view
        dbSignal.pluginAdded.connect(view.addPluginHandler)
        
    def _connectViewToProfileDB(self):
        """ connect the signal from the view to profile database  
            store, delete or edit the database based on the view's request
        """
        logger.info("initailize model&view connection")
        viewSignal = self.view.profileSignals
        db = self.profileDB
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
        logger.info("initailize model&view connection")
        dbSignal = self.profileDB.signals
        profileView = self.view.MainStack.ProfileSettingPage
        fileView = self.view.MainStack.FileUploadPage.fileTable
        # connect db's response to load profile data 
        dbSignal.send.connect(profileView.loadProfile)
        # connect db's response to add new profile selection on view
        dbSignal.profileAdded.connect(profileView.addProfile)
        dbSignal.profileAdded.connect(fileView.addProfile)
        
    
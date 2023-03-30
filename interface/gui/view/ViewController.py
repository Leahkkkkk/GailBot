from typing import Dict, TypedDict, Tuple, Any, List
from view.MainWindow import MainWindow
from view.Signals import FileSignals, ProfileSignals, ViewSignals, PluginSignals

class SettingDict(TypedDict):
    engine_setting: Dict
    plugin_setting: List[str] 

class ViewController():
    """ 
        a view controller that provides functions that the caller 
        can use to interact with the frontend interface
    """
    def __init__(self) -> None:
        self.window: MainWindow = MainWindow()
    
    def addAvailableSettings(self, profileNames: List[str]):
        """ add the available setting to the profile setting interface

        Args:
            profileNames (List[str]): a list of profile names
        """
        self.window.addAvailableSetting(profileNames)
    
    
    def addAvailablePluginSuites(self, pluginSuites: List[Tuple[str, Dict[str, str]]]):
        """ add the available plugin suites to the interface

        Args:
            pluginSuites (List[Tuple[str, Dict[str, str]]]): a list of tuples 
            that stores the plugin suites information, 
            the first element of the tuple stores the plugin name as a string
            and the second element stores the plugin metadata as a dictionary
        """
        self.window.addAvailablePluginSuites(pluginSuites)
        
        
    def show(self):
        """ 
        run the interface
        """
        self.window.show()
        
    # function that involves in file transcription 
    def showTranscribeInProgress(self):
        """ 
        when called, redirect the gui to the transcribe in progress page
        """
        self.window.showTranscribeInProgress()
        
    def showTranscribeSuccess(self):
        """ 
        when called, redirect the gui to the transcribe success page
        """
        self.window.showTranscribeSuccess()
        
    def showFileUploadPage(self):
        """ 
        when called, redirect the gui to the  file upload page
        """
        self.window.showFileUploadPage()
        
    def busyThreadWarning(self):
        """ 
        when called, show a warning message box indicating the thread is 
        busy
        """
        self.window.busyThreadPool()
    
    def showStatusMsg(self, msg, time = 2000):
        """ show msg on the gui's status bar

        Args:
            msg (str): the message tha will be displayed
            time (int, optional): the time the msg will be displayed
            Defaults to 2000.
        """
        self.window.showStatusMsg(msg,time)     
   
    def showFilesTranscriptionProgress(self, msg: Tuple[str, str]):
        """ when called, show the transcribe process for all the file
            in gui

        Args:
            msg (str): the message
        """
        self.window.showFileProgress(msg)
        
    def clearStatusMsg(self):
        """ 
        when called, clear up the current status message
        """
        self.window.freeThread()
  
    def transcriptionFailed(self, err : str):
        """ display a warning box with error message to indicate that the 
            when transcription fails

        Args:
            err (str): the error message
        """
        self.window.TranscribeFailed(err)
        
    
    def afterTranscribeCancelled(self):
        """
            return back to the file upload page when user decide to stop 
             transcribe
        """
        self.window.confirmCancel()
        
    # function that involves in editing, adding, and deleting file 
    def updateFile(self, data: Tuple[str, Any]):
        """ update the data of one file

        Args:
            data (Tuple[str, Any]): a tuple with field and content pair, 
                the field stores the part of the file that will be changed, 
                and the content stores the new data that will be set to 

        Returns:
            None 
        """
        return self.window.updateFile(data)
    
    def addFile(self, file: Dict[str, str]):
        """add file to the data base

        Args:
            file (Dict[str, str]): _description_

        """
        return self.window.addFileToTables(file)
    
    def changeFileToTranscribed(self, filekey: str):
        """change the file status to be transcribed

        Args:
            filekey (str): the key that identifies the file
        """         
        self.window.changeFiletoTranscribed(filekey)
        
        
    # function that involves in editing, deleting and adding profile
    def deleteProfile(self, profileName: str):
        """ delete any frontend element relating to the profile 
            identified by  profileName

        Args:
            profileName (str): the name of the profile to be deleted
        """
        self.window.deleteProfile(profileName)
    
    
    def addProfile(self, profileName:str):
        """ add profile identified by profileName to the frontend interface 

        Args:
            profileName (str): the name of the profile to be added
        """
        self.window.addProfile(profileName)
    
    def loadProfile(self, profileData: Tuple[str, Dict]):
        """ load the profile data to the front end profile setting page

        Args:
            profileData (Tuple[str, Dict]):  a tuple that stores the name of 
                                             the profile and the setting data
        """
        self.window.loadProfile(profileData)
        
   
    def addPlugin(self, pluginSuite: Tuple[str, Dict[str, str]]):
        """ add plugin identified by plugin name to the view

        Args:
            pluginSuite: Tuple[str, Dict[str, str]]: 
            a tuple that stores the plugin suite information 
            the tuple contains the name of the plugin suite and a 
            dictionary of the plugin suite information
        """
        self.window.addPlugin(pluginSuite)
   
    # function that involves the entire view object
    def closeEvent(self, id: int ) -> None:
        """ called when a request to close the app 

        Args:
            id (int): the exitcode 
        """
        self.window.closeEvent(id)
     
    def showErr(self, err: str) -> None:
        """when called, open a warning box to show the err message

        Args:
            err (str): the error message
        """
        self.window.showError(err)
       
    # return the signal interface    
    def getFileSignal(self) -> FileSignals:
        """ 
        returns the file table signals
        """
        return self.window.fileTableSignals
    
    def getProfileSignal(self) -> ProfileSignals:
        """ 
        returns the profile signals 
        """
        return self.window.profileSignals
    
    def getViewSignal(self) -> ViewSignals:
        """ 
        returns the view signal
        """
        return self.window.viewSignal
   
    def getPluginSignal(self) -> PluginSignals:
        """ 
        returns the plugin signal
        """
        return self.window.pluginSignal
    
    def displayPluginSuiteDetail(self, suiteInfo) -> None :
        """ 
        open a frontend dialog to display suiteInfo 
        """
        self.window.displayPluginSuiteDetail(suiteInfo) 
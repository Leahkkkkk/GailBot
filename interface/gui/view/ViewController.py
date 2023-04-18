from typing import Dict, TypedDict, Tuple, Any, List
from view.MainWindow import MainWindow
from view.Signals import FileSignals, DataSignal, ViewSignals, DataSignal

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
    
    def show(self):
        """ 
        run the interface
        """
        self.window.show()
        
    def addAvailableSettings(self, profileNames: List[Tuple[str, Dict]]):
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
        
     
    def addAvailableEngineSetting(self, engines: List[Tuple[str, Dict]]):
        """ add the available engine setting to the interface

        Args:
            engines: a list of engine setting names 
        """
        self.window.addAvailableEngineSettings(engines)
    
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
  
    def afterTranscribeCancelled(self):
        """
            return back to the file upload page when user decide to stop 
             transcribe
        """
        self.window.confirmCancel()
        
    def changeFileToTranscribed(self, filekey: str):
        """change the file status to be transcribed

        Args:
            filekey (str): the key that identifies the file
        """         
        self.window.changeFiletoTranscribed(filekey)
     
    def removeFile(self, filekey:str):
        """remove file from the file table

        Args:
            filekey (str): the key that identifies the file
        """         
        self.window.removeFile(filekey)   
    
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
    
    def getProfileSignal(self) -> DataSignal:
        """ 
        returns the profile signals 
        """
        return self.window.MainStack.SettingPage.ProfilePage.signal
    
    def getViewSignal(self) -> ViewSignals:
        """ 
        returns the view signal
        """
        return self.window.viewSignal
   
    def getPluginSignal(self) -> DataSignal:
        """ 
        returns the plugin signal
        """
        return self.window.MainStack.SettingPage.PluginPage.signal
    
    def getEngineSignal(self) -> DataSignal:
        """
        return the engine signal
        """ 
        return self.window.MainStack.SettingPage.EngineSetPage.signal
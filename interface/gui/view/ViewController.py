from typing import Dict, TypedDict, Tuple, Any, List
from view.MainWindow import MainWindow
from view.signal.interface import TranscribeSignal, DataSignal, SystemSignal, DataSignal
from view.signal.signalObject import PluginSignal, ProfileSignal, FileSignal, EngineSignal, GuiSignal, GBTranscribeSignal
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
    def getFileSignal(self) -> DataSignal:
        """ 
        returns the file table signals
        """
        return FileSignal 
    
    def getProfileSignal(self) -> DataSignal:
        """ 
        returns the profile signals 
        """
        return ProfileSignal 
    
    def getViewSignal(self) -> SystemSignal:
        """ 
        returns the view signal
        """
        return GuiSignal
   
    def getPluginSignal(self) -> DataSignal:
        """ 
        returns the plugin signal
        """
        return PluginSignal 
    
    def getEngineSignal(self) -> DataSignal:
        """
        return the engine signal
        """ 
        return EngineSignal

    def getTranscriptionSignal(self) -> TranscribeSignal:
        """ 
        return the transcribeSignal
        """
        return GBTranscribeSignal
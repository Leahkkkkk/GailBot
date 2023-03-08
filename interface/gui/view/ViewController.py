from typing import Dict, TypedDict, Tuple, Any
from view.MainWindow import MainWindow

class SettingDict(TypedDict):
    engine_setting: Dict
    plugin_setting: Dict 
    
    
class ViewController():
    """ 
        a view controller that provides functions that the caller 
        can use to interact with the frontend interface
    """
    def __init__(self, 
                 setting_data: SettingDict) -> None:
        self.window = MainWindow(setting_data)
    
    def showTranscribeInProgress(self):
        """ 
        when called, redirect the gui to the transcribe in progress page
        """
        self.window.showTranscribeInProgress()
        
    def showTranscribeSuccess(self):
        """ 
        when called, redirect the gui to the transcribe success page
        """
        self.window.showTranscribeInProgress()
        
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
            time (int, optional): the time the msg will stay in thjeh pgui
            Defaults to 2000.
        """
        self.window.showStatusMsg(msg,time)     
   
    def showFilesTranscriptionProgress(self, msg):
        """ when called, show the transcribe process for all the file
            in gui

        Args:
            msg (str): the message
        """
        self.window.showFileProgress()
        
    def clearStatusMsg(self):
        """ 
        when called, clear up the current status message
        """
        self.window.freeThread()
  
    def transcriptipnFailed(self, err : str):
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
        
        
    def updateFile(self, data: Tuple[str, Any]):
        """ update the data of one file

        Args:
            data (Tuple[str, Any]): a tuple with field and content pair, 
                the field stores the part of the file that will be changed, 
                and the content stores the new data that will be set to 

        Returns:
            None 
        """
        return self.window.updateFile
    
    
    def addFile(self, file: Dict[str, str]):
        """add file to the data base

        Args:
            file (Dict[str, str]): _description_

        Returns:
            _type_: _description_
        """
        return self.window.addFileToTables(file)
    
    def changeFileToTranscribed(self, filekey: str):
        """change the file status to be transcribed

        Args:
            filekey (str): the key that identifies the file
        """         
        self.window.changeFiletoTranscribed(filekey)
        
    def closeEvent(self, id) -> None:
        """ called when a request to close the app 

        Args:
            id (int): the exitcode 
        """
        self.window.closeEvent(id)
     
    def showErr(self, err):
        """when called, open a warning box to show the err message

        Args:
            err (str): the error message
        """
        self.window.showError(err)
        
    def getFileSignal(self):
        """ 
        returns the file table signals
        """
        return self.window.fileTableSignals
    
    def getProfileSignal(self):
        """ 
        returns the profile signals 
        """
        return self.window.profileSignals
    
    def getViewSignal(self):
        """ 
        returns the view signal
        """
        return self.window.viewSignal
    
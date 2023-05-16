'''
File: TranscribeController.py
Project: GailBot GUI
File Created: Tuesday, 1st November 2022 7:40:56 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Tuesday, 1st November 2022 7:41:01 pm
Modified By:  Siara Small  & Vivian Li
-----
Description:
connect the backend transcription process with the front end view object, 
so that the front end is able to reflect the transcription progress
'''

from dataclasses import dataclass
from typing import List, Dict, Tuple

from controller.util.Error import  ERR
from controller.Request import Request
from view import ViewController
from gbLogger import makeLogger
from PyQt6.QtCore import pyqtSignal, QObject, QThreadPool, QRunnable, pyqtSlot
from gailbot.api import GailBot

@dataclass 
class ThreadControl:
    maxThread = 5 
    
    
class Signal(QObject):
    """ a signal object to communicate the transcription process with 
        the front end view object 
    """
    start    = pyqtSignal()
    finish   = pyqtSignal()
    error    = pyqtSignal(str)
    busy     = pyqtSignal()
    progress = pyqtSignal(tuple)
    killed   = pyqtSignal()

class TranscribeController(QObject):
    def __init__(self, ThreadPool: QThreadPool, view: ViewController, gb: GailBot):
        """ a controller that controls the transcription process

        Constructor Args:
            ThreadPool (QThreadPool): a threadpool provided by the caller 
            view (ViewController): view object that handle the signal from the 
                                   backend
            gb: an instance of GailBot api 
        
        """
        super().__init__()
        self.logger = makeLogger ("B")
        self.logger.info("initialize the transcribe controller")
        self.ThreadPool = ThreadPool
        self.signal = Signal()
        self.transcribeSignal = view.getTranscriptionSignal()
        self.gb = gb
        # connect to view handler for over-loaded threadpool
       
        # clear the source memeory  
        self.transcribeSignal.clearSourceMemory.connect(self.gb.clear_source_memory)
        # view handler to redirect to different pages based on the 
        # transcribe result 
        self.signal.start.connect(view.showTranscribeInProgress)
        self.signal.finish.connect(view.showTranscribeSuccess)
        
        # view handler to show transcription status
        self.signal.progress.connect(view.showFilesTranscriptionProgress)
        
        # view handler for transcription field 
        self.signal.error.connect(view.showErr)
        
        

    def runGailBot(self, transcribeRequest:Request):
        # pass 
        """ function to run gailbot on a separate thread """
        self.logger.info(f"active thread numbers : {self.ThreadPool.activeThreadCount()}")
        if self.ThreadPool.activeThreadCount() >= ThreadControl.maxThread:
            self.signal.busy.emit()
            self.logger.warn("threadpool busy")
        else:
            try:
                self.ThreadPool.clear()
                self.logger.info(f"the files to be transcribed are :{transcribeRequest.data}")
                self.worker = GBWorker(
                    transcribeRequest.data,  
                    transcribeRequest.succeed,
                    transcribeRequest.fail,
                    self.signal, self.gb)
                self.signal.start.emit()
                assert self.ThreadPool.tryStart(self.worker)
            except Exception as e:
                self.signal.error.emit(ERR.FAIL_START_TRANSCRIBE(str(e)))
                self.logger.error(f"failed to start transcribe due to error {e}", exc_info=e)


class GBWorker(QRunnable):
    def __init__(self, 
                 files: List[Tuple[str, Dict[str, str]]], 
                 continuation: callable,
                 failure:callable,
                 signal: Signal, 
                 gb: GailBot) -> None:
        super().__init__()
        self.signal = signal
        self.killed = False
        
        self.filedata = dict() ## stores the file data 
        self.continueFun = continuation 
        self.failureFun = failure
        
        for file in files :
            name, data = file 
            self.filedata[name] = data 
            
        self.gb = gb
        self.logger = makeLogger()
        
    @pyqtSlot()
    def run(self):
        self.logger.info(f"start to transcribe the files {self.filedata}")
        # add the progress displayer to every file to be able to 
        # display progress message sent by gailbot
        try: 
            for name in self.filedata.keys():
                self.gb.add_progress_display(name, self.getProgressDisplayer(name))
        except Exception as e:
            self.logger.error(f"Failed to add progress displayer, get error {e}")
      
        try:
            self.signal.start.emit()
            self.logger.info("Transcribing")
            # get the transcription result
            invalid, fails = self.gb.transcribe(list(self.filedata.keys()))
            
            for filename, data in self.filedata.items():
                if filename in invalid or filename in fails:
                    self.filedata[filename]["Status"] = "Not Transcribed" ## add to variable
                else:
                    self.filedata[filename]["Status"] = "Transcribed"
            self.logger.info(f"the failure files are {fails}, the invalid files are {invalid}")
            if invalid and fails:
                self.signal.error.emit(ERR.INVALID_TRANSCRIBE.format(str(invalid)) +
                                "\n" + ERR.FAIL_TRANSCRIBE.format(str(fails)))
            elif fails:
                self.signal.error.emit(ERR.FAIL_TRANSCRIBE.format(str(fails)))
            elif invalid: 
                self.signal.error.emit(ERR.INVALID_TRANSCRIBE.format(str(invalid)))
            self.continueFun([(name, data) for name, data in self.filedata.items()])
        except Exception as e:
            self.signal.error.emit(ERR.ERROR_WHEN_DUETO.format("transcription", str(e)))
            self.logger.error(f"Error during transcription: {e}", exc_info=e)
            self.continueFun([(name, data) for name, data in self.filedata.items()])
        finally:
            self.signal.finish.emit()
            self.setAutoDelete(True)
    
    def kill(self):
        """ public function to kill current running thread, the thread 
            will terminates after finishing the last function call 
        """
        self.logger.info("received request to cancel the thread")
        try:
            self.killed = True
            self.signal.killed.emit()
        except Exception as e:
            self.logger.error(f"Error while killing  the thread {e}", exc_info=e)
            self.signal.error(ERR.ERROR_WHEN_DUETO.format("cancelling thread", str(e)))

    def getProgressDisplayer(self, name):
        """private function to emit file progress
        Arg: 
            name: the name that can be used to identify the transcription 
        """
        return lambda msg : self.signal.progress.emit((name, msg))
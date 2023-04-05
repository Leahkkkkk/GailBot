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
import time
from typing import List, Dict
from controller.util.Error import  ERR
from view.MainWindow import MainWindow
from view import ViewController
from gbLogger import makeLogger
from PyQt6.QtCore import pyqtSignal, QObject, QThreadPool, QRunnable, pyqtSlot
from gailbot.api import GailBot

@dataclass 
class ThreadControl:
    maxThread = 5 
    
@dataclass 
class TranscribeError:
    INVALID_FILES = "The following files are not valid input {files}"    
    
class Signal(QObject):
    """ a signal object to communicate the transcription process with 
        the front end view object 
    """
    start = pyqtSignal()
    finish = pyqtSignal()
    fileTranscribed = pyqtSignal(str)
    error = pyqtSignal(str)
    busy = pyqtSignal()
    progress = pyqtSignal(tuple)
    killed = pyqtSignal()

class TranscribeController(QObject):
    def __init__(self, ThreadPool: QThreadPool, view: ViewController, gb: GailBot):
        """ a controller that controls the transcription process

        Constructor Args:
            ThreadPool (QThreadPool): a threadpool provided by the parent 
            view (ViewController): view object that handle the signal from the 
                               backend
            files (list): a list of files to be transcribed
        
        Field:
            1. ThreadPool: a threadpool where the function will be run 
            2. Signal: contains pyqtSignal to communicate with the caller 
            3. files: a list of files to be transcribed 
        
        Public function:
            1. runGailbot(): wrapper function to run gailbot
            2. cancelGailBot(): cancel the gailbot running process
        """
        super().__init__()
        self.logger = makeLogger ("B")
        self.logger.info("initialize the transcribe controller")
        self.ThreadPool = ThreadPool
        self.signal = Signal()
        self.gb = gb
        # connect to view handler for over-loaded threadpool
        self.signal.busy.connect(view.busyThreadWarning)
        
        # view handler to redirect to different pages based on the 
        # transcribe result 
        self.signal.start.connect(view.showTranscribeInProgress)
        self.signal.finish.connect(view.showTranscribeSuccess)
        self.signal.killed.connect(view.showFileUploadPage)
        
        # view handler to show transcription status
        self.signal.progress.connect(view.showFilesTranscriptionProgress)
        
        # view handler for transcription field 
        self.signal.error.connect(view.showErr)
        
        # view handler for change file display when transcription succeed
        self.signal.fileTranscribed.connect(view.changeFileToTranscribed)
        
        # handle view request to cancel gailbot
        view.getFileSignal().cancel.connect(self.cancelGailBot)

    def runGailBot(self, files: Dict[str, str]):
        # pass 
        """ function to run gailbot on a separate thread """
        self.logger.info(f"active thread numbers : {self.ThreadPool.activeThreadCount()}")
        if self.ThreadPool.activeThreadCount() >= ThreadControl.maxThread:
            self.signal.busy.emit()
            self.logger.warn("threadpool busy")
        else:
            try:
                self.ThreadPool.clear()
                self.logger.info(f"the files to be transcribeda are :{files}")
                self.worker = GBWorker(files, self.signal, self.gb)
                self.signal.start.emit()
                assert self.ThreadPool.tryStart(self.worker)
            except Exception as e:
                self.signal.error.emit(ERR.ERROR_WHEN_DUETO("transcribing file", str(e)))
                self.logger.error(f"failed to start transcribe due to error {e}", exc_info=e)

    def cancelGailBot(self):
        """ handler for user's request to cancel the gailbot """
        self.logger.info("receive request to cancel gailbot")
        try:
          if self.worker:
             self.worker.kill()
              
        except:
          self.signal.error.emit(ERR.ERROR_WHEN_DUETO("canceling transcription", str))
          self.logger.error("failed to cancel transcription")

class GBWorker(QRunnable):
    def __init__(self, files: List[str], signal: Signal, gb: GailBot) -> None:
        super().__init__()
        self.signal = signal
        self.killed = False
        self.files: List[str] = files 
        self.gb = gb
        self.logger = makeLogger("F")
        
    @pyqtSlot()
    def run(self):
        self.logger.info(f"start to transcribe the files {self.files}")
        # add the progress displayer to every file to be able to 
        # display progress message sent by gailbot
        try: 
            for file in self.files:
                self.gb.add_progress_display(file, self.getProgressDisplayer(file))
        except Exception as e:
            self.logger.error(f"Failed to add progress displayer, get error {e}")
      
        try:
            self.signal.start.emit()
            self.logger.info("Transcribing")
            # get the transcription result
            invalid, fails = self.gb.transcribe(list(self.files))
            self.logger.info(f"the failure files are {fails}, the invalid files are {invalid}")
            if invalid and fails:
                self.signal.error.emit(ERR.INVALID_FILE.format(str(invalid)) + "\n" + ERR.FAIL_TRANSCRIBE.format(str(fails)))
            elif fails:
                self.signal.error.emit(ERR.FAIL_TRANSCRIBE.format(str(fails)))
            elif invalid: 
                self.signal.error.emit(ERR.INVALID_FILE.format(str(invalid)))
        except Exception as e:
            self.signal.error.emit(ERR.ERROR_WHEN_DUETO.format("transcription", str(e)))
            self.logger.error(f"Error during transcription: {e}", exc_info=e)
            self.signal.finish.emit()
        else:
            if not self.killed:
                untranscribed = set(fails + invalid)
                if len(untranscribed):
                    self.logger.warn(f" following files are not transcribed {untranscribed}")
                for filename in self.files:
                    if not filename in untranscribed:
                        self.signal.fileTranscribed.emit(filename)
            time.sleep(0.2) 
            self.signal.finish.emit()
        finally:
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

    def getProgressDisplayer(self, file):
        """private function to emit file progress
        Args:
            file (_type_): _description_
            msg (_type_): _description_
        """
        return lambda msg : self.signal.progress.emit((file, msg))
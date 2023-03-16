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
from typing import List, Dict
from controller.util.Error import ErrorMsg, ThreadException, ErrorFormatter
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
    progress = pyqtSignal(str)
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
        self.signal.progress.connect(view.showStatusMsg)
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
                if not self.ThreadPool.tryStart(self.worker):
                    raise ThreadException(ErrorMsg.RESOURCEERROR)
            except Exception as e:
                self.signal.error.emit("failed to start transcription")
                self.logger.error(f"failed to start transcribe due to error {e}", exc_info=e)


    def cancelGailBot(self):
        """ handler for user's request to cancel the gailbot """
        self.logger.info("receive request to cancel gailbot")
        try:
          if self.worker:
             self.worker.kill()
              
        except:
          self.signal.error.emit("failed to cancel gailbot")
          self.logger.error("failed to cancel transcription")

class GBWorker(QRunnable):
    def __init__(self, files: Dict [str, str], signal: Signal, gb: GailBot) -> None:
        super().__init__()
        self.signal = signal
        self.killed = False
        self.files: Dict[str, str] = files 
        self.gb = gb
        self.logger = makeLogger("F")
        
    @pyqtSlot()
    def run(self):
        self.logger.info(f"start to transcribe the files {self.files}")
        try:
            self.signal.start.emit()
            self.signal.progress.emit("Transcribing")
            self.logger.info("Transcribing")
            result, invalid = self.gb.transcribe(list(self.files.values()))
            self.logger.info(f"the transcription result is {result}")
            self.logger.info(f"the invalid files are {invalid}")
            assert result
            if len(invalid) != 0:
                invalidFiles = str(invalid)
                self.signal.error.emit(
                    TranscribeError.INVALID_FILES.format(files=invalidFiles))
        except Exception as e:
            self.signal.error.emit(ErrorFormatter.DEFAULT_ERROR.format(
                source="transcription", msg=e))
            self.logger.error(f"Error during transcription: {e}", exc_info=e)
            self.signal.finish.emit()
        else:
            if not self.killed:
                for key, filename in self.files.items():
                    if not filename in invalid:
                        self.signal.fileTranscribed.emit(key)
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
            self.signal.error("The task cannot been cancelled")

            
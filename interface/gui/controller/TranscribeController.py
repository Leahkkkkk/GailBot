'''
File: TranscribeController.py
Project: GailBot GUI
File Created: Tuesday, 1st November 2022 7:40:56 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Tuesday, 1st November 2022 7:41:01 pm
Modified By:  Siara Small  & Vivian Li
-----
'''
from util.Error import ErrorMsg, ThreadExeceptiom
from view.MainWindow import MainWindow
from controller.Thread.GBRunnable import Worker
from util.Logger import makeLogger
from PyQt6.QtCore import pyqtSignal, QObject, QThreadPool, pyqtSlot



class Signal(QObject):
    """ a signal object that  """
    start = pyqtSignal()
    finish = pyqtSignal()
    fileTranscribed = pyqtSignal(str)
    error = pyqtSignal(str)
    busy = pyqtSignal()
    progress = pyqtSignal(str)
    killed = pyqtSignal()


class TranscribeController(QObject):
    def __init__(self, ThreadPool: QThreadPool, view: MainWindow, files:list):
        """ a controller that controls the transcription processs 

        Args:
            ThreadPool (QThreadPool): a threadpool provided by the parent 
            view (MainWindow): view object that handle the signal from the 
                               backend
            files (list): a list of files to be transcribed
        """
        super().__init__()
        self.logger = makeLogger ("B")
        self.logger.info("initialize the transcribe controller")
        self.ThreadPool = ThreadPool
        self.signal = Signal()
        self.files = files
        # connect to view handler for over-loaded threadpool
        self.signal.busy.connect(view.busyThreadPool)
        
        # view handler to redirect to different pages based on the 
        # transcibe result 
        self.signal.start.connect(view.showTranscribeInProgress)
        self.signal.finish.connect(view.showTranscribeSuccess)
        self.signal.killed.connect(view.showFileUploadPage)
        
        # view handler to show transcribtion status
        self.signal.progress.connect(view.showStatusMsg)
        self.signal.progress.connect(view.showFileProgress)
        
        # view handler for transcription fialed 
        self.signal.error.connect(view.TranscribeFailed)
        
        # view handler for change file display when transcription succeed
        self.signal.fileTranscribed.connect(view.changeFiletoTranscribed)
        
        # handle view request to cancle gailbot
        view.fileTableSignals.cancel.connect(self.cancelGailBot)

    def runGailBot(self):
        """ function to run gailbot on a separate thread """
        self.logger.info(self.ThreadPool.activeThreadCount())
        if self.ThreadPool.activeThreadCount() > 0:
            self.signal.busy.emit()
            self.logger.warn("threadpool busy")
        else:
            try:
                self.ThreadPool.clear()
                self.logger.info(self.files)
                self.worker = Worker(self.files, self.signal)
                self.signal.start.emit()
                if not self.ThreadPool.tryStart(self.worker):
                    raise ThreadExeceptiom(ErrorMsg.RESOURCEERROR)
            except:
                self.signal.error("failed to start transcribing")
                self.logger.error("failed to start transcribe")
    

    def cancelGailBot(self):
        """ handler for user's request to cancel the gailbot """
        self.logger.info("receive request to cancel gailbot")
        try:
          if self.worker:
             self.worker.kill()
              
        except:
          self.signal.error.emit("failed to cancel gailbot")
          self.logger.error("failed to cancel transcription")

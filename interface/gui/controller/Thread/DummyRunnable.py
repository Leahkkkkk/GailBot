""" implenmentation of Worker class 
a subclass of QRunnable class 
used to run a function on separte thread 
with the added feature of handling signals
"""
from PyQt6.QtCore import QRunnable, QObject, pyqtSlot, pyqtSignal
import logging
import time


class Signals(QObject):
    finished = pyqtSignal()
    start = pyqtSignal()
    progress = pyqtSignal(str)
    error = pyqtSignal(str)
    result = pyqtSignal()
    killed = pyqtSignal()

class Worker(QRunnable):
    def __init__(self):
        super(Worker, self).__init__()
        self.signals = Signals()
        self.is_killed = False

    @pyqtSlot()
    def run(self):
        try:
            self.signals.start.emit()
            for i in range(30):
                self.signals.progress.emit(str(i+1))
                time.sleep(0.3)

                if self.is_killed:
                    self.signals.killed.emit()
                    break
                
        except Exception as e:
            self.signals.error.emit(f"${e.__class__}fails" )
            time.sleep(5)
        else:
            self.signals.result.emit()
        finally:
            if not self.is_killed:
                self.signals.finished.emit()

    def kill(self):
        self.is_killed = True

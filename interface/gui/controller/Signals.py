from unittest import result
from PyQt6.QtCore import QThreadPool, pyqtSignal, QObject

class Signal(QObject):
    start = pyqtSignal()
    finish = pyqtSignal()
    error = pyqtSignal(str)
    busy = pyqtSignal()
    progress = pyqtSignal(str)
    killed = pyqtSignal()
    fileTranscribed = pyqtSignal(tuple)
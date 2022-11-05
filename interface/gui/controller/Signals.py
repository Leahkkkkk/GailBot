from PyQt6.QtCore import pyqtSignal, QObject

class Signal(QObject):
    start = pyqtSignal()
    finish = pyqtSignal()
    fileTranscribed = pyqtSignal(str)
    error = pyqtSignal(str)
    busy = pyqtSignal()
    progress = pyqtSignal(str)
    fileProgress = pyqtSignal(tuple)
    killed = pyqtSignal()

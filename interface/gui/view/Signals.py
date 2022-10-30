from inspect import getfile
from PyQt6.QtCore import QObject, pyqtSignal


class FileSignals(QObject):
    postFile = pyqtSignal(object)
    editFile = pyqtSignal(object)
    delete = pyqtSignal(object)
    getFile = pyqtSignal(str)
    transcribe = pyqtSignal(set)
    cancel = pyqtSignal()
    getFileToTranscribe = pyqtSignal(str)
    changeStatus = pyqtSignal(tuple)
    changeProfile = pyqtSignal(tuple)
    requestprofile = pyqtSignal(str)
    
class ProfileSignals(QObject):
    post = pyqtSignal(tuple)
    edit = pyqtSignal(tuple)
    get  = pyqtSignal(object)
    delete = pyqtSignal(object)
    addPlugin = pyqtSignal(tuple)

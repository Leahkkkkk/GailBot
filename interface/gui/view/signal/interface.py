'''
File: Signals.py
Project: GailBot GUI
File Created: Friday, 4th November 2022 1:01:27 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 10th November 2022 9:58:28 am
Modified By:  Siara Small  & Vivian Li
-----
Description: main siganls for view object to communicate with backend database
'''

from PyQt6.QtCore import QObject, pyqtSignal

class FileSignals(QObject):
    """ file signals for frontend to communicate with file database  """
    postFileRequest      = pyqtSignal(object)
    deleteRequest        = pyqtSignal(object)
    changeProfileRequest = pyqtSignal(object)
    requestprofile       = pyqtSignal(object)
    viewOutputRequest    = pyqtSignal(object)
    transcribe           = pyqtSignal(list)
    progressChanged      = pyqtSignal(tuple)
    cancel               = pyqtSignal()

class TranscribeSignal(QObject):
    transcribe = pyqtSignal(object)
    updateProgress = pyqtSignal(tuple)
    sendToConfirm = pyqtSignal(list)
    sendToTranscribe = pyqtSignal(list)
    sendToComplete = pyqtSignal(list)
    clearSourceMemory = pyqtSignal()

class ViewSignals(QObject):
    restart    = pyqtSignal()
    clearcache = pyqtSignal()
    
class StyleSignals(QObject):
    changeColor = pyqtSignal(str)
    changeFont  = pyqtSignal(str)

class DataSignal(QObject):
    editRequest    = pyqtSignal(object)
    getRequest     = pyqtSignal(object)
    deleteRequest  = pyqtSignal(object)
    postRequest    = pyqtSignal(object)
    
    viewSourceRequest = pyqtSignal(object)
    viewOutputRequest = pyqtSignal(object)
    
    
    detailRequest = pyqtSignal(object)
    fileProfileRequest = pyqtSignal(object)
    changeFileProfileRequest = pyqtSignal(object)
    
    deleteSucceed  = pyqtSignal(str)
    addSucceed     = pyqtSignal(str)
    editSucceed    = pyqtSignal(str)

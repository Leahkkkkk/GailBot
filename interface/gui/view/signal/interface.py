'''
File: Signals.py
Project: GailBot GUI
File Created: Friday, 4th November 2022 1:01:27 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 10th November 2022 9:58:28 am
Modified By:  Siara Small  & Vivian Li
-----
Description: main signal for view object to communicate with backend database
'''

import typing
from PyQt6.QtCore import QObject, pyqtSignal
class TranscribeSignal(QObject):
    """ 
    transcription signal for sending request for transcription
    """
    transcribe = pyqtSignal(object)
    updateProgress = pyqtSignal(tuple)
    sendToConfirm = pyqtSignal(list)
    sendToTranscribe = pyqtSignal(list)
    transcriptionComplete = pyqtSignal(list)
    clearSourceMemory = pyqtSignal()

class SystemSignal(QObject):
    """ 
    system signal 
    """
    restart    = pyqtSignal()
    clearcache = pyqtSignal()
    
class DataSignal(QObject):
    """ 
    include basic signals for querying backend data
    """
    editRequest       = pyqtSignal(object)
    getRequest        = pyqtSignal(object)
    deleteRequest     = pyqtSignal(object)
    postRequest       = pyqtSignal(object)
    viewSourceRequest = pyqtSignal(object)
    detailRequest     = pyqtSignal(object)
    getAllNameRequest = pyqtSignal(object)
    deleteSucceed     = pyqtSignal(str)
    addSucceed        = pyqtSignal(str)
    editSucceed       = pyqtSignal(str)
    
class FileDataSignal(DataSignal):
    """
    sub-class of DataSignal class for FileDataSignal, which adds
    two special signals for file data
    """
    viewOutputRequest        = pyqtSignal(object)
    changeFileProfileRequest = pyqtSignal(object)
    fileProfileRequest       = pyqtSignal(object)
    def __init__(self):
        super().__init__()
        
class StyleSignals(QObject):
    """
    Style Signal for controlling color and fontSize changes 
    """
    changeColor = pyqtSignal(str)
    changeFont  = pyqtSignal(str)
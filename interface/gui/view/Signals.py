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
    postFile = pyqtSignal(object)
    editFile = pyqtSignal(object)
    delete = pyqtSignal(object)
    getFile = pyqtSignal(str)
    transcribe = pyqtSignal(set)
    cancel = pyqtSignal()
    getFileToTranscribe = pyqtSignal(str)
    changeProfile = pyqtSignal(tuple)
    requestprofile = pyqtSignal(str)
    progressChanged = pyqtSignal(tuple)
    
class ProfileSignals(QObject):
    """ profile signals for front end to communicate with profile database"""
    editRequest   = pyqtSignal(object)
    getRequest    = pyqtSignal(object)
    deleteRequest = pyqtSignal(object)
    postRequest   = pyqtSignal(object)
    profileAdded  = pyqtSignal(str)

class PluginSignals(QObject):
    addRequest = pyqtSignal(object)
    detailRequest = pyqtSignal(object)
    deleteRequest = pyqtSignal(object)
    addPlugin = pyqtSignal(str)
    pluginAdded = pyqtSignal(str)
    pluginDeleted = pyqtSignal(str)
    updatePlugin = pyqtSignal(str)

class ViewSignals(QObject):
    restart = pyqtSignal()
    clearcache = pyqtSignal()
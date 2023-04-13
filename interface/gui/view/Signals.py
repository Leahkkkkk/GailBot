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
    viewOutput           = pyqtSignal(object)
    transcribe           = pyqtSignal(list)
    progressChanged      = pyqtSignal(tuple)
    cancel               = pyqtSignal()

    # signal for controlling view only
class ProfileSignals(QObject):
    """ profile signals for front end to communicate with profile database"""
    editRequest    = pyqtSignal(object)
    getRequest     = pyqtSignal(object)
    deleteRequest  = pyqtSignal(object)
    postRequest    = pyqtSignal(object)
    profileAdded   = pyqtSignal(str)
    profileDeleted = pyqtSignal(str)

class PluginSignals(QObject):
    addRequest    = pyqtSignal(object)
    detailRequest = pyqtSignal(object)
    deleteRequest = pyqtSignal(object)
    viewSource    = pyqtSignal(object)
    addPlugin     = pyqtSignal(str)
    pluginAdded   = pyqtSignal(str)
    pluginDeleted = pyqtSignal(str)
    updatePlugin  = pyqtSignal(str)

class ViewSignals(QObject):
    restart    = pyqtSignal()
    clearcache = pyqtSignal()

class StyleSignals(QObject):
    changeColor = pyqtSignal(str)
    changeFont  = pyqtSignal(str)

GlobalStyleSignal = StyleSignals()
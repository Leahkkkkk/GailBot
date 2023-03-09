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
    progressChanged = pyqtSignal(str)
    
class ProfileSignals(QObject):
    """ profile signals for front end to communicate with profile database"""
    post = pyqtSignal(tuple)
    edit = pyqtSignal(tuple)
    get  = pyqtSignal(object)
    delete = pyqtSignal(str)
    addPlugin = pyqtSignal(tuple)

class ViewSignals(QObject):
    restart = pyqtSignal()
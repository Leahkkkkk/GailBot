'''
File: Signals.py
Project: GailBot GUI
File Created: Friday, 4th November 2022 1:01:27 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Saturday, 5th November 2022 2:05:03 pm
Modified By:  Siara Small  & Vivian Li
-----
'''

from PyQt6.QtCore import pyqtSignal, QObject

class Signal(QObject):
    """ a signal object that contains signal for communication between 
        backend transcription process and frontend view object"""
    start = pyqtSignal()
    finish = pyqtSignal()
    fileTranscribed = pyqtSignal(str)
    error = pyqtSignal(str)
    busy = pyqtSignal()
    progress = pyqtSignal(str)
    fileProgress = pyqtSignal(tuple)
    killed = pyqtSignal()
    restart = pyqtSignal()

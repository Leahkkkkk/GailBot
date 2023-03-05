'''
File: DummyRunnable.py
Project: GailBot GUI
File Created: Wednesday, 25th September 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Wednesday, 5th October 2022 5:04:05 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: using time.sleep to run a fake backend function , for testing 
             purpose only 
'''
import time
from config.GailBotData import  getWorkPath
from typing import Dict

from PyQt6.QtCore import (
    QRunnable, 
    QObject, 
    pyqtSlot, 
    pyqtSignal)


class Signals(QObject):
    """ contain signals in order for QRunnable object to communicate
        with controller
    """
    finish = pyqtSignal()
    start = pyqtSignal()
    progress = pyqtSignal(str)
    error = pyqtSignal(str)
    killed = pyqtSignal()

class Worker(QRunnable):
    """  contain dummy function that is able to run on a separate thread 
    """
    def __init__(self, files: Dict [str, str], signals: Signals, gb = None):
        super(Worker, self).__init__()
        self.signals = signals
        self.files = files
        self.is_killed = False

    @pyqtSlot()
    def run(self):
        """ public function to execute the dummy function """
        try:
            workPath = getWorkPath()
            WORKSPACE_DIRECTORY_PATH = workPath.workSpace
            PLUGIN_DOWNLOAD_DIRECORY = workPath.plugin
            self.signals.progress.emit(WORKSPACE_DIRECTORY_PATH)
            time.sleep(2)
            self.signals.progress.emit(PLUGIN_DOWNLOAD_DIRECORY)
            time.sleep(2)

            self.signals.start.emit()
            for i in range(10):
                self.signals.progress.emit(str(i+1))
                time.sleep(0.2)

                if self.is_killed:
                    self.signals.killed.emit()
                    break
                
        except Exception as e:
            self.signals.error.emit(f"${e.__class__}fails" )
            time.sleep(5)
        else:
            self.signals.finish.emit()
    
        finally:
            if not self.is_killed:
                self.signals.finish.emit()

    def kill(self):
        """ kill the thread"""
        self.is_killed = True

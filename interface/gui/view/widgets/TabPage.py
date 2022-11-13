'''
File: TabPage.py
Project: GailBot GUI
File Created: Sunday, 23rd October 2022 10:39:27 am
Author: Siara Small  & Vivian Li
-----
Last Modified: Sunday, 23rd October 2022 10:40:25 am
Modified By:  Siara Small  & Vivian Li
-----
Description: Tab page widget with the signal to support functionalities for 
             control flow 
'''
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal, QObject


class Signals(QObject):
    """ contain signals to communicate with the parent tab widget """
    nextPage = pyqtSignal()
    goToNextPage = pyqtSignal()
    previousPage = pyqtSignal()
    close = pyqtSignal()
    
class TabPage(QWidget):
    """ the wrapper class for tab pages with signals to redirect pages """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.signals = Signals()

    
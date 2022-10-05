from PyQt6.QtWidgets import QWidget, QStatusBar
from PyQt6 import QtCore 
from util import Logger
import logging


class StatusBar(QStatusBar):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setMinimumSize(QtCore.QSize(900,40))
        self.statusLog = Logger.StatusBarHandler(self.showStatusMsg)
        logging.getLogger().addHandler(self.statusLog)
    
    def showStatusMsg(self, msg:str, time=None):
        self.setStyleSheet("color: black")
        if "WARN" in msg:
            self.setStyleSheet("color: orange")
        elif "ERROR" in msg:
            self.setStyleSheet("color: red")

        if time:
            self.showMessage(msg, time)
        else:
             self.showMessage(msg, 5000)
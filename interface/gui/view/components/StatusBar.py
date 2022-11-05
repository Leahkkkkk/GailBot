'''
File: StatusBar.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 10:26:36 am
Modified By:  Siara Small  & Vivian Li
-----
'''

import logging

from util import Logger
from util.Style import Dimension, StyleSheet
from PyQt6.QtCore import QSize 
from PyQt6.QtWidgets import  QStatusBar


class StatusBar(QStatusBar):
    """ A statusbar that display status message """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setMinimumSize(QSize(Dimension.STATUSWIDTH, Dimension.STATUSHEIGHT))
        self.statusLog = Logger.StatusBarHandler(self.showStatusMsg)
        logging.getLogger().addHandler(self.statusLog)
    
    def showStatusMsg(self, msg:str, time=None):
        """ Public function to display message on statusbar

        Args:
            msg (str): the message to be displayed 
            time (int, optional): the amount of time the message last 
                                  Defaults to None.
        """
        self.setStyleSheet(StyleSheet.statusText)
        if "WARN" in msg:
            self.setStyleSheet(StyleSheet.warnText)
        elif "ERROR" in msg:
            self.setStyleSheet(StyleSheet.errorText)

        if time:
            self.showMessage(msg, time)
        else:
             self.showMessage(msg, 2000)
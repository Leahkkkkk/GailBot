'''
File: Console.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 9:54:20 am
Modified By:  Siara Small  & Vivian Li
-----
Description: implementation of a console that display logging message 
'''
import logging

from util.Style import Dimension
from util.Text import WindowTitle

from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout,
    QLabel, 
    QPlainTextEdit
)
from PyQt6.QtCore import QSize


class Console(QWidget):
    """ A console window that display all log messages """
    def __init__(self):
        super().__init__()
        self.LogBox = QPlainTextEdit()
        self.LogBox.setReadOnly(True)
        logging.getLogger().setLevel(logging.DEBUG)
        self.resize(QSize(Dimension.CONSOLEWIDTH, Dimension.CONSOLEHEIGHT))

        self.label = QLabel(WindowTitle.consoleWindow)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.LogBox)
        self.setLayout(layout)
        
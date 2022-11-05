'''
File: Console.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 9:54:20 am
Modified By:  Siara Small  & Vivian Li
-----
'''
import logging

from util import Logger
from view.style.styleValues import Dimension, Geometry
from util.Config import WindowTitle

from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout,
    QLabel, 
    QPlainTextEdit
)

class Console(QWidget):
    """ A console window that display all log messages """
    def __init__(self):
        super().__init__()
        self.LogBox = QPlainTextEdit()
        self.LogBox.setReadOnly(True)
        self.LogHandler = Logger.ConsoleHandler(self.LogBox)
        
        logging.getLogger().addHandler(self.LogHandler)
        logging.getLogger().setLevel(logging.DEBUG)
        self.resize(Dimension.CONSOLE)
        self.setGeometry(Geometry.CONSOLE)

        self.label = QLabel(WindowTitle.consoleWindow)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.LogBox)
        self.setLayout(layout)
        
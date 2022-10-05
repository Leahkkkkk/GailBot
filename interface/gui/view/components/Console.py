# Console.py 
# implementation of console window 
#
from asyncio.subprocess import DEVNULL
from distutils.debug import DEBUG
from distutils.log import ERROR, INFO, WARN
from PyQt6.QtWidgets import *
import logging
from util import Logger

class Console(QWidget):
    def __init__(self):
        super().__init__()
        self.LogBox = QPlainTextEdit()
        self.LogBox.setReadOnly(True)
        self.LogHandler = Logger.ConsoleHandler(self.LogBox)
        
        logging.getLogger().addHandler(self.LogHandler)
        logging.getLogger().setLevel(logging.DEBUG)
        self.resize(1000,300)
        self.setGeometry(300, 700, 1000,300)
        # self.setStyleSheet("background-color: black;")


        # setting the layout of the console window
        # TODO: change the layout 
        self.label = QLabel("Console Window")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.LogBox)
        self.setLayout(layout)
        
'''
File: MenuBar.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 10:17:30 am
Modified By:  Siara Small  & Vivian Li
-----
'''
from view.style.styleValues import Geometry

from PyQt6.QtWidgets import QMenuBar, QMenu
from PyQt6 import QtCore, QtGui


class ManuBar(QMenuBar):
    """ Gui menu bar, include open and close console option """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setGeometry(Geometry.MENUBAR)
        self.Console = QMenu("Console")
        self.OpenConsole = QtGui.QAction("Open")
        self.Console.addAction(self.OpenConsole)
        self.CloseConsole = QtGui.QAction("Close")
        self.Console.addAction(self.CloseConsole)
        self.addAction(self.Console.menuAction())
        
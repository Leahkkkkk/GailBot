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
from util.Text import MenuBarText

from PyQt6.QtWidgets import QMenuBar, QMenu
from PyQt6 import QtGui


class ManuBar(QMenuBar):
    """ Gui menu bar, include open and close console option """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.Console = QMenu(MenuBarText.console)
        self.OpenConsole = QtGui.QAction(MenuBarText.open)
        self.Console.addAction(self.OpenConsole)
        self.CloseConsole = QtGui.QAction(MenuBarText.close)
        self.Console.addAction(self.CloseConsole)
        self.addAction(self.Console.menuAction())
        
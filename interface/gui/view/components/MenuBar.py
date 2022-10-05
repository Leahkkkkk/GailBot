from PyQt6.QtWidgets import QMenuBar, QMenu
from PyQt6 import QtCore, QtGui


class ManuBar(QMenuBar):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setGeometry(QtCore.QRect(0, 0, 900, 37))
        self.Console = QMenu("Console")
        self.OpenConsole = QtGui.QAction("Open")
        self.Console.addAction(self.OpenConsole)
        self.CloseConsole = QtGui.QAction("Close")
        self.Console.addAction(self.CloseConsole)
        self.addAction(self.Console.menuAction())
        
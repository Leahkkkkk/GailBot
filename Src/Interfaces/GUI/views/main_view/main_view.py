# Standard imports

# Local imports
from .main_vew_ui import Ui_MainWindow
# Third party imports
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot

class MainView(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        # Adding the MainView
        self._main_ui = Ui_MainWindow()
        self._main_ui.setupUi(self)
        s = self._main_ui.centralwidget.findChild(QtWidgets.QPushButton,"startButton")
        print(s)

    ####################### MODIFIERS ################################

    def show_transcription_screen(self) -> None:
        print("Switching to transcription screen")




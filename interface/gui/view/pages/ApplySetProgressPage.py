from PyQt6.QtWidgets import *
from PyQt6 import QtCore

""" Class for apply settings in progress page """
class ApplySetProgressPage(QWidget):
    """ initialize class """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._initWidget()
        self._initLayout()
    """ initialize widget """
    def _initWidget(self):
        self.label = QLabel("Apply Settings in Progress")
    """ initialize vertical layout """
    def _initLayout(self):
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addWidget(self.label)
        

    
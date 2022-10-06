'''
File: ApplySetSuccessPage.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 11:05:10 am
Modified By:  Siara Small  & Vivian Li
-----
'''
from view.style import Background
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class ApplySetSuccessPage(QWidget):
    """ apply settings successful page """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._initWidget()
        self._initLayout()
        self._initStyle()
    def _initWidget(self):
        """ initialize widget """
        self.label = QLabel("Apply Settings Successful")
    
    def _initLayout(self):
        """ initalize layout """
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addWidget(self.label)
    
    def _initStyle(self):
        """ initalize style """   
        Background.initBackground(self)

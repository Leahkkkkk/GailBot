'''
File: ApplySetProgressPage.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 11:04:03 am
Modified By:  Siara Small  & Vivian Li
-----
'''

from view.widgets import Label, Button
from view.style.styleValues import Color, FontSize, FontFamily
from view.style import Background

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea
from PyQt6.QtCore import Qt


class ApplySetProgressPage(QWidget):
    """ apply settings in progress page """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._initWidget()
        self._initLayout()
        self._initStyle()
    
    def _initWidget(self):
        """ initialize widget """
        self.label = Label.Label("Apply Settings in Progress", 
                                 FontSize.HEADER2, 
                                 FontFamily.MAIN)
        self.Formatting = QLabel("Formatting file headers")
        self.Formatting.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.InProgress = QLabel("Files in progress:")
        self.InProgress.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.cancelBtn = Button.ColoredBtn("Cancel", Color.ORANGE, FontSize.BTN)
        
    def _initLayout(self):
        """ initialize vertical layout """
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.Formatting)
        self.verticalLayout.addWidget(self.InProgress)
        self.verticalLayout.addWidget(self.cancelBtn, 4, 
                                      alignment = Qt.AlignmentFlag.AlignHCenter)
        

    def _initStyle(self):
        """ initialize style """
        Background.initBackground(self)
        

    
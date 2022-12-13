'''
File: ScrollArea.py
Project: GailBot GUI
File Created: Saturday, 10th December 2022 2:34:51 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Saturday, 10th December 2022 2:37:32 pm
Modified By:  Siara Small  & Vivian Li
-----
'''

from util.Style import Dimension, Color
from PyQt6.QtWidgets import QScrollArea 
from PyQt6.QtCore import QSize

class ScrollArea(QScrollArea):
    """ a customized QComboBox Widget """
    def __init__(self, *args, **kwargs) -> None:
        """ initializes widget """
        super().__init__(*args, **kwargs)
        self.verticalScrollBar().setStyleSheet(
            f"background-color:{Color.SCORLL_BAR};"
            f"border: 1px {Color.MAIN_BACKRGOUND} solid")
        self.horizontalScrollBar().setStyleSheet(
            f"background-color:{Color.SCORLL_BAR};"
            f"border: 1px {Color.MAIN_BACKRGOUND} solid")
        self.setWidgetResizable(True)
        

        
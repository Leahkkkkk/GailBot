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

from view.style.WidgetStyleSheet import SCROLL_BAR
from PyQt6.QtWidgets import QScrollArea 
from PyQt6.QtCore import QSize, Qt

class ScrollArea(QScrollArea):
    """ a customized QComboBox Widget """
    def __init__(self, *args, **kwargs) -> None:
        """ initializes widget """
        super().__init__(*args, **kwargs)
        self.verticalScrollBar().setStyleSheet(SCROLL_BAR)
        self.horizontalScrollBar().setStyleSheet(SCROLL_BAR)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        

        
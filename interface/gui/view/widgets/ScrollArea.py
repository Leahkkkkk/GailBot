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

from view.Signals import GlobalStyleSignal
from view.config.Style import STYLE_DICT, StyleSheet
from view.Signals import GlobalStyleSignal
from PyQt6.QtWidgets import QScrollArea 
from PyQt6.QtCore import QSize, Qt

SCROLLBAR = StyleSheet.SCROLL_BAR
def changecolor(colormode):
    global SCROLLBAR
    SCROLLBAR = STYLE_DICT[colormode].SCROLL_BAR

GlobalStyleSignal.changeColor.connect(changecolor)
class ScrollArea(QScrollArea):
    """ a customized QComboBox Widget """
    def __init__(self, *args, **kwargs) -> None:
        """ initializes widget """
        super().__init__(*args, **kwargs)
        self.verticalScrollBar().setStyleSheet(SCROLLBAR)
        self.horizontalScrollBar().setStyleSheet(SCROLLBAR)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        GlobalStyleSignal.changeColor.connect(self.colorchange)
    
    def colorchange(self, colormode):
        self.verticalScrollBar().setStyleSheet(STYLE_DICT[colormode].SCROLL_BAR)
        self.horizontalScrollBar().setStyleSheet(STYLE_DICT[colormode].SCROLL_BAR)

        
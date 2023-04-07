'''
File: ComboBox.py
Project: GailBot GUI
File Created: Tuesday, 18th October 2022 6:21:46 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Sunday, 30th October 2022 12:18:56 pm
Modified By:  Siara Small  & Vivian Li
-----
'''
from view.Signals import GlobalStyleSignal
from ..config.Style import Dimension, STYLE_DICT, StyleSheet
from PyQt6.QtWidgets import QComboBox 

class ComboBox(QComboBox):
    """ a customized QComboBox Widget """
    def __init__(self, *args, **kwargs) -> None:
        """ initializes widget """
        super().__init__(*args, **kwargs)
        self.setStyleSheet(StyleSheet.COMBO_BOX)
        self.setFixedHeight(Dimension.COMBOBOX_HEIGHT)
        GlobalStyleSignal.changeColor.connect(self.colorChange)
         
    def colorChange(self, colormode):
        self.setStyleSheet(STYLE_DICT[colormode].COMBO_BOX)
        
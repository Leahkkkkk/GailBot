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
from ..config.Style import STYLE_DATA
from PyQt6.QtWidgets import QComboBox 

class ComboBox(QComboBox):
    """ a customized QComboBox Widget """
    def __init__(self, *args, **kwargs) -> None:
        """ initializes widget """
        super().__init__(*args, **kwargs)
        self.setStyleSheet(STYLE_DATA.StyleSheet.COMBO_BOX)
        self.setFixedHeight(STYLE_DATA.Dimension.COMBOBOX_HEIGHT)
        self.setMinimumWidth(STYLE_DATA.Dimension.INPUTWIDTH)
        STYLE_DATA.signal.changeColor.connect(self.colorChange)
         
    def colorChange(self):
        self.setStyleSheet(STYLE_DATA.StyleSheet.COMBO_BOX)
        
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
from util.Style import Dimension, Color
from PyQt6.QtWidgets import QComboBox 
from PyQt6.QtCore import QSize

class ComboBox(QComboBox):
    """ a customized QComboBox Widget """
    def __init__(self, *args, **kwargs) -> None:
        """ initializes widget """
        super().__init__(*args, **kwargs)
        self.setStyleSheet("QComboBox {"
                           f"background-color: {Color.INPUT_BACKGROUND};"
                           f"color:{Color.INPUT_TEXT};"
                           f"border:1px solid {Color.INPUT_BORDER};"
                           f"padding: 3px 12px 3px 12px;"
                           f"border-radius: 7px;"
                           f"margin: 5px;"
                           "}"
                        )
        self.setFixedHeight(40)
        
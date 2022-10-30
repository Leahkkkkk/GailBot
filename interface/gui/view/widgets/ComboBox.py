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


from PyQt6.QtWidgets import QComboBox 
from PyQt6.QtCore import QSize

class ComboBox(QComboBox):
    """ a customized QComboBox Widget """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setStyleSheet("padding: 10px; font-size:14px")
        self.setContentsMargins(0,20,0,20)
        self.setFixedSize(QSize(170,50))
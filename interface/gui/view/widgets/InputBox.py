'''
File: InputBox.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 1:44:14 pm
Modified By:  Siara Small  & Vivian Li
-----
'''
from view.style.styleValues import (
    FontSize, 
    Dimension, 
    Color
)

from PyQt6.QtWidgets import (
    QLabel, 
    QWidget, 
    QHBoxLayout, 
    QLineEdit
)
from PyQt6.QtCore import QSize


class InputBox(QWidget):
    """ an input box widget

    Args: 
        label(str): the label of the input Field 
    """
    def __init__(self, label:str, *args, **kwargs) -> None:
        """initialize input box"""
        super().__init__(*args, **kwargs)
        self.label = label
        self._initWidget()
        self._initLayout()
        self._connectSignal()

    def value(self):
        """ public function to ge the value of the input """
        return self.InputFeild.text()
    
    def _initWidget(self):
        """initialize widgets for input box"""
        self.inputlabel = QLabel(self.label)
        self.inputFeild = InputField(self) 
        self.inputFeild.setMaximumSize(Dimension.INPUTFIELD)
    
    def _initLayout(self):
        """initialize layouts for input box"""
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)
        self.layout.addWidget(self.inputlabel) 
        self.layout.addWidget(self.inputFeild)
    
    def _connectSignal(self):
        """connect signal- dummy for now"""
        pass


class InputField(QLineEdit):
    """ the input field of input box"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setStyleSheet(f"font-size: {FontSize.TEXT_FIELD};"
                           f"padding:0;"
                           f"border: 1px solid {Color.BORDERGREY} ")
        self.setFixedSize(QSize(Dimension.INPUTFIELD_WIDTH, 
                                Dimension.INPUTFIELD_HEIGHT))
        
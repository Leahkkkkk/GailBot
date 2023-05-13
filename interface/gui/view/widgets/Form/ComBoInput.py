'''
File: ComBoInput.py
Project: GailBot GUI
File Created: Monday, 9th January 2023 12:01:32 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Monday, 9th January 2023 12:02:58 pm
Modified By:  Siara Small  & Vivian Li
-----
'''
from typing import List 

from .FormWidget import FormWidget
from ..Label import Label 
from ..ComboBox import ComboBox
from view.config.Style import STYLE_DATA
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

class InputCombo(QWidget, FormWidget):
    def __init__(self, 
                 selections: List[str], 
                 label: str, 
                 vertical: bool = False,
                 labelSize = STYLE_DATA.FontSize.BODY,
                 inputText = None, 
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.selections = selections 
        self.vertical = vertical
        self.label = label 
        self.labelSize = labelSize
        self.label = label.replace("_", " ").capitalize()
        self.inputText = inputText
        self.initUI()
        self.connectSignal()
    
    def initUI(self):
        """ 
        initializing ui
        """
        self.inputLabel = Label(self.label, self.labelSize)
        self.inputField = ComboBox()
        self.inputField.addItems(self.selections)
        
        if self.value:
            self.inputField.setCurrentText(self.value)
        
        self._layout = QVBoxLayout() if self.vertical else QHBoxLayout()
        self.setLayout(self._layout)
        self._layout.addWidget(self.inputLabel)
        self._layout.addStretch()
        self._layout.addWidget(self.inputField)
        self.setMinimumHeight(80)
        self.setFixedWidth(STYLE_DATA.Dimension.FORM_INPUT_WIDTH)
        self.setMinimumWidth(STYLE_DATA.Dimension.INPUTWIDTH)
    
    def connectSignal(self):
        """ 
        connect file signal
        """
        self.inputField.currentTextChanged.connect(self.updateValue)
        STYLE_DATA.signal.changeFont.connect(self.fontChange)
    
    def fontChange(self):
        self.inputLabel.fontChange(STYLE_DATA.FontSize.BODY)
        
    def setValue(self, value: str):
        """ 
        set the current value as value
        """
        self.inputField.setCurrentText(value)
        self.value = value 
    
    def getValue(self) -> str:
        """ return the user selection as a string 
        """
        return self.inputField.currentText()
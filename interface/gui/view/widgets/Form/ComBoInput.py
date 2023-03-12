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

from view.widgets.Form.FormWidget import FormWidget
from view.widgets import Label, ComboBox 
from view.config.Style import Color, FontSize
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

class InputCombo(QWidget, FormWidget):
    def __init__(self, 
                 selections: List[str], 
                 label: str, 
                 vertical: bool = False,
                 labelSize = FontSize.BODY,
                 inputText = None, 
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.selections = selections 
        self.vertical = vertical
        self.label = label 
        self.labelSize = labelSize
        self.inputText = inputText
        self.initUI()
        self.connectSignal()
    
    def initUI(self):
        super().initUI()
        self.inputLabel = Label.Label(self.label, self.labelSize)
        self.inputField = ComboBox.ComboBox()
        self.inputField.addItems(self.selections)
        
        if self.value:
            self.inputField.setCurrentText(self.value)
        
        self._layout = QVBoxLayout() if self.vertical else QHBoxLayout()
        self.setLayout(self._layout)
        self._layout.addWidget(self.inputLabel)
        self._layout.addWidget(self.inputField)
    
    def connectSignal(self):
        self.inputField.currentTextChanged.connect(self.updateValue)
        
        
    def setValue(self, value):
        self.inputField.setCurrentText(value)
        self.value = value 
    
    def getValue(self):
        return self.inputField.currentText()
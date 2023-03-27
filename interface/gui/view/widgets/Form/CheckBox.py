'''
File: CheckBox.py
Project: GailBot GUI
File Created: Thursday, 12th January 2023 1:24:08 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 12th January 2023 1:51:57 pm
Modified By:  Siara Small  & Vivian Li
-----
'''

from .FormWidget import FormWidget
from view.widgets.Label import Label
from view.config.Style import FontSize
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QCheckBox

class CheckBox(QWidget, FormWidget):
    def __init__(self, label:str, state = False, *args, **kwargs) -> None:
        super(CheckBox, self).__init__(*args, **kwargs)
        self.label = label 
        self.state = state 
        self.initUI()
        
    def initUI(self):
        self._layout = QHBoxLayout()
        self.checkBox = QCheckBox()
        self.pluginLabel = Label(self.label, FontSize.BODY)
        self.setLayout(self._layout)
        self._layout.addWidget(self.checkBox)
        self._layout.addWidget(self.pluginLabel)
        self._layout.setSpacing(20)
        self._layout.addStretch()
        self.checkBox.setChecked(self.state)
        self.setContentsMargins(0,0,0,0)
        self.setFixedHeight(50)
    
    def setValue(self, value: bool):
        self.checkBox.setChecked(value)
    
    def getValue(self):
        return self.checkBox.isChecked()
    
    def isChecked(self):
        return self.checkBox.isChecked()
   
    def enable(self):
        self.checkBox.setCheckable(True)
    
    def disable(self):
        self.checkBox.setCheckable(False)
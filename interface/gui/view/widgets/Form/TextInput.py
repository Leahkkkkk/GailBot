'''
File: TextInput.py
Project: GailBot GUI
File Created: Monday, 9th January 2023 9:57:42 am
Author: Siara Small  & Vivian Li
-----
Last Modified: Monday, 9th January 2023 12:02:32 pm
Modified By:  Siara Small  & Vivian Li
-----
'''

from .FormWidget import FormWidget
from ..Label import Label
from view.config.Style import STYLE_DATA
from view.Signals import GlobalStyleSignal
from copy import deepcopy

from PyQt6.QtWidgets import QLineEdit, QHBoxLayout, QVBoxLayout, QWidget
from PyQt6.QtCore import QSize

class InputField(QLineEdit, FormWidget):
    def __init__(self, 
                 width = STYLE_DATA.Dimension.INPUTWIDTH, 
                 height = STYLE_DATA.Dimension.INPUTHEIGHT, *args, **kwargs):
        super(InputField, self).__init__(*args, **kwargs)
        self.setFixedSize(QSize(width, height))
        self.setStyleSheet(STYLE_DATA.StyleSheet.INPUT_TEXT)
        
        STYLE_DATA.signal.changeColor.connect(self.colorchange)
        STYLE_DATA.signal.changeFont.connect(self.colorchange)
    
    def colorchange(self):
        self.setStyleSheet(STYLE_DATA.StyleSheet.INPUT_TEXT)
        
    
    def mouseDoubleClickEvent(self, a0) -> None:
        super().mouseDoubleClickEvent(a0)
        self.clear()
          
class TextInput(QWidget, FormWidget):
    def __init__(self,
                 label: str, 
                 labelSize = STYLE_DATA.FontSize.BODY, 
                 inputText = None,
                 vertical = False,
                 width = STYLE_DATA.Dimension.INPUTWIDTH,
                 height = STYLE_DATA.Dimension.INPUTHEIGHT,
                 *args, **kwargs) -> None:
        super(TextInput, self).__init__(*args, **kwargs)
        self.label = deepcopy(label)
        self.label = self.label.replace("_", " ").capitalize()
        self.vertical = vertical
        self.labelSize = labelSize
        self.value = inputText
        self._width = width
        self._height = height 
        self.initUI()
        self.connectSignal()
        
    def initUI(self):
        self.inputLabel = Label(self.label, self.labelSize)
        self.inputField = InputField(self._width, self._height)
        if self.value:
            self.inputField.setText(str(self.value))
        self._layout = QHBoxLayout() 
        self.setLayout(self._layout)
        self._layout.addWidget(self.inputLabel)
        self._layout.addWidget(self.inputField)
        
    def connectSignal(self):
        self.inputField.textChanged.connect(self.updateValue)
        STYLE_DATA.signal.changeFont.connect(self.fontchange)

    def setValue(self, value):
        self.value = value 
        self.inputField.setText(str(value))
    
    def getValue(self):
        return self.inputField.text()
    
    def fontchange(self):
        self.inputLabel.fontChange(STYLE_DATA.FontSize.BODY)
    
from view.widgets import Label, InputBox, Button
from view.style.styleValues import FontFamily, FontSize, Color
from view.style import Background

from PyQt6.QtWidgets import (
    QWidget, 
    QLabel, 
    QVBoxLayout, 
    QSpacerItem,
    QSizePolicy,
    QScrollArea,
    QComboBox
)

from PyQt6.QtCore import Qt, QSize

""" TODO: create functions to load the form values
    TODO: create functions to disable editing 
    TODO: create functiosn to retrieve form data
"""
class TextForm(QWidget):
    """ required settings page"""
    def __init__(self, data, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.data = data
        self.inputDict = dict()
        self._initWidget()
        self._initStyle()

    
    def _initWidget(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(0)
 
        for key, items in self.data.items():
            newLabel = Label.Label(key, FontSize.BTN, FontFamily.MAIN)
            self.layout.addWidget(newLabel)
            for key,value in items.items():
                keyCopy = key
                if "bool" in key:
                    key = key.replace("bool", "")
                    newInput = Button.onOffButton(key, value=="ON")
                if "combo" in key:
                    key = key.replace("combo","")
                    newInput = InputBox.InputCombo(label=key, selections=value)
                else:
                    newInput = InputBox.InputBox(key, inputText=value)
                newInput.setContentsMargins(25,5,15,0)
                self.layout.addWidget(newInput)
                self.inputDict[keyCopy] = newInput
            spacer = QSpacerItem(400, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            self.layout.addItem(spacer)

    def getValue(self) -> dict:
        value = dict()
        for key, input in self.inputDict.items():
            value[key] = input.value()
        return value
            
    def _initStyle(self):
        Background.initBackground(self, Color.BLUEWHITE)
    
    def updateValues(self, data:dict):
        for key, input in self.inputDict.items():
            input.setText(data[key])
        
    

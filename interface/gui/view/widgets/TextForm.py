from view.widgets import Label, InputBox, Button
from view.style.styleValues import FontFamily, FontSize, Color
from view.style.Background import initBackground

from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout)


class TextForm(QWidget):
    """ required settings page"""
    def __init__(self, data, backgroundColor=Color.BLUEWHITE, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.data = data
        self.backgroundColor = backgroundColor 
        self.inputDict = dict()
        self._initWidget()
        self._initStyle()

    
    def _initWidget(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(10)
 
        for key, items in self.data.items():
            newLabel = Label.Label(key, FontSize.BTN, FontFamily.MAIN)
            self.layout.addWidget(newLabel)
            for key, value in items.items():
                keyCopy = key
                if "bool" in key:
                    key = key.replace("bool", "")
                    newInput = Button.onOffButton(key, value=="ON")
                elif "combo" in key:
                    key = key.replace("combo","")
                    newInput = InputBox.InputCombo(label=key, selections=value)
                else:
                    newInput = InputBox.InputBox(key, inputText=value)
                newInput.setContentsMargins(25,5,15,0)
                self.layout.addWidget(newInput)
                self.inputDict[keyCopy] = newInput
       

    def getValue(self) -> dict:
        value = dict()
        for key, input in self.inputDict.items():
            value[key] = input.value()
        return value
            
    def _initStyle(self):
        initBackground(self, self.backgroundColor)
    
    def updateValues(self, data:dict):
        for key, input in self.inputDict.items():
            input.setText(data[key])
        
    

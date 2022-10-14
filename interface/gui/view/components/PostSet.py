from view.widgets import Label, InputBox, Button
from view.style.styleValues import FontFamily, FontSize, Color
from view.style import Background

from PyQt6.QtWidgets import (
    QWidget, 
    QLabel, 
    QVBoxLayout, 
    QSpacerItem,
    QSizePolicy,
    QScrollArea
)

from PyQt6.QtCore import Qt, QSize

class PostSet(QWidget):
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
        self.layout.setContentsMargins(0,0,0,0)
 
        
        for key, items in self.data.items():
            newLabel = Label.Label(key, FontSize.BTN, FontFamily.MAIN)
            self.layout.addWidget(newLabel)
            for key,value in items.items():
                if "bool" in key:
                    key = key.replace("bool", "")
                    newInput = Button.onOffButton(key, value=="ON")
                else:
                    newInput = InputBox.InputBox(key, inputText=value)
                self.layout.addWidget(newInput)
                self.inputDict[key] = newInput
            spacer = QSpacerItem(400, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            self.layout.addItem(spacer)

        
        
    
    def _initStyle(self):
        # self.setObjectName("PostSet")
        # self.layout.setObjectName("Layout")
        # self.setStyleSheet( "#PostSet{{border: 1px solid #000; padding: 30px;}}")
        Background.initBackground(self, Color.BLUEWHITE)
    
    
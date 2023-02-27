from view.widgets.Form.FormWidget import FormWidget
from view.widgets import Label
from util.Style import Color, Dimension, FontFamily, FontSize
from util.Text import BtnText as Text 

from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout

class onOffButton(QWidget, FormWidget):
    def __init__(self, 
                label: str,
                state: str = "ON",   
                *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.label = label 
        self.value = state 
        self.initUI()
        self.connectSignal()
    
    def initUI(self):
        self.label = Label.Label(self.label, FontSize.BTN)
        if self.value or self.value.lower() == "on":
            self.onOffBtn = QPushButton(Text.on)
        else:
            self.onOffBtn = QPushButton(Text.off)
        self.onOffBtn.setMaximumSize(
            Dimension.ICONBTN, Dimension.ICONBTN
        )
        self._layout = QHBoxLayout()
        self.setLayout(self._layout)
        self._layout.addWidget(self.label)
        self._layout.addWidget(self.onOffBtn)
    
    def buttonClickHandler(self):
        if self.onOffBtn.text() == Text.on:
            self.onOffBtn.setText(Text.off)
            self.value = Text.off 
        else:
            self.onOffBtn.setText(Text.on)
            self.value = Text.on 
    
    def setValue(self, value):
        self.onOffBtn.setText(value)
        self.value = value 
        
    def getValue(self):
        return self.value
    
    def connectSignal(self):
        self.onOffBtn.clicked.connect(self.buttonClickHandler)
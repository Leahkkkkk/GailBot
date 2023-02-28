from view.widgets.Form.FormWidget import FormWidget
from view.widgets import Label
from util.Style import Color, Dimension, FontFamily, FontSize
from util.Text import BtnText as Text 

from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout

class onOffButton(QWidget, FormWidget):
    def __init__(self, 
                label: str,
                state: bool,   
                *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.label = label 
        self.value = state 
        self.initUI()
        self.connectSignal()
    
    def initUI(self):
        self.label = Label.Label(self.label, FontSize.BTN)
        if self.value == True:
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
            self.value = False
        else:
            self.onOffBtn.setText(Text.on)
            self.value = True
    
    def setValue(self, value):
        self.value = value 
        if value or value == "true":
            self.onOffBtn.setText(Text.on)
        else: 
            self.onOffBtn.setText(Text.off)
        
    def getValue(self):
        return self.value
    
    def connectSignal(self):
        self.onOffBtn.clicked.connect(self.buttonClickHandler)
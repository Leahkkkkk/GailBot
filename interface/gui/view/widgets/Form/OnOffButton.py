from view.widgets.Form.FormWidget import FormWidget
from view.widgets import Label
from config.Style import Color, Dimension, FontFamily, FontSize
from config.Text import BtnText as Text 

from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout

class onOffButton(QWidget, FormWidget):
    def __init__(self, 
                label: bool,
                state: bool = False,   
                *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.label = label 
        self.value = state 
        self.initUI()
        self.connectSignal()
    
    def initUI(self):
        self.label = Label.Label(self.label, FontSize.BTN)
        if self.value:
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
        if self.value:
            self.onOffBtn.setText(Text.off)
            self.value = False
        else:
            self.onOffBtn.setText(Text.on)
            self.value = True
    
    def setValue(self, value: bool):
        self.value = value 
        if value:
            self.onOffBtn.setText(Text.on)
        else: 
            self.onOffBtn.setText(Text.off)
        
    def getValue(self):
        return self.value
    
    def connectSignal(self):
        self.onOffBtn.clicked.connect(self.buttonClickHandler)
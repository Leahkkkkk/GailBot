from ..Label import Label
from view.config.Style import STYLE_DATA, Dimension
from view.config.Text import BtnText as Text 
from copy import deepcopy
from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout
from .FormWidget import FormWidget
class onOffButton(QWidget, FormWidget):
    def __init__(self, 
                label: str,
                state: bool = False,   
                *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.label = deepcopy(label)
        self.label = self.label.replace("_", " ").capitalize()
        self.value = state 
        self.initUI()
        self.connectSignal()
    
    def initUI(self):
        self.setFixedWidth(STYLE_DATA.Dimension.FORM_INPUT_WIDTH)
        self.label = Label(self.label, STYLE_DATA.FontSize.BTN)
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
        self._layout.addStretch()
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
        STYLE_DATA.signal.changeFont.connect(self.changeFont)

    def changeFont(self):
        self.label.fontChange(STYLE_DATA.FontSize.BTN)
'''
File: OnOffButton.py
Project: GailBot GUI
File Created: 2023/04/01
Author: Siara Small  & Vivian Li
-----
Last Modified:2023/05/23
Modified By:  Siara Small  & Vivian Li
-----
Description: implementation fo on and off button that change the text to 
             either on or off after being clicked 
'''
from ..Label import Label
from view.config.Style import STYLE_DATA, Dimension
from view.config.Text import BTN_TEXT as Text 
from copy import deepcopy
from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout
from .FormWidget import FormWidget
class onOffButton(QWidget, FormWidget):
    def __init__(self, 
                label: str,
                state: bool = False,   
                *args, **kwargs) -> None:
        """construct an instance of onOffButton

        Args:
            label (str): the text that will be displayed next to the button,
                         which describes the function of the button
            state (bool, optional): the initial state of the button. Defaults to False.
        """
        super().__init__(*args, **kwargs)
        self.label = deepcopy(label)
        self.label = self.label.replace("_", " ").capitalize()
        self.value = state 
        self.initUI()
        self.connectSignal()
    
    def initUI(self):
        """
        initialize the UI of the button
        """
        self.setFixedWidth(STYLE_DATA.Dimension.FORM_INPUT_WIDTH)
        self.label = Label(self.label, STYLE_DATA.FontSize.BTN)
        if self.value:
            self.onOffBtn = QPushButton(Text.ON)
        else:
            self.onOffBtn = QPushButton(Text.OFF)
        self.onOffBtn.setMaximumSize(
            Dimension.ICONBTN, Dimension.ICONBTN
        )
        self._layout = QHBoxLayout()
        self.setLayout(self._layout)
        self._layout.addWidget(self.label)
        self._layout.addStretch()
        self._layout.addWidget(self.onOffBtn)
    
    def buttonClickHandler(self):
        """
        change the state and the text on the button when being clicked  
        """
        if self.value:
            self.onOffBtn.setText(Text.OFF)
            self.value = False
        else:
            self.onOffBtn.setText(Text.ON)
            self.value = True
    
    def setValue(self, value: bool):
        """
        set the value of the function to be value 
        """
        self.value = value 
        if value:
            self.onOffBtn.setText(Text.ON)
        else: 
            self.onOffBtn.setText(Text.OFF)
        
    def getValue(self):
        """ 
        get the value of the button
        """
        return self.value
    
    def connectSignal(self):
        """ 
        connect the button's signal
        """
        self.onOffBtn.clicked.connect(self.buttonClickHandler)
        STYLE_DATA.signal.changeFont.connect(self.changeFont)

    def changeFont(self):
        """ 
        called when the gui's font size mode changed
        """
        self.label.changeFont(STYLE_DATA.FontSize.BTN)
'''
File: CheckBox.py
Project: GailBot GUI
File Created: Thursday, 12th January 2023 1:24:08 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 12th January 2023 1:51:57 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: Implement a checkbox widget
'''
import os
from .FormWidget import FormWidget
from ..Label import Label
from view.config.Style import STYLE_DATA
from config_frontend import PROJECT_ROOT
from PyQt6.QtWidgets import QWidget, QHBoxLayout,  QCheckBox

""" style sheet of the CheckBox """
CHECKBOX_STYLESHEET = \
""" 
QCheckBox {{
    spacing: 5px;
}}
QCheckBox::indicator:unchecked {{
    image: url({0});
    width: 30px;
    height:30px;
}}

QCheckBox::indicator:unchecked:hover {{
    image: url({1});
    width: 30px;
    height:30px;
}}

QCheckBox::indicator:unchecked:pressed {{
    image: url({2});
    width: 30px;
    height:30px;
}}

QCheckBox::indicator:checked {{
    image: url({2});
    width: 30px;
    height:30px;
}}

QCheckBox::indicator:checked:hover {{
    image: url({2});
    width: 30px;
    height:30px;
}}

QCheckBox::indicator:checked:pressed {{
      image: url({0});
    width: 30px;
    height:30px;
}}

QCheckBox::indicator:indeterminate:hover {{
    image: url({1});
    width: 30px;
    height:30px;
}}

QCheckBox::indicator:indeterminate:pressed {{
      image: url({1});
    width: 30px;
    height:30px;
}}

"""
class CheckBox(QWidget, FormWidget):
    
    def __init__(self, label:str, state = False, *args, **kwargs) -> None:
        """construct an instance of checkbox widgetq

        Args:
            label (str): the text that will be displayed next to the checkbox,
                         which illustrates the purpose of the checkbox
            state (bool, optional): the initial state of the checkbox. Defaults to False.
        """
        super(CheckBox, self).__init__(*args, **kwargs)
        self.label = label 
        self.state = state 
        self.initUI()
        
    def initUI(self):
        """ initialize the checkbox ui """
        self._layout = QHBoxLayout()
        self.checkBox = QCheckBox()
        self.label = Label(self.label, STYLE_DATA.FontSize.INSTRUCTION_CAPTION, STYLE_DATA.FontFamily.MAIN)
        self.setLayout(self._layout)
        self._layout.addWidget(self.checkBox)
        self._layout.addWidget(self.label)
        self._layout.setSpacing(20)
        self._layout.addStretch()
        self.checkBox.setChecked(self.state)
        self.setContentsMargins(0,0,0,0)
        self.setFixedHeight(50)
        self.setStyle()
        STYLE_DATA.signal.changeColor.connect(self.setStyle)
        STYLE_DATA.signal.changeFont.connect(self.changeFont)
    
    def setStyle(self):
        """ initialize the style of the checkbox """
        self.checkBox.setStyleSheet(CHECKBOX_STYLESHEET.format(
            os.path.join(PROJECT_ROOT, STYLE_DATA.Asset.unchecked),
            os.path.join(PROJECT_ROOT, STYLE_DATA.Asset.hover),
            os.path.join(PROJECT_ROOT, STYLE_DATA.Asset.checked),
        ))
    
        
    def setValue(self, value: bool):
        """ set the value of the checkbox to be value """
        self.checkBox.setChecked(value)
    
    def getValue(self):
        """ get the value of the checkbox """
        return self.checkBox.isChecked()
    
    def isChecked(self) -> bool:
        """ return a boolean that indicates if the checkbox is checked or not """
        return self.checkBox.isChecked()
   
    def enable(self):
        """ enable the checkbox to be checkable """
        self.checkBox.setCheckable(True)
    
    def disable(self):
        """ disable the checkbox to be checkable """
        self.checkBox.setCheckable(False)
    
    def changeFont(self):
        """ called when the gui's font size mode is changed  """
        self.label.changeFont(STYLE_DATA.FontSize.INSTRUCTION_CAPTION)
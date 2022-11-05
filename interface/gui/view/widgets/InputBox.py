'''
File: InputBox.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 1:44:14 pm
Modified By:  Siara Small  & Vivian Li
-----
'''
from util.SytemSet import SysFontSize,  SysStyleSheet
from util.Config import Color, FontSize, Dimension

from view.style.styleValues import (
    Dimension, 
)
from view.widgets import (
    Label
)

from PyQt6.QtWidgets import (
    QComboBox, 
    QWidget, 
    QHBoxLayout, 
    QLineEdit,
    QVBoxLayout
)
from PyQt6.QtCore import QSize, Qt

class InputBox(QWidget):
    """ an input box widget

    Args: 
        label(str): the label of the input Field 
    """
    def __init__(
        self, 
        label:str, 
        vertical  = False, 
        labelSize = SysFontSize.body, 
        inputText = None,
        selections = None,
        *args, 
        **kwargs) -> None:
        """initialize input box"""
        super().__init__(*args, **kwargs)
        self.label = label
        self.vetical = vertical
        self.lableSize = labelSize
        self.inputText = inputText
        self.selections = selections
        self._initWidget()
        self._initLayout()

 

    def value(self) -> str: 
        """ public function to ge the value of the input """
        return self.inputFeild.text()

    def setText(self,text:str):
        """set the current text of the input field

        Args:
            text (str): text content
        """
        self.inputFeild.setText(text)
    
    def disable(self):
        """ a public function to disable the edit """
        self.inputFeild.setReadOnly(True)
    
    
    def enable(self):
        """ a public function to enable the edit """
        self.inputFeild.setReadOnly(False)
    
    def _initWidget(self):
        """initialize widgets for input box"""
        self.inputlabel = Label.Label(self.label, self.lableSize)
        self.inputFeild = InputField(self) 
        self.inputFeild.setMaximumSize(Dimension.INPUTFIELD)
        if self.inputText:
            self.setText(self.inputText)
            
    def _initLayout(self):
        """initialize layouts for input box"""
        if self.vetical:
            self.layout = QVBoxLayout(self)
        else:
            self.layout = QHBoxLayout(self)

        self.setLayout(self.layout)
        self.layout.addWidget(self.inputlabel) 
        self.layout.addWidget(
            self.inputFeild, 
            alignment=Qt.AlignmentFlag.AlignLeft)
    

class InputField(QLineEdit):
    """ the input field of input box"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setFixedSize(Dimension.INPUTFIELD)
        

class InputCombo(InputBox):
    def __init__(
        self,
        selections:list, 
        label:str, 
        vertical = False, 
        labelSize = FontSize.BODY, 
        inputText = None,
        *args, **kwargs) -> None:
        
        super().__init__(
        label,
        vertical,
        labelSize,
        inputText,
        selections,
        *args, **kwargs)
        """ an combobox with an label on top 
            Args:
            selections (list) :  a list of selections available for the combo box
            vertical : true if the display of the combobox and the label will be 
                       in vertical layout  
            labelSize: the size of the label
            inputText: the default text displayed on the combo box
        """
        self.selections = selections 
    
    def _initWidget(self):
        """initialize widgets for input box"""
        self.inputlabel = Label.Label(self.label, self.lableSize)
        self.inputFeild = ComboSelection(self.selections)
        self.inputFeild.setStyleSheet("")
        
    def value(self):
        """ return the value of the input """
        return self.inputFeild.currentText()
    
    def setText(self,text:str):
        """ set the current text of the combo box """
        self.inputFeild.setCurrentText(text)
    
    def disable(self):
        """ disable the edit of the combo box """
        self.inputFeild.setDisabled(True)
    
    def enable(self):
        self.inputFeild.setDisabled(False)
        

class ComboSelection(QComboBox):
    """ a costomized combobox 
        Args: 
        slections: a list of available options 
    """
    def __init__(self, selections:list, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.addItems(selections)


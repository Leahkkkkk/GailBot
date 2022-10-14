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
from view.style.styleValues import (
    FontSize, 
    Dimension, 
    Color, 
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
        vertical = False, 
        labelSize = FontSize.BODY, 
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
        self._connectSignal()

    def value(self):
        """ public function to ge the value of the input """
        return self.inputFeild.text()
    
    def setText(self,text:str):
        self.inputFeild.setText(text)
    
    def disableEdit(self):
        self.inputFeild.setReadOnly(True)
    
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
        self.layout.addWidget(self.inputFeild, alignment=Qt.AlignmentFlag.AlignLeft)
    
    def _connectSignal(self):
        """connect signal- dummy for now"""
        pass


class InputField(QLineEdit):
    """ the input field of input box"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setStyleSheet(f"font-size: {FontSize.TEXT_FIELD};"
                           f"padding:0;"
                           f"border: 1px solid {Color.BORDERGREY} ")
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
        
        self.selections = selections 
    
    def _initWidget(self):
        """initialize widgets for input box"""
        self.inputlabel = Label.Label(self.label, self.lableSize)
        self.inputFeild = ComboSelection(self.selections)
        self.inputFeild.setMaximumSize(Dimension.INPUTFIELD)


    def value(self):
        """ public function to ge the value of the input """
        return self.inputFeild.currentText()
    
    def setText(self,text:str):
        self.inputFeild.setCurrentText(text)
    
    def disableEdit(self):
        self.inputFeild.setEditable(False)

class ComboSelection(QComboBox):
    def __init__(self,selections:list, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.addItems(selections)

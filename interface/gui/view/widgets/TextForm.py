'''
File: TextForm.py
Project: GailBot GUI
File Created: Friday, 4th November 2022 1:01:27 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Friday, 4th November 2022 5:57:10 pm
Modified By:  Siara Small  & Vivian Li
-----
'''


from typing import Dict 
from view.widgets import Label, InputBox, Button
from util.Config import FontFamily, FontSize, Dimension
from util.SytemSet import SysColor 
from view.style.Background import initBackground

from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout)


class TextForm(QWidget):
    def __init__(self, 
                 data: Dict[str, str], 
                 backgroundColor: str = SysColor.subBackground,
                 *args, **kwargs) -> None:
        """ Display a form 

        Args:
            data (Dict[str, str]): a dictionary that stores the form 
                                   and initial values of the form 
            backgroundColor str  : the background color
        """
        super().__init__(*args, **kwargs)
        self.data = data
        self.backgroundColor = backgroundColor 
        self.inputDict = dict()
        self._initWidget()
        self._initStyle()


    def getValue(self) -> Dict[str, str]:
        """ public function that return the result of the form in a dictionary 

        Returns:
            Dict[str, str] a dictionary that stores the form values from the user
        """
        value = dict()
        for key, input in self.inputDict.items():
            value[key] = input.value()
        return value
            
    
    def setValues(self, data: Dict[str, str]):
        """ public function to update the widget values
        
        Args:
            data (Dict[str, str]): a dictionary that stores the values to be 
                                   updated 
        """
        for key, input in self.inputDict.items():
            input.setText(data[key])
    
    def _initWidget(self):
        """ initialize the widget """
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(Dimension.STANDARDSPACING)
 
        for key, items in self.data.items():
            newLabel = Label.Label(key, FontSize.BTN, FontFamily.MAIN)
            self.layout.addWidget(newLabel)
            for key, value in items.items():
                keyCopy = key
                if "bool" in key:
                    key = key.replace("bool", "") 
                    newInput = Button.onOffButton(key, value == value)
                elif "combo" in key:
                    key = key.replace("combo","")
                    newInput = InputBox.InputCombo(label=key, selections=value)
                else:
                    newInput = InputBox.InputBox(key, inputText=value)
                self.layout.addWidget(newInput)
                self.inputDict[keyCopy] = newInput
       
    def _initStyle(self):
        """ initialize the widget style """
        initBackground(self, self.backgroundColor)
        

        
    

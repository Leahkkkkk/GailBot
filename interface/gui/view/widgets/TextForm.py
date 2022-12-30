'''
File: TextForm.py
Project: GailBot GUI
File Created: Friday, 4th November 2022 1:01:27 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Friday, 4th November 2022 5:57:10 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: a form widget that implement a form that takes in user input 
'''
from dataclasses import dataclass
from typing import Dict 

from view.widgets import (
    Label, 
    InputBox, 
    Button,
    ToggleView
)
from util.Style import (
    FontFamily, 
    FontSize, 
    Dimension, 
    Color
)
from view.widgets.Background import initSecondaryColorBackground

from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout,
)
from PyQt6.QtCore import Qt

@dataclass
class InputFormat:
    BOOL = " bool"
    COMBO = " combo"
    DEPENDENT_COMBO = " dependent combo"
    
    
class TextForm(QWidget):
    def __init__(self, 
                 data: Dict[str, str], 
                 background : bool = True,
                 toggle : bool = False, 
                 *args, **kwargs) -> None:
        """ Displays a form 

        Constructor Args:
            data (Dict[str, str]): a dictionary that stores the form 
                                   and initial values of the form 
            backgroundColor (bool)  : if true, the background is auto filled 
                                      with default color
        
        Public Functions:
        1. enableForm(self) -> None
        2. disableForm(self) -> None
        3. getValue(self) -> Dict[str, str]
        4. setValues(self, data: Dict[str, str])
        """
        super().__init__(*args, **kwargs)
        self.data : Dict[str, dict] = data
        self.inputDict = dict()
        self.toggle = toggle 
        self.setMinimumHeight(Dimension.WIN_MIN_HEIGHT // 3 * 2)
        self.setMinimumWidth(Dimension.WIN_MIN_WIDTH // 2)
        self._initWidget()
        self._initLayout()
        if background:
            self._initStyle()
    
    def enableForm(self) -> None:
        """ public function that enable the form edit """
        for key, input in self.inputDict.items():
            input.enable()
            input.setStyleSheet("color:black;")
            
    
    def disableForm(self) -> None:
        """ public function that disable the form edit """
        for key, input in self.inputDict.items():
            input.disable()
            input.setStyleSheet("color:grey;")
     
            
    def getValue(self) -> Dict[str, str]:
        """ public function that return the result of the form in a dictionary 

        Returns:
            Dict[str, str] a dictionary that stores the form values from the user
        """
        value = dict()
        for key, input in self.inputDict.items():
            value[key] = input.value()
        return value
            
    def setValues(self, data: Dict[str, str]) -> None:
        """ public function to update the widget values
        
        Args:
            data (Dict[str, str]): a dictionary that stores the values to be 
                                   updated 
        """
        for key, input in self.inputDict.items():
            input.setText(data[key])
    
    def _initWidget(self):
        """ initializes the widgets """
        self.mainContainer = QWidget()
        self.mainContainer.setMinimumWidth(Dimension.INPUTWIDTH * 2)
        self.mainVertical = QVBoxLayout()
        self.mainContainer.setLayout(self.mainVertical)
        self.mainVertical.setSpacing(10)
        count = 0
        
        for tittleKey, items in self.data.items():
            """ adding spacing """
            if count != 0 and not self.toggle:
                self.mainVertical.addSpacing(Dimension.LARGE_SPACING)
            count += 1
            
            """ create additional layout if the form elements are 
            displayed in a toggle view """
            if self.toggle:
                toggleViewContainer = QWidget()
                toggleViewLayout = QVBoxLayout()
                toggleViewContainer.setLayout(toggleViewLayout)
            
            """ create the label  """
            tittleKey = tittleKey.split(". ")[-1]
            if not self.toggle:
                newLabel = Label.Label(tittleKey, FontSize.BTN, FontFamily.MAIN)
                self.mainVertical.addWidget(newLabel)
            
            """ create the form component element """
            for key, value in items.items():
                keyCopy = key
                if InputFormat.BOOL in key:
                    key = key.replace( InputFormat.BOOL, "").split(". ")[-1]
                    newInput = Button.onOffButton(key, value == value)
                elif InputFormat.COMBO in key:
                    key = key.replace( InputFormat.COMBO, "").split(". ")[-1]
                    if self.toggle:
                        newInput = InputBox.InputCombo(
                            label=key, selections=value, vertical=True)
                    else:
                        newInput = InputBox.InputCombo(
                            label=key, selections=value)
                        newInput.setMinimumHeight(80)
                else:
                    key = key.split(". ")[-1]
                    newInput = InputBox.InputBox(key, inputText=value)
                
                """ add element to the layout """
                if self.toggle : 
                    toggleViewLayout.addWidget(newInput)
                else:
                    self.mainVertical.addWidget(newInput)
                self.inputDict[key] = newInput
            
            if self.toggle:
                toggleViewLayout.addStretch()
                toggleViewContainer.setFixedHeight(len(items.values()) * 120)
                toggleView = ToggleView.ToggleView (
                    tittleKey, 
                    toggleViewContainer,
                    headercolor = Color.MAIN_BACKRGOUND, 
                    viewcolor = Color.MAIN_BACKRGOUND)
                
                self.mainVertical.addWidget(toggleView)
        self.mainVertical.addStretch()
                
    def _initLayout(self):
        """ initialize the layout """
        self.setLayout(self.mainVertical)
        
    def _initStyle(self):
        """ initializes the widget style """
        initSecondaryColorBackground(self)
    
    def addWidget(self, widget, alignment = Qt.AlignmentFlag.AlignLeft):
        """ add widget to the Text form under the same column """
        self.mainVertical.addWidget(widget, alignment=alignment)

   

        
    

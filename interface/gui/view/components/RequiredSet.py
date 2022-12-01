'''
File: RequiredSet.py
Project: GailBot GUI
File Created: Friday, 4th November 2022 1:01:27 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Tuesday, 8th November 2022 4:00:50 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: implementation of the required setting form 
'''

from typing import Dict 

from view.widgets import ToggleView
from view.components.SpeechEngineForm import SpeechEngineForm
from view.components.OutputFormatForm import OutPutFormat
from util.Text import CreateNewProfilePageText as Text 
from util.Style import Dimension

from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
)
from PyQt6.QtCore import Qt

class RequiredSet(QWidget):
    """ implementation of a form that allow user to create required setting 
    
    Public Functions: 
    1.  getValue() -> Dict[str, dict] 
        get the form value
    2.  setValue(data: Dict[str, dict]) -> None
        taking a dictionary that stores the form values, and load those
        form values
    
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._initWidget()
        self._initLayout()
         
    def _initWidget(self):
        """initialize widgets"""
        self.engineForm = SpeechEngineForm()
        self.engineFormView = ToggleView.ToggleView(
            Text.engineSettingHeader,self.engineForm, header = True)
        self.engineFormView.setScrollHeight(self.engineForm.height())
        self.outPutForm = OutPutFormat()
        self.outPutFormView = ToggleView.ToggleView(
            Text.outputSettingHeader, self.outPutForm, header = True)
        self.outPutFormView.setScrollHeight(self.outPutForm.height())
        self.outPutFormView.setScrollHeight(Dimension.OUTPUT_FORM_HEIGHT)
        self.engineFormView.Btn.clicked.connect(self.outPutFormView.hideView)
        self.outPutFormView.Btn.clicked.connect(self.engineFormView.hideView)

    def _initLayout(self):
        """initialize layout"""
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addWidget(
            self.engineFormView, alignment=Qt.AlignmentFlag.AlignTop)
        self.verticalLayout.addWidget(
            self.outPutFormView, stretch = 2, alignment=Qt.AlignmentFlag.AlignTop)  
    
    def setValue(self, data: Dict [str, dict]):
        """ a public function to set the form value

        Args:
            data (Dict[str, Dict[str, dict]]): a dictionary that stores the 
                                               profile values
        """
        self.engineForm.setValue(data["Engine"])
        self.outPutForm.setValue(data["Output Form Data"])
    
    def getValue(self) -> Dict [str, dict]:
        """ a public function that get the file value

        Returns:
            dict: returns a dictionary that stores the profile values
        """
        profile = dict() 
        profile["Engine"] = self.engineForm.getValue()
        profile["Output Form Data"] = self.outPutForm.getValue()
        return profile

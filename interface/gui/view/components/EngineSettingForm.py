'''
File: EngineSettingForm.py
Project: GailBot GUI
File Created: Friday, 4th November 2022 1:01:27 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Tuesday, 8th November 2022 4:00:50 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: implementation of the required setting form 
'''

from typing import Dict, TypedDict

from view.widgets import ToggleView, DependentCombo
from view.config.Text import EngineForm
from view.config.Text import ProfilePageText as Text 
from view.config.Style import Dimension
from gbLogger import makeLogger


from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
)
from PyQt6.QtCore import Qt
    
class EngineSettingForm(QWidget):
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
        self.logger =  makeLogger("F")
        
    def _initWidget(self):
        """initialize widgets"""
        self.engineForm = DependentCombo(
            EngineForm.Engine, Text.selectengine, Text.formPivotKey)
        self.toggleView = ToggleView(
            Text.engineSettingHeader, self.engineForm, header = True)
        self.toggleView.setScrollHeight(Dimension.OUTPUT_FORM_HEIGHT)
    
    def _initLayout(self):
        """initialize layout"""
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addWidget(
            self.toggleView, alignment=Qt.AlignmentFlag.AlignTop)
    
    def setValue(self, data: Dict [str, dict]):
        """ a public function to set the form value

        Args:
            data (Dict[str, Dict[str, dict]]): a dictionary that stores the 
                                               profile values
        """
        self.logger.info(f"try to set the data {data}")
        self.engineForm.setValue(data)
    
    def getValue(self) -> Dict [str, dict]:
        """ a public function that get the file value

        Returns:
            dict: returns a dictionary that stores the profile values
        """
        profile = self.engineForm.getValue()
        return profile
